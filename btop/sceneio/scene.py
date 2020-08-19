# todo : license

import bpy

from .mesh import MeshIO
from .material import MaterialIO
#from .light import LightIO


class SceneIO(object):
    """

    """

    def __init__(self):
        self.meshio = MeshIO()
        self.materialio = MaterialIO()
        #self.lightio = LightIO()

    def write_to_file(self, writer):
        writer.write('WorldBegin\n\n')

        for object in bpy.data.objects:
            writer.write('AttributeBegin\n')

            if object.type == 'MESH':
                self.materialio.write_to_file(writer, object)
                self.meshio.write_to_file(writer, object)
            elif object.type == 'LIGHT':
                #self.lightio.write_to_file(writer, object)
                pass

            writer.write('AttributeEnd\n\n')

        writer.write('WorldEnd\n')

    def read_from_file(self, parser):
        pass