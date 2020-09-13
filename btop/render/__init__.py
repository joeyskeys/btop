# todo : license goes here

import os
import subprocess

import bpy

from ..logger import get_logger
from ..sceneio import PBRTExporter


class PBRTRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'PBRT_RENDER'
    bl_label = 'pbrt'
    bl_use_preview = True
    bl_use_shading_nodes_custom = False
    bl_use_postprocess = True

    # Constructor
    def __init__(self):
        self.renderer = None

    def __del__(self):
        pass

    def render(self, depsgraph):
        exporter = PBRTExporter()

        setting_props = bpy.context.scene.pbrt_setting_props
        filename = os.path.basename(bpy.data.filepath) or 'tmp.blend'
        pbrt_executable = setting_props.pbrt_location
        cache_filepath = os.path.join(setting_props.pbrt_cache_folder, filename.replace('.blend', '.pbrt'))
        outfile = os.path.join(setting_props.pbrt_cache_folder, filename.replace('.blend', '.exr'))

        #exporter.export("/home/joey/Desktop/scene.pbrt")
        exporter.export(cache_filepath)

        try:
            #subprocess.call([pbrt_executable, '--outfile', outfile, cache_filepath])
            cmd_comps = [pbrt_executable, '--outfile', outfile, cache_filepath]
            print('command is : ', ' '.join(cmd_comps))
            os.system(' '.join(cmd_comps))
        except Exception as e:
            print('execute pbrt command failed:\n', e)

    def view_update(self, context, depsgraph):
        pass

    def view_draw(self, context, depsgraph):
        pass


def register():
    bpy.utils.register_class(PBRTRenderEngine)


def unregister():
    bpy.utils.unregister_class(PBRTRenderEngine)