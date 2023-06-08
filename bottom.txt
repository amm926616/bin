#!/usr/bin/env python

def set_active_layer_to_bottom():
    images = gimp.image_list()
    for image in images:
        bottom_layer = image.layers[-1]
        pdb.gimp_image_set_active_layer(image, bottom_layer)

set_active_layer_to_bottom()