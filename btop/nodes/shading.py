# todo : license

import bpy

from ..misc import PBRTNodeTypes
from ..misc import registry


class PBRTShaderNode(bpy.types.ShaderNode):
    """
    Base class for PBRT shading nodes
    """

    bl_compatibility = {'PBRT'}
    bl_icon = 'MATERIAL'

    socket_dict = {}

    @classmethod
    def poll(cls, tree: bpy.types.NodeTree):
        return tree.bl_idname in ('ShaderNodeTree', 'PBRTTreeType') and bpy.context.scene.render.engine == 'PBRT_RENDER'

    def create_sockets_from_dict(self):
        for key, value in self.socket_dict.items():
            input_socket = self.inputs.new(value[0], key)
            if len(value) > 1 and hasattr(input_socket, 'default_value'):
                input_socket.default_value = value[1]

    def init(self, context):
        self.create_sockets_from_dict()
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


class PBRTShaderNodeWithRemapRoughness(PBRTShaderNode):
    remaproughness = bpy.props.BoolProperty(name="remaproughness",
                                            description="Roughness values are expected to be in the range [0,1] if true",
                                            default=True)

    def draw_buttons(self, context, layout: 'UILayout'):
        layout.prop(self, 'remaproughness')

    def get_data_dict(self):
        param_dict = super().get_data_dict()
        param_dict['params'].update({'remaproughness': self.remaproughness})
        return param_dict


@PBRTNodeTypes('material')
class PBRTShaderNodeDisney(PBRTShaderNode):
    bl_label = 'PBRT Disney Shader'

    class_type = 'PBRTShaderNodeDisney'
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
        'difftrans': ('NodeSocketVector', (1, 1, 1)),
        'flatness': ('NodeSocketColor', (0, 0, 0)),
    }

    def draw_buttons(self, context, layout: 'UILayout'):
        layout.prop(self, 'thin')

    def update_visibility(self, context):
        self.inputs['difftrans'].enabled = self.thin
        self.inputs['flatness'].enabled = self.thin

    thin = bpy.props.BoolProperty(name="thin",
                                  description="Controls whether the thin is enabled surface model",
                                  default=False,
                                  update=update_visibility)

    def get_data_dict(self):
        param_dict = super().get_data_dict()
        param_dict['params'].update({'thin': self.thin})
        return param_dict


@PBRTNodeTypes('material')
class PBRTShaderNodeFourier(PBRTShaderNode):
    bl_label = 'PBRT Fourier Shader'

    class_type = 'PBRTShaderNodeFourier'
    shader_type = 'fourier'

    bsdffile = bpy.props.StringProperty(name="bsdffile",
                                        description="File that stores the Fourier BSDF description",
                                        )

    def draw_buttons(self, context, layout: 'UILayout'):
        layout.prop(self, 'bsdffile')

    def get_data_dict(self):
        return {
            'name': self.name,
            'type': self.shader_type,
            'params': {'bsdffile': self.bsdffile}
        }


