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

    # Spot light props
    coneangle: bpy.props.FloatProperty(name="coneangle",
                                       description="The angle that the spotlight's cone makes with its primary axis",
                                       default=30,
                                       min=0,
                                       max=180)

    conedeltaangle: bpy.props.FloatProperty(name="conedeltaangle",
                                            description="The angle at which the spotlight intensity begins to fall off at the edges",
                                            default=5,
                                            min=0,
                                            max=90)

    # Area light props
    twosided: bpy.props.BoolProperty(name="twosided",
                                     description="Determines whether the light source emits light from just the side of the surface where the surface normal points or both sides",
                                     default=False)

    samples: bpy.props.IntProperty(name="samples",
                                   description="Suggested number of shadow samples to take when computing illumination from the light",
                                   default=1,
                                   min=1)


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

        col = layout.column()
        row = layout.row()

        light_props = light.pbrt_light_props

        row.prop(light_props, "scale")

        if light.type == "SPOT":
            row.prop(light_props, "coneangle")
            row.prop(light_props, "conedeltaangle")
        elif light.type == "AREA":
            row.prop(light_props, "twosided")
            row.prop(light_props, "samples")


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