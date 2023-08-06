import json
import math
import os
import shutil
import sys
import time
from ast import literal_eval

import dask.array as da
import h5py as h5
import numpy as np
import pkg_resources
import zarr
from distributed import Client
from musictune.deconvolution.deconvolve import deconvolve_parallel
from musictune.io.modules import decompress, merge_lines, reposition_lines
from musictune.io.utilities import read_config, get_save_path, get_files, opt_chunksize, from_zarr, to_zarr

f = open(sys.argv[1], "r")
param = json.loads(f.read())
f.close()

config_path = param['config_path']
f = open(config_path, "r")
config = json.loads(f.read())
f.close()

# directories and range options
s = param['range']['sessions']
l = param['range']['lasers']
d = param['range']['pzf_dirs']

sessions = read_config(config_path, s, l, d)

z_range = str(param['range']['z_range'])

# Line weights and paramters
line_weights_file = param['lines']['weights_file']
option = param['lines']['weights_option']
line_no = param['lines']['single_line_no']

# Deconvolution parameters
deconv_status = literal_eval(param['deconvolve']['status'])
overlap = literal_eval(param['deconvolve']['overlap'])
psf_path = param['deconvolve']['psf_path']
psf_res = param['deconvolve']['psf_res']
iterations = int(param['deconvolve']['iterations'])
td = param['save']['tmp_dir']

tmp_chunks = literal_eval(param['save']['tmp_chunks'])
xy_chunks = literal_eval(param['save']['xy_chunks'])
zchunk_range = [*map(int, param['save']['zchunk_range'].split('-'))]

n_workers = param['cluster']['n_workers']
threads_per_worker = param['cluster']['threads_per_worker']
ld = param['cluster']['local_directory']

local_directory = os.environ.get(ld)
if not local_directory:
    local_directory = ld

tmp_dir = os.environ.get(td)
if not tmp_dir:
    tmp_dir = td

if line_weights_file == "":
    f = open(pkg_resources.resource_filename("musictune", 'data/Weights.json'), "r")
    weights = json.loads(f.read())
    f.close()
else:
    f = open(line_weights_file, "r")
    weights = json.loads(f.read())
    f.close()

if psf_path == "measured":
    psf_path = pkg_resources.resource_filename("musictune", 'data/PSF/CV_us_640_fine.tif')
    psf_res = (0.23325, 0.23325, 0.23325)
elif psf_path == "theoretical":
    psf_path = pkg_resources.resource_filename("musictune", 'data/PSF/PSF_16bit_full.tif')
    psf_res = (0.933, 0.933, 0.933)

# if __name__ == "__main__":
#     client = Client(processes=False, n_workers=n_workers, threads_per_worker=threads_per_worker,
#                     local_directory=local_directory)

client = Client('tcp://127.0.0.1:'+sys.argv[2])
print(client)

start_time = time.time()

start_index = weights['ReadCrop']['index']
crop_length = weights['ReadCrop']['length']
weight = np.array(weights['Weight'])
weighted_pixels = np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels'])

save_root = os.path.join(get_save_path(config['Basename']["Project"]), config['Basename']["Sample"])
save_dir = os.path.join(save_root, config['Basename']["Sequence"])

for sess in sessions:
    print(f"Processing session: {sess}")
    img_res = sessions[sess]['Image Resolution']
    print(f"Image resolution: {img_res}")
    psf_invert = not sessions[sess]['Reversed']

    lasers = sessions[sess]['Files']
    grid = 1e8 * np.arange(sessions[sess]['Image Start'], sessions[sess]['Image End'],
                           sessions[sess]['Pixel Size'] * sessions[sess]['Scale Factor'])

    for las in lasers:
        print(f"\tProcessing Lasers: {las}")
        directories = lasers[las]

        for pzf_dir in directories:
            print(f"\t\tProcessing PZF directory: {pzf_dir}")

            block = get_files(pzf_dir, z_range=z_range)

            sample = decompress(block['pzf_files'][0]).compute()

            delayed_planes = [decompress(fn) for fn in block['pzf_files']]
            delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4') for x in delayed_planes]

            da_line_planes = da.stack(delayed_planes)

            coordinate_file = h5.File(block['h5_filepath'], 'r')
            coordinates = da.from_array(
                np.expand_dims(np.array([coordinate_file.get(fn.split(os.sep)[-1])[:] for fn in block['pzf_files']]),
                               1), chunks=(1, 1, da_line_planes.chunksize[-1]))

            ## Merge lines
            merge_chunk_size = (1, da_line_planes.chunksize[1], 1, da_line_planes.chunksize[3])

            da_planes = da.map_blocks(merge_lines, da_line_planes, weighted_pixels, option=option,
                                      start_index=start_index,
                                      crop_length=crop_length, line_no=line_no, chunks=merge_chunk_size,
                                      dtype='f4').squeeze()

            da_planes_repositioned = da.map_blocks(reposition_lines, da_planes, coordinates, grid, dtype='f4')

            save_path = os.path.join(save_dir, *pzf_dir.split(os.sep)[-2:]) + '.zarr'
            tmp_save_path = tmp_dir + save_path

            shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), da_planes.shape, tmp_chunks))

            store = zarr.NestedDirectoryStore(tmp_save_path)
            z_out = zarr.create(shape=shape, chunks=tmp_chunks, dtype=da_planes.dtype, store=store, overwrite=True,
                                fill_value=0)

            print(f"\t\tSaving tmp image: {tmp_save_path}")
            tp = da.to_zarr(da_planes, z_out)

            chunk_size = opt_chunksize(da_planes.shape[0], xy_chunks, zchunk_range[0], zchunk_range[1])

            dask_img = from_zarr(tmp_save_path, chunk_size=chunk_size)
            print(f"\t\tRechunking image: {dask_img}")

            if deconv_status:
                print("\t\tDeconvolving")

                dask_img = deconvolve_parallel(dask_img,
                                               img_resolution=img_res,
                                               chunk_size=chunk_size,
                                               overlap=overlap,
                                               psf_invert=psf_invert,
                                               psf_path=psf_path,
                                               psf_res=psf_res,
                                               iterations=iterations)

            path = to_zarr(dask_img, prefix='', chunk_size=chunk_size, save_path=save_path)

            print(f"\t\tSaved:{path}")

            shutil.rmtree(tmp_save_path)
            print("\t\tTmp file removed\n")

elapsed_time = time.time() - start_time
print("Elapsed time:", elapsed_time)

config["ZARR Conversion"] = param
config["ZARR Conversion"]["elapsed_time"] = elapsed_time

with open(os.path.join(save_root, config['Basename']['Sequence'] + '.json'), 'w') as outfile:
    json.dump(config, outfile, indent=4)

client.close()
