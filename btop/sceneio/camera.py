

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
        camera_props = active_camera.data.pbrt_camera_props
        orient_line_comps = []
        camera_line_comps = ['Camera {} float shutteropen {} shutterclose {}'.format(camera_props.camera_type,
                                                                                     camera_props.shutter_open,
                                                                                     camera_props.shutter_close)]

        if camera_props.camera_type != "realistic":
            camera_line_comps.append('"float frameratio" {}'.format(camera_props.frame_ratio))
            camera_line_comps.append('"float screenwindow" {}'.format(camera_props.screen_window))

            if camera_props.camera_type != "environment":
                camera_line_comps.append('"float lensradius" {}'.format(camera_props.lens_radius))
                camera_line_comps.append('"float focaldistance" {}'.format(camera_props.focal_distance))

            if camera_props.camera_type == "perspective":
                camera_line_comps.append('"float fov" {}'.format(camera_props.fov))

        else:
            camera_line_comps.append('"string lensfile" "{}"'.format(camera_props.lens_file))
            camera_line_comps.append('"float aperturediameter" {}'.format(camera_props.aperture_diameter))
            camera_line_comps.append('"float focusdistance" {}'.format(camera_props.focus_distance))
            camera_line_comps.append('"bool simpleweighting" "{}"'.format(camera_props.simple_weighting))

        # todo : write camera lookat
        writer.write(' '.join(camera_line_comps))

    def read_from_file(self, parser):
        pass

    def create_in_bl(self, scene):
        pass