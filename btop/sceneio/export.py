# todo : license

import bpy

from .camera import CameraIO


class PBRTExporter(object):
    """
    Export blender scene into a pbrt scene file
    """

    def __init__(self):
        self.cameraio = CameraIO()
        #self.filmio = FilmIO()
        #self.samplerio = SamplerIO()
        #self.integratorio = IntegratorIO()
        #self.sceneio = SceneIO()

    def export(self, output_path):
        file_handler = open(output_path, 'w')

        self.cameraio.write_to_file(file_handler)
        #self.filmio.write_to_file(file_handler)
        #self.samplerio.write_to_file(file_handler)
        #self.sceneio.write_to_file(file_handler)