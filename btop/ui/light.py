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


class PBRTLightProperties(bpy.types.PropertyGroup):
    scale: bpy.props.FloatProperty(name="scale",
                                   description="Scale factor that modulates the amount of light that the light source emits into the scene",
                                   default=1,
                                   min=0)

    # Area light props
    twosided: bpy.props.BoolProperty(name="twosided",
                                     description="Determines whether the light source emits light from just the side of the surface where the surface normal points or both sides",
                                     default=False)

    samples: bpy.props.IntProperty(name="samples",
                                   description="Suggested number of shadow samples to take when computing illumination from the light",
                                   default=1,
                                   min=1)

    def object_poll(self, object):
        return object.type == 'MESH'

    geometry: bpy.props.PointerProperty(name="geometry",
                                        type=bpy.types.Object,
                                        description="The geometry used to specify the shape of area light",
                                        poll=object_poll)

    # Goniometric light props
    isgoniometric: bpy.props.BoolProperty(name="isgoniometric",
                                          description="A bool property to determine whether a point light is a goniometric one",
                                          default=False)

    mapname: bpy.props.StringProperty(name="mapname",
                                      description="The filename of the image file that stores a goniometric diagram to use for the lighting distribution",
                                      default="",
                                      subtype="FILE_PATH")

    # Porjection light props
    isprojection: bpy.props.BoolProperty(name="isprojection",
                                         description="A bool property to determine wheter a distant light is a projection one",
                                         default=False)

    fov: bpy.props.FloatProperty(name="fov",
                                 description="The spread angle of the projected light, along the shorter image axis",
                                 default=45,
                                 min=1,
                                 max=90)


class PBRT_PT_light(bpy.types.Panel):
    bl_label = "Light"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER' and context.active_object.type == 'LIGHT'

    def draw(self, context):
        layout = self.layout
        light = context.active_object.data

        layout.use_property_split = True

        layout.prop(light, "type", expand=True)
        layout.prop(light, "color")

        light_props = light.pbrt_light_props

        if light.type != "AREA":
            layout.row().prop(light_props, "scale")

        if light.type == "SPOT":
            layout.row().prop(light, "spot_size")
            layout.row().prop(light, "spot_blend")
        elif light.type == "AREA":
            layout.row().prop(light_props, "twosided")
            layout.row().prop(light_props, "samples")
            layout.row().prop(light_props, "geometry")
        elif light.type == "POINT":
            layout.row().prop(light_props, "isgoniometric")
            if light_props.isgoniometric:
                layout.row().prop(light_props, "mapname")
        elif light.type == "SUN":
            layout.row().prop(light_props, "isprojection")
            if light_props.isprojection:
                layout.row().prop(light_props, "fov")
                layout.row().prop(light_props, "mapname")


def register():
    # Register property group
    bpy.utils.register_class(PBRTLightProperties)
    bpy.types.Light.pbrt_light_props = bpy.props.PointerProperty(type=PBRTLightProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_light)


def unregister():
    # Unregister property group
    del bpy.types.Light.pbrt_light_props
    bpy.utils.unregister_class(PBRTLightProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_light)