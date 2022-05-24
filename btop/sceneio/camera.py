# This source file is part of btop
#
# This software is released under the GPL-3.0 license.
#
# Copyright (c) 2020 Joey Chen. All rights reserved.
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import bpy
import mathutils

import math


class CameraIO(object):
    """

    """

    def __init__(self):
        self.camera_type = 'perspective'
        self.shutter_open = None
        self.shutter_close = None
        self.extra_params = {}

    def write_to_file(self, writer):
        active_camera = bpy.context.scene.camera

        # Add scale to convert right hand system to left hand system
        scale_line = 'Scale -1 1 1'

        # Get camera position and orientation
        camera_matrix = active_camera.matrix_world
        eye_pos = camera_matrix.translation
        look_vec = mathutils.Vector((0, 0, -1))
        look_vec.rotate(camera_matrix.to_3x3())
        look_at = eye_pos + look_vec * 3
        up_vec = mathutils.Vector((0, 1, 0))
        up_vec.rotate(camera_matrix.to_3x3())
        orient_line = 'LookAt {} {} {} {} {} {} {} {} {}'.format(*eye_pos.to_tuple(),
                                                                   *look_at.to_tuple(),
                                                                   *up_vec.to_tuple())

        # Get camera properties
        camera_props = active_camera.data.pbrt_camera_props
        camera_line_comps = ['Camera "{}" "float shutteropen" {} "float shutterclose" {}'.format(camera_props.camera_type,
                                                                                       camera_props.shutter_open,
                                                                                       camera_props.shutter_close)]

        if camera_props.camera_type != "realistic":
            camera_line_comps.append('"float frameratio" {}'.format(camera_props.frame_ratio))
            #camera_line_comps.append('"float screenwindow" [{} {} {} {}]'.format(camera_props.screen_window_x_min,
            #                                                                     camera_props.screen_window_x_max,
            #                                                                     camera_props.screen_window_y_min,
            #                                                                     camera_props.screen_window_y_max))

            if camera_props.camera_type != "environment":
                camera_line_comps.append('"float lensradius" {}'.format(camera_props.lens_radius))
                camera_line_comps.append('"float focaldistance" {}'.format(camera_props.focal_distance))

            if camera_props.camera_type == "perspective":
                # Get fov from camera attributes
                angle = bpy.context.scene.camera.data.angle
                ratio = bpy.context.scene.render.resolution_y / bpy.context.scene.render.resolution_x
                fov = 2 * math.degrees(math.atan(ratio * math.tan(angle / 2)))
                camera_line_comps.append('"float fov" {}'.format(fov))

        else:
            camera_line_comps.append('"string lensfile" "{}"'.format(camera_props.lens_file))
            camera_line_comps.append('"float aperturediameter" {}'.format(camera_props.aperture_diameter))
            camera_line_comps.append('"float focusdistance" {}'.format(camera_props.focus_distance))
            camera_line_comps.append('"bool simpleweighting" "{}"'.format(camera_props.simple_weighting))

        # Write out
        writer.write(scale_line + '\n')
        writer.write(orient_line + '\n')
        writer.write(' '.join(camera_line_comps) + '\n\n')

    def read_from_file(self, parser):
        pass

