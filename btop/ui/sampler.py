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


class PBRTSamplerProperties(bpy.types.PropertyGroup):
    sampler_type: bpy.props.EnumProperty(name="sampler_type",
                                         items=[
                                             ("o2sequence", "O2sequence", ""),
                                             ("halton", "Halton", ""),
                                             ("random", "Random", ""),
                                             ("sobol", "Sobol", ""),
                                             ("stratified", "Stratified", "")],
                                         default="halton")

    pixel_samples: bpy.props.IntProperty(name="pixel_samples",
                                         description="The number of samples to take",
                                         default=16,
                                         soft_max=128,
                                         min=1)

    jitter: bpy.props.BoolProperty(name="jitter",
                                   description="Whether or not the generated samples should be jittered inside each stratum",
                                   default=True)

    xsamples: bpy.props.IntProperty(name="xsample",
                                   description="The number of samples per pixel to take in the x direction",
                                   default=2,
                                   soft_max=128,
                                   min=1)

    ysamples: bpy.props.IntProperty(name="ysample",
                                    description="The number of samples per pixel to take in the y direction",
                                    default=2,
                                    soft_max=128,
                                    min=1)


class PBRT_PT_sampler(bpy.types.Panel):
    bl_label = "Sampler"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        sampler_props = context.scene.pbrt_sampler_props
        layout.row().prop(sampler_props, "sampler_type", text="Sampler Type")
        if sampler_props.sampler_type != "stratified":
            layout.row().prop(sampler_props, "pixel_samples", text="Pixel Samples")
        else:
            layout.row().prop(sampler_props, "jitter", text="Jitter")
            layout.row().prop(sampler_props, "xsamples", text="X Samples")
            layout.row().prop(sampler_props, "ysamples", text="Y Samples")


def register():
    # Register property group
    bpy.utils.register_class(PBRTSamplerProperties)
    bpy.types.Scene.pbrt_sampler_props = bpy.props.PointerProperty(type=PBRTSamplerProperties)

    bpy.utils.register_class(PBRT_PT_sampler)


def unregister():
    # Unregister property group
    del bpy.types.Scene.pbrt_sampler_props
    bpy.utils.unregister_class(PBRTSamplerProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_sampler)