# todo : license

import bpy


class MaterialIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer, meshobj, indent=0):

        def write_with_indent(idnt, content):
            writer.write('\t' * idnt + content)

        def find_node(nodes, name):
            for n in nodes:
                if n.bl_idname == name:
                    return n
            return None

        # Get output node from active material
        material = meshobj.active_material
        output_node = find_node(material.node_tree.nodes, 'ShaderNodeOutputMaterial')

        if output_node is None:
            raise Exception('Cannot find output node for material : %s' %material.name)

        # Get PBRT shader node from output surface socket
        shader = output_node.inputs['Surface'].links[0].from_node
        # Export from the shader node
        if hasattr(shader, 'export'):
            shader.export(indent, writer)

        else:
            raise Exception('None pbrt material assigned : %s' %shader.name)
