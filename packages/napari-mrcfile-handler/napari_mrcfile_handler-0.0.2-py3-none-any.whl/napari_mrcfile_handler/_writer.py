"""
This module is a mrcfile writer plugin for napari

It implements the ``napari_get_writer`` and ``napari_write_image`` hook specifications.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs
"""

from napari_plugin_engine import napari_hook_implementation
import mrcfile
import numpy as np




def write_mrc_file(path, data, meta, layertype):
    if not path.endswith((".mrc")):
        return None
    if layertype == "label":
        data = data.astype(np.int16)
    

    voxel_size = 1
    if "pixel_spacing" in meta["metadata"]:
        voxel_size = meta["metadata"]["pixel_spacing"]
    

    with mrcfile.new(path, overwrite=True) as mrc:
        mrc.set_data(data)
        mrc.voxel_size = voxel_size
        mrc.update_header_from_data()

    return path

@napari_hook_implementation
def napari_write_image(path, data, meta):
    return write_mrc_file(path, data, meta, "image")


@napari_hook_implementation
def napari_write_labels(path, data, meta):
    return write_mrc_file(path, data, meta, "label")

