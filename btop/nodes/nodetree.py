# todo: license

import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from nodeitems_builtins import ShaderNodeCategory

from ..misc import PBRTNodeTypes, registry


@PBRTNodeTypes
class PBRTNodeTree(bpy.types.NodeTree):
    """
    PBRT node tree
    """
    bl_label = "PBRT Material Nodes"
    bl_idname = "pbrt_material_nodes"
    bl_icon = "MATERIAL"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "PBRT_RENDER"


class PBRTNodeCategory(NodeCategory):
    @classmethod
    def poll(self, context):
        return context.scene.render.engine == "PBRT_RENDER" and context.space_data.tree_type == "ShaderNodeTree"


pbrt_shader_node_category = [
    PBRTNodeCategory("PBRT_MATERIAL", "Material", items=
        [NodeItem(mat[0], mat[1]) for mat in registry.material_nodes]),

    PBRTNodeCategory("PBRT_TEXTURE", "Texture", items=
        [NodeItem(tex[0], tex[1]) for tex in registry.texture_nodes]),
]


original_poll_func = None

def hide_cycles_nodes_poll():
    @classmethod
    def func(cls, context):
        return context.scene.render.engine != "PBRT_RENDER"
    return func


def hide_func(cls, context):
    return context.scene.render.engine != "PBRT_RENDER"


def register():
    global original_poll_func
    original_poll_func = ShaderNodeCategory.poll
    ShaderNodeCategory.poll = hide_func
    nodeitems_utils.register_node_categories("PBRT_SHADER_NODES", pbrt_shader_node_category)


def unregister():
    ShaderNodeCategory.poll = original_poll_func
    nodeitems_utils.unregister_node_categories("PBRT_SHADER_NODES")