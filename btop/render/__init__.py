# todo : license goes here

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
        exporter.export("/home/joey/Desktop/scene.pbrt")

    def view_update(self, context, depsgraph):
        pass

    def view_draw(self, context, depsgraph):
        pass


def register():
    bpy.utils.register_class(PBRTRenderEngine)


def unregister():
    bpy.utils.unregister_class(PBRTRenderEngine)