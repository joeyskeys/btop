# todo : license

import bpy


class PBRTShaderNode(bpy.types.ShaderNode):
    """
    Base class for PBRT shading nodes
    """

    bl_compatibility = {'PBRT'}
    bl_icon = 'MATERIAL'

    @classmethod
    def poll(cls, tree: bpy.types.NodeTree):
        return tree.bl_idname in ('ShaderNodeTree', 'PBRTTreeType') and bpy.context.scene.render.engine == 'PBRT_RENDER'

    def create_sockets_from_dict(self, sock_dict):
        for key, value in self.sock_dict.items():
            self.inputs.new(key, value[0]).default_value = value[1]

    def init(self, context):
        self.create_sockets_from_dict(self.socket_dict)
        self.outputs.new('NodeSocketShader', 'Shader')

    def get_data_dict(self):
        param_dict = {
            'name': self.name,
            'type': self.shader_type,
            'params': {}
        }

        for key, value in self.sock_dict.items():
            sock = self.inputs[key]
            if sock.is_linked:
                from_node = sock.links[0].from_node
                param_dict['params'][key] = ('texture {}'.format(key), from_node.name)
            else:
                # float type socket
                if sock.type == 'VALUE':
                    sock_value = '{}'.format(sock.default_value)
                # color type socket
                elif sock.type == 'RGBA':
                    rgba_v = sock.default_value
                    sock_value = '[{} {} {}]'.format(rgba_v[0], rgba_v[1], rgba_v[2])
                else:
                    raise Exception('socket type unsupported : {}'.format(sock.type))

        return param_dict


class PBRTShaderNodeDisney(PBRTShaderNode):
    bl_label = 'PBRT Disney Shader'

    shader_type = 'disney'

    socket_dict = {
        'color': ('NodeSocketColor', (0.5, 0.5, 0.5, 1.0)),
        'anisotropic': ('NodeSocketFloat', 0),
        'clearcoat': ('NodeSocketFloat', 0),
        'clearcoatgloss': ('NodeSocketFloat', 0),
        'eta': ('NodeSocketFloat', 1.5),
        'metallic': ('NodeSocketFloat', 0),
        'roughness': ('NodeSocketFloat', 0.5),
        'scatterdistance': ('NodeSocketVector', (0, 0, 0)),
        'sheen': ('NodeSocketFloat', 0),
        'sheentint': ('NodeSocketFloat', 0.5),
        'spectrans': ('NodeSocketFloat', 0),
        'speculartint': ('NodeSocketFloat', 0),
        'difftrans': ('NodeSocketColor', (1, 1, 1)),
        'flatness': ('NodeSocketColor', (0, 0, 0)),
    }

    thin = bpy.props.BoolProperty(name="thin",
                                  description="Controls whether the thin is enabled surface model",
                                  default=False)

    def draw_buttons(self, context, layout: 'UILayout'):
        layout.prop(self, 'thin')
        self.inputs['difftrans'].enabled = self.thin
        self.inputs['flatness'].enabled = self.thin



class PBRTShaderNodeFourier(PBRTShaderNode):
    bl_label = 'PBRT Fourier Shader'

    shader_type = 'fourier'

    bsdffile = bpy.props.StringProperty(name="bsdffile",
                                        description="File that stores the Fourier BSDF description",
                                        )

    def draw_buttons(self, context, layout: 'UILayout'):
        layout.prop(self, 'bsdffile')