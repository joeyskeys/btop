

import bpy


class CameraIO(object):
    """

    """

    def __init__(self):
        self.camera_type = 'perspective'
        self.shutter_open = None
        self.shutter_close = None
        self.extra_params = {}

    def read_from_bl(self, scene):
        pass

    def write_to_file(self, writer):
        active_camera = bpy.context.scene.camera

    def read_from_file(self, parser):
        pass

    def create_in_bl(self, scene):
        pass