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


class PBRTWorldProperties(bpy.types.PropertyGroup):
    luminance: bpy.props.FloatVectorProperty(name="luminance",
                                             description="A radiance scale factor for the light",
                                             default=(0.4, 0.4, 0.4),
                                             subtype='COLOR')

    samples: bpy.props.IntProperty(name="samples",
                                   description="Suggested number of shadow samples to take when computing illumination \
                                        from the light",
                                   default=1,
                                   min=1)

    mapname: bpy.props.StringProperty(name="mapname",
                                      description="The environment map to use for the infinite area light",
                                      subtype="FILE_PATH")


class PBRT_PT_world(bpy.types.Panel):
    bl_label = "World"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "world"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True

        world_props = context.scene.pbrt_world_props

        layout.row().prop(world_props, "luminance", text="Luminance")
        layout.row().prop(world_props, "samples", text="Samples")
        layout.row().prop(world_props, "mapname", text="MapName")


def register():
    # Register property group
    bpy.utils.register_class(PBRTWorldProperties)
    bpy.types.Scene.pbrt_world_props = bpy.props.PointerProperty(type=PBRTWorldProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_world)


def unregister():
    # Unregister property group
    del bpy.types.Scene.pbrt_world_props
    bpy.utils.unregister_class(PBRTWorldProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_world)
