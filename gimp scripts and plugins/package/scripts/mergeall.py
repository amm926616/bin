#!/usr/bin/env python3

import sys
import gi
gi.require_version('Gimp', '3.2')
from gi.repository import Gimp, Gio, GLib

class MergeAllLayersPlugin(Gimp.PlugIn):

    def do_query_procedures(self):
        return ["python-fu-merge-all-layers"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None
        )

        procedure.set_menu_label("Merge ALL Layers")
        procedure.add_menu_path("<Image>/File")

        procedure.set_documentation(
            "Merge all layers in all open images",
            "Loops through all open images and merges visible layers",
            name
        )

        procedure.set_attribution(
            "You", "You", "2026"
        )

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, data):
        # Get all open images
        images = Gimp.list_images()

        for img in images:
            # Merge visible layers (equivalent to CLIP-TO-IMAGE)
            img.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(MergeAllLayersPlugin.__gtype__, sys.argv)
