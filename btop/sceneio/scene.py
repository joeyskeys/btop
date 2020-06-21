# todo : license

import bpy

from .mesh import MeshIO
#from .material import MaterialIO
#from .light import LightIO


class SceneIO(object):
    """

    """

    def __init__(self):
        self.meshio = MeshIO()
        #self.materialio = MaterialIO()
        #self.lightio = LightIO()

    def write_to_file(self, writer):
        writer.write('WorldBegin')

        for object in bpy.data.objects:
            writer.write('AttributeBegin')

            if object.type == 'MESH':
                # todo : export texture and material first
                self.meshio.write_to_file(writer, object)
            elif object.type == 'LIGHT':
                self.lightio.write_to_file(writer, object)

            writer.write('AttributeEnd')

        writer.write('WorldEnd')

    def read_from_file(self, parser):
        pass