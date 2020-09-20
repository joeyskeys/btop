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


class LightIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):
        for object in bpy.data.objects:
            if object.type == 'LIGHT':
                light_type = object.data.type
                light_line_comps = ['LightSource']
                light_color = object.data.color
                light_location = object.location
                light_location_tuple = light_location.to_tuple()

                if light_type == 'POINT':
                    light_line_comps.append('"point"')
                    light_line_comps.append('"rgb I" [{} {} {}] "point from" [{} {} {}]'.format(
                        light_color.r, light_color.g, light_color.b, *light_location_tuple
                    ))

                elif light_type == 'SUN':
                    light_line_comps.append('"distant"')
                    light_rotation = object.matrix_world.to_quaternion()
                    light_direction = light_location + mathutils.Vector((0, 0, -1)).rotate(light_rotation)
                    light_direction_tuple = light_direction.to_tuple()
                    light_line_comps.append('"rgb L" [{} {} {}] "point from" [{} {} {}] "point to" [{} {} {}]'.format(
                        light_color.r, light_color.g, light_color.b, *light_location_tuple, *light_direction_tuple
                    ))

                elif light_type == 'SPOT':
                    light_rotation = object.matrix_world.to_quaternion()
                    light_direction = light_location + mathutils.Vector((0, 0, -1)).rotate(light_rotation)
                    light_direction_tuple = light_direction.to_tuple()
                    spot_size = object.data.spot_size / math.pi * 180
                    spot_blend = object.data.spot_blend * spot_size
                    light_line_comps.append('"rgb I" [{} {} {}] "point from" [{} {} {}] "point to" [{} {} {}] \
                                             "float coneangle" {} "float conedeltaangle" {}'.format(
                        light_color.r, light_color.g, light_color.b, *light_location_tuple, *light_direction_tuple,
                        spot_size, spot_blend
                    ))

                else:
                    raise Exception('light type {} not supported'.format(light_type))

                writer.write(' '.join(light_line_comps) + '\n\n')

        world_props = bpy.context.scene.pbrt_world_props
        light_line_comps = ['LightSource "infinite"']
        lum = world_props.luminance
        light_line_comps.append('"rgb L" [{} {} {}] "integer samples" {} "string mapname" "{}"'.format(
            lum.r, lum.g, lum.b, world_props.samples, world_props.mapname
        ))
        writer.write(' '.join(light_line_comps) + '\n\n')
