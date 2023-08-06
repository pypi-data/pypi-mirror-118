"""
This module is a plugin for napari in which you can add the pixel spacing (voxel size) to the metadata of the layer 

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""

import magicgui
from magicgui.widgets import LineEdit
from napari_plugin_engine import napari_hook_implementation
from magicgui import magic_factory
from napari.layers import Labels as Labellayer
from napari.layers import Image as ImageLayer

from napari.viewer import Viewer
import mrcfile
from numpy import ndarray, ones 


pixel_spacing_tooltip = "The pixel spacing (Å/pixel) to be added to layers (will be automatically changed when \"Scan\" is used)"
scanner_tooltip = "Scan the layers (Image and Labels) for information about the pixel spacing and use the first found value for the layers"
adjust_all_tooltip = "Add the pixel spacing to all found label layers not just the currently selected"


@magic_factory(pixel_spacing={"widget_type":"LineEdit", "label":"Å/Pixel","value":"1.0", "tooltip":pixel_spacing_tooltip},
 scanner={"widget_type":"CheckBox", "label":"Scan", "value":True, "tooltip":scanner_tooltip},
 call_button="(Scan and) adjust selected layer",adjust_all={"widget_type":"CheckBox", "label":"Adjust all", "value":True, "tooltip":adjust_all_tooltip} )
def PixelSpacing(pixel_spacing: float, napari_viewer: Viewer, scanner: bool, adjust_all: bool):
    if not adjust_all:
        layers = [napari_viewer.layers.selection.active]
        if not isinstance(layers[0], (Labellayer, ImageLayer)):
            layers = []
        
    else:
        layers = [l for l in napari_viewer.layers if isinstance(l, (Labellayer))]
    
    
    ps = float(pixel_spacing)


    if scanner:
        for l in napari_viewer.layers:
            if l.source.path is None:
                continue
            elif "pixel_spacing" in l.metadata:
                ps = l.metadata["pixel_spacing"]
                break
            elif l.source.path.endswith(".mrc"):
                mrc = mrcfile.open(l.source.path, permissive=True, header_only=True)
                ps = mrc.voxel_size.x
                
                break

    assert isinstance(ps, (float, int, ndarray))
    

    PixelSpacing.pixel_spacing.value = ps
    for layer in layers:
        layer.metadata["pixel_spacing"] = ps
    


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return PixelSpacing
