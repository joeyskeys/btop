# todo : license

import bpy

from .camera import CameraIO
from .film import FilmIO
from .sampler import SamplerIO
from .integrator import IntegratorIO


class PBRTExporter(object):
    """
    Export blender scene into a pbrt scene file
    """

    def __init__(self):
        self.cameraio = CameraIO()
        self.samplerio = SamplerIO()
        self.integratorio = IntegratorIO()
        self.filmio = FilmIO()
        #self.sceneio = SceneIO()

    def export(self, output_path):
        file_handler = open(output_path, 'w')

        self.cameraio.write_to_file(file_handler)

        self.samplerio.write_to_file(file_handler)
        self.integratorio.write_to_file(file_handler)
        self.filmio.write_to_file(file_handler)

        #self.sceneio.write_to_file(file_handler)