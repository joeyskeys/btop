# todo : license goes here

import os

bl_info = {
    "name": "btop",
    "author": "Joey Chen",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "PBRT Renderer",
    "warning": "",
    "category": "Render"
}

if "bpy" in locals():
    import importlib

    importlib.reload(ui)

else:
    import bpy


def register():
    print('register pbrt')
    from . import render
    from . import ui
    from . import nodes

    render.register()
    ui.register()
    nodes.register()


def unregister():
    from . import render
    from . import ui
    from . import nodes

    render.unregister()
    ui.unregister()
    nodes.unregister()


if __name__ == '__main__':
    register()