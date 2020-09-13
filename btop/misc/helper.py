# todo : license

import bpy


class Registry(object):
    def __init__(self):
        self.cls_to_register = []
        self.material_nodes = []
        self.texture_nodes = []

    def add_new_class(self, cls, node_type=None):
        self.cls_to_register.append(cls)

        # We need the class type bacause cls.__class__.__name__ is not the correct value
        if node_type == 'material':
            self.material_nodes.append((cls.class_type, cls.shader_type))
            cls.category = 'Material'

        elif node_type == 'texture':
            self.texture_nodes.append((cls.class_type, cls.shader_type))
            cls.category = 'Texture'

        else:
            cls.category = 'Default'

    def register(self):
        for c in self.cls_to_register:
            print('register', c)
            bpy.utils.register_class(c)

    def unregister(self):
        for c in self.cls_to_register:
            bpy.utils.unregister_class(c)


registry = Registry()


class PBRTNodeTypes(object):
    def __init__(self, node_type=None):
        self.node_type = node_type
        self.material_nodes = []
        self.texture_nodes = []

    def __call__(self, cls):
        registry.add_new_class(cls, self.node_type)
        return cls
