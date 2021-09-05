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

from .mesh import get_mesh_comps


class LightIO(object):
    """

    """

    def __init__(self):
        self.area_light_geometries = []

    def write_to_file(self, writer):
        # Clear area light geometry cache before each light export
        self.area_light_geometries = []

        for object in bpy.data.objects:
            # Skip object write if hidden
            if object.hide_get():
                continue

            if object.type == 'LIGHT':
                light_type = object.data.type

                if light_type in ('POINT', 'SUN', 'SPOT'):
                    light_line_comps = ['LightSource']
                elif light_type == 'AREA':
                    light_line_comps = ['\t', 'AreaLightSource "diffuse"']
                else:
                    raise Exception('light type {} not supported'.format(light_type))

                light_color = object.data.color
                light_location = object.location
                light_location_tuple = light_location.to_tuple()
                light_props = object.data.pbrt_light_props
                area_light_pre_comps = []
                area_light_post_comps = []

                if light_type == 'POINT':
                    if light_props.isgoniometric:
                        light_line_comps.append('"goniometric" "rgb I" [{} {} {}] "string mapname" "{}"'.format(
                            light_color.r, light_color.g, light_color.b, light_props.mapname.replace("\\", "/")
                        ))
                    else:
                        light_line_comps.append('"point"')
                        light_line_comps.append('"rgb I" [{} {} {}] "point from" [{} {} {}]'.format(
                            light_color.r, light_color.g, light_color.b, *light_location_tuple
                        ))

                elif light_type == 'SUN':
                    if light_props.isprojection:
                        light_line_comps.append('"projection" "rgb I" [{} {} {}] "string mapname" "{}"').format(
                            light_color.r, light_color.g, light_color.b, light_props.mapname.replace("\\", "/")
                        )
                    else:
                        light_line_comps.append('"distant"')
                        light_rotation = object.matrix_world.to_quaternion()
                        temp_vec = mathutils.Vector((0, 0, -1))
                        temp_vec.rotate(light_rotation)
                        light_direction = light_location + temp_vec
                        light_direction_tuple = light_direction.to_tuple()
                        light_line_comps.append('"rgb L" [{} {} {}] "point from" [{} {} {}] "point to" [{} {} {}]'.format(
                            light_color.r, light_color.g, light_color.b, *light_location_tuple, *light_direction_tuple
                        ))

                elif light_type == 'SPOT':
                    light_line_comps.append('"spot"')
                    light_rotation = object.matrix_world.to_quaternion()
                    temp_vec = mathutils.Vector((0, 0, -1))
                    temp_vec.rotate(light_rotation)
                    light_direction = light_location + temp_vec
                    light_direction_tuple = light_direction.to_tuple()
                    spot_size = object.data.spot_size / math.pi * 180
                    spot_blend = object.data.spot_blend * spot_size
                    light_line_comps.append('"rgb I" [{} {} {}] "point from" [{} {} {}] "point to" [{} {} {}] "float coneangle" {} "float conedeltaangle" {}'.format(
                        light_color.r, light_color.g, light_color.b, *light_location_tuple, *light_direction_tuple,
                        spot_size, spot_blend
                    ))

                elif light_type == "AREA":
                    meshobj = light_props.geometry
                    if meshobj:
                        area_light_pre_comps.append('AttributeBegin')
                        light_line_comps.append('"rgb L" [{} {} {}]'.format(light_color.r, light_color.g, light_color.b))
                        light_line_comps.append('"bool twosided" "{}" "integer samples" {}'.format('true' if light_props.twosided else 'false', light_props.samples))
                        area_light_post_comps += get_mesh_comps(meshobj, 1)
                        area_light_post_comps.append('AttributeEnd')
                        self.area_light_geometries.append(meshobj)
                    else:
                        # Area light illegal
                        continue

                if light_type == "AREA":
                    area_light_pre_comps.append(' '.join(light_line_comps))
                    writer.write('\n'.join(area_light_pre_comps + area_light_post_comps) + '\n\n')
                else:
                    light_line_comps.append('"spectrum scale" [{} {}]'.format(light_props.scale, light_props.scale))
                    writer.write(' '.join(light_line_comps) + '\n\n')

        world_props = bpy.context.scene.pbrt_world_props
        light_line_comps = ['LightSource "infinite"']
        lum = world_props.luminance
        light_line_comps.append('"rgb L" [{} {} {}] "integer samples" {} "string mapname" "{}"'.format(
            lum.r, lum.g, lum.b, world_props.samples, world_props.mapname.replace("\\", "/")
        ))
        writer.write(' '.join(light_line_comps) + '\n\n')