@PBRTNodeTypes('material')
class PBRTShaderNodeGlass(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Glass Shader'

    class_type = 'PBRTShaderNodeGlass'
    shader_type = 'glass'

    socket_dict = {
        'Kr': ('NodeSocketColor', (1.0, 1.0, 1.0)),
        'Kt': ('NodeSocketColor', (1.0, 1.0, 1.0)),
        'eta': ('NodeSocketVector', (1.5, 1.5, 1.5)),
        'uroughness': ('NodeSocketFloat', 0),
        'vroughness': ('NodeSocketFloat', 0),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeHair(PBRTShaderNode):
    bl_label = 'PBRT Hair Shader'

    class_type = 'PBRTShaderNodeHair'
    shader_type = 'hair'

    socket_dict = {
        'sigma_a': ('NodeSocketColor', (0, 0, 0)),
        'color': ('NodeSocketColor', (0, 0, 0)),
        'eumelanin': ('NodeSocketFloat', 1),
        'pheomelanin': ('NodeSocketFloat', 0.5),
        'eta': ('NodeSocketFloat', 1.55),
        'beta_m': ('NodeSocketFloat', 0.3),
        'beta_n': ('NodeSocketFloat', 0.3),
        'alpha': ('NodeSocketFloat', 2),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeKdSubsurface(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT KdSubsurface Shader'

    class_type = 'PBRTShaderNodeKdSubsurface'
    shader_type = 'kdsubsurface'

    socket_dict = {
        'Kd': ('NodeSocketColor', (0.5, 0.5, 0.5)),
        'mfp': ('NodeSocketFloat', 1),
        'eta': ('NodeSocketFloat', 1.3),
        'Kr': ('NodeSocketColor', (1.0, 1.0, 1.0)),
        'Kt': ('NodeSocketColor', (1.0, 1.0, 1.0)),
        'uroughness': ('NodeSocketFloat', 0),
        'vroughness': ('NodeSocketFloat', 0),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeMatte(PBRTShaderNode):
    bl_label = 'PBRT Matte Shader'

    class_type = 'PBRTShaderNodeMatte'
    shader_type = 'matte'

    socket_dict = {
        'Kd': ('NodeSocketColor', (0.5, 0.5, 0.5)),
        'sigma': ('NodeSocketFloat', 0),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeMetal(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Metal Shader'

    class_type = 'PBRTShaderNodeMetal'
    shader_type = 'metal'

    socket_dict = {
        'eta': ('NodeSocketColor', (1.0, 1.0, 1.0)),
        'k': ('NodeSocketColor', (0, 0, 0)),
        'roughness': ('NodeSocketFloat', 0.01),
        'uroughness': ('NodeSocketFloat', 0.01),
        'vroughness': ('NodeSocketFloat', 0.01),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeMirror(PBRTShaderNode):
    bl_label = 'PBRT Mirror Shader'

    class_type = 'PBRTShaderNodeMirror'
    shader_type = 'mirror'

    socket_dict = {
        'Kr': ('NodeSocketColor', 0.9),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeMixture(PBRTShaderNode):
    bl_label = 'PBRT Mixture Shader'

    class_type = 'PBRTShaderNodeMixture'
    shader_type = 'mix'

    socket_dict = {
        'amount': ('NodeSocketVector', (0.5, 0.5, 0.5)),
        'namedmaterial1': ('NodeSocketShader'),
        'namedmaterial2': ('NodeSocketShader'),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodePlastic(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Plastic Shader'

    class_type = 'PBRTShaderNodePlastic'
    shader_type = 'plastic'

    socket_dict = {
        'Kd': ('NodeSocketColor', (0.25, 0.25, 0.25)),
        'Ks': ('NodeSocketColor', (0.25, 0.25, 0.25)),
        'roughness': ('NodeSocketFloat', 0.1),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeSubstrate(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Substrate Shader'

    class_type = 'PBRTShaderNodeSubstrate'
    shader_type = 'substrate'

    socket_dict = {
        'Kd': ('NodeSocketColor', (0.5, 0.5, 0.5)),
        'Ks': ('NodeSocketColor', (0.5, 0.5, 0.5)),
        'uroughness': ('NodeSocketFloat', 0.1),
        'vroughness': ('NodeSocketFloat', 0.1),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeSubsurface(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Subsurface Shader'

    class_type = 'PBRTShaderNodeSubsurface'
    shader_type = 'subsurface'

    socket_dict = {
        'sigma_a': ('NodeSocketVector', (0.0011, 0.0024, 0.014)),
        'sigma_prime_s': ('NodeSocketVector', (2.55, 3.12, 3.77)),
        'eta': ('NodeSocketFloat', 1.33),
        'Kr': ('NodeSocketColor', (1, 1, 1)),
        'Kt': ('NodeSocketColor', (1, 1, 1)),
        'uroughness': ('NodeSocketFloat', 0),
        'vroughness': ('NodeSocketFloat', 0),
    }

    coefficient_name = bpy.props.StringProperty(name="name",
                                                description="Name of measured subsurface scattering coefficients",
                                                default="")

    scale = bpy.props.FloatProperty(name="scale",
                                    description="Scale factor that is applied to sigma_a and sigma_prime_s",
                                    default=1,
                                    soft_max=2,
                                    min=0)

    def draw_buttons(self, context, layout: 'UILayout'):
        layout.prop(self, 'coefficient_name')
        layout.prop(self, 'scale')
        super(PBRTShaderNodeSubsurface, self).draw_buttons(context, layout)

    def get_data_dict(self):
        data_dict = super(PBRTShaderNodeSubsurface, self).get_data_dict()
        data_dict['params']['name'] = self.coefficient_name
        data_dict['params']['scale'] = self.scale
        return data_dict


@PBRTNodeTypes('material')
class PBRTShaderNodeTranslucent(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Translucent Shader'

    class_type = 'PBRTShaderNodeTranslucent'
    shader_type = 'translucent'

    socket_dict = {
        'Kd': ('NodeSocketColor', (0.25, 0.25, 0.25)),
        'Ks': ('NodeSocketColor', (0.25, 0.25, 0.25)),
        'reflect': ('NodeSocketColor', (0.5, 0.5, 0.5)),
        'transmit': ('NodeSocketColor', (0.5, 0.5, 0.5)),
        'roughness': ('NodeSocketFloat', 0.1),
    }


@PBRTNodeTypes('material')
class PBRTShaderNodeUber(PBRTShaderNodeWithRemapRoughness):
    bl_label = 'PBRT Uber Shader'

    class_type = 'PBRTShaderNodeUber'
    shader_type = 'uber'

    socket_dict = {
        'Kd': ('NodeSocketColor', (0.25, 0.25, 0.25)),
        'Ks': ('NodeSocketColor', (0.25, 0.25, 0.25)),
        'Kr': ('NodeSocketColor', (0, 0, 0)),
        'Kt': ('NodeSocketColor', (0, 0, 0)),
        'roughness': ('NodeSocketFloat', 0.1),
        'urougnness': ('NodeSocketFloat', 0),
        'vroughness': ('NodeSocketFloat', 0),
        'eta': ('NodeSocketFloat', 1.5),
        'opacity': ('NodeSocketColor', (1, 1, 1)),
    }


# Register all the shading nodes
def register():
    registry.register()


# Unregister all the shading nodes
def unregister():
    registry.unregister()