# todo : license

import bpy

from .mesh import MeshIO
from .material import MaterialIO
from .light import LightIO


class SceneIO(object):
    """

    """

    def __init__(self):
        self.meshio = MeshIO()
        self.materialio = MaterialIO()
        self.lightio = LightIO()

    def write_to_file(self, writer):
        writer.write('WorldBegin\n\n')

        # Light should be written in the world block
        self.lightio.write_to_file(writer)

        for object in bpy.data.objects:

            if object.type == 'MESH':
                writer.write('AttributeBegin\n')
                self.materialio.write_to_file(writer, object)
                self.meshio.write_to_file(writer, object)
                writer.write('AttributeEnd\n\n')

        writer.write('WorldEnd\n')

    def read_from_file(self, parser):
        pass