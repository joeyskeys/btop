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


class PBRTIntegratorProperties(bpy.types.PropertyGroup):
    integrator_type: bpy.props.EnumProperty(name="integrator_type",
                                            items=[
                                                ("path", "Path", ""),
                                                ("bdpt", "BDPT", ""),
                                                ("directlighting", "DirectLighting", ""),
                                                ("mlt", "MLT", ""),
                                                ("sppm", "SPPM", ""),
                                                ("whited", "Whited", ""),
                                                ("tof_path", "ToF Path", ""),
                                                ("tof_bdpt", "ToF BDPT", ""),
                                                ("tof_mlt", "ToF MLT", ""),
                                                ("tof_sppm", "ToF SPPM", ""),
                                                ("depth", "Depth", "")],
                                            default="path")

    # Path integrator parameters
    max_depth: bpy.props.IntProperty(name="max_depth",
                                     description="Maximum length of a light-carrying path sampled by the integrator",
                                     default=5,
                                     soft_max=50,
                                     min=1)

    # Pixelbound is shared with Directlighting and BDPT integrator
    pixelbound_x_min: bpy.props.IntProperty(name="pixelbound_x_min",
                                            description="x min coordination of subset image to sample",
                                            default=0,
                                            soft_max=1920,
                                            min=0)

    pixelbound_x_max: bpy.props.IntProperty(name="pixelbound_x_max",
                                            description="x max coordination of subset image to sample",
                                            default=1920,
                                            soft_max=1920,
                                            min=1)

    pixelbound_y_min: bpy.props.IntProperty(name="pixelbound_y_min",
                                            description="y min coordination of subset image to sample",
                                            default=0,
                                            soft_max=1080,
                                            min=0)

    pixelbound_y_max: bpy.props.IntProperty(name="pixelbound_x_max",
                                            description="y max coordination of subset image to sample",
                                            default=1080,
                                            soft_max=1080,
                                            min=1)

    rr_threshold: bpy.props.FloatProperty(name="rr_threshold",
                                          description="Determines when Russian roulette is applied to paths",
                                          default=1,
                                          max=1,
                                          min=0)

    light_sample_strategy: bpy.props.EnumProperty(name="light_sample_strategy",
                                                  items=[
                                                      ("spatial", "Spatial", ""),
                                                      ("uniform", "Uniform", ""),
                                                      ("power", "Power", "")],
                                                  default="spatial")

    # Direct lighting integrator parameters
    strategy: bpy.props.EnumProperty(name="The strategy to use for sampling direct lighting",
                                                         items=[
                                                             ("all", "All", ""),
                                                             ("one", "One", "")],
                                                         default="all"
                                                         )

    # BDPT integrator parameters
    visualizestrategies: bpy.props.BoolProperty(name="visualizestrategies",
                                                 description="If true, an image is saved for each (s,t) bidirectional path generation strategy used by the integrator",
                                                 default=False)

    visualizeweights:bpy.props.BoolProperty(name="visualizeweights",
                                             description="If true, an image is saved with the multiple importance sampling weights for each (s,t) bidirectional path generation strategy",
                                             default=False)

    # MTL integrator parameters
    bootstrap_samples: bpy.props.IntProperty(name="bootstrap_samples",
                                             description="Number of samples to take during the bootstrap phase",
                                             default=100000,
                                             soft_max=1000000,
                                             min=1)

    chains: bpy.props.IntProperty(name="chains",
                                  description="Number of unique Markov chains chains to follow with the Metropolis algorithm",
                                  default=1000,
                                  soft_max=100000,
                                  min=1)

    mutations_per_pixel: bpy.props.IntProperty(name="mutations_per_pixel",
                                               description="Number of path mutations to apply per pixel in the image",
                                               default=100,
                                               soft_max=10000,
                                               min=1)

    largest_step_probability: bpy.props.FloatProperty(name="largest_step_probability",
                                                      description="Probability of discarding the current path and generating a new random path",
                                                      default=0.3,
                                                      max=1,
                                                      min=0)

    sigma: bpy.props.FloatProperty(name="sigma",
                                   description="Standard deviation of the perturbation applied to random samples",
                                   default=0.01,
                                   max=1,
                                   min=0)

    # SPPM integrator parameters
    iterations: bpy.props.IntProperty(name="iterations",
                                      description="Total number of iterations of photon shooting from light sources",
                                      default=64,
                                      soft_max=128,
                                      min=1)

    photons_per_iteration: bpy.props.IntProperty(name="photons_per_iteration",
                                                 description="Number of photons to shoot from light sources in each iteration",
                                                 default=-1)

    image_write_frequency: bpy.props.IntProperty(name="image_write_frequency",
                                                 description="Frequency at which to write out the current image(power of 2)",
                                                 default=31,
                                                 soft_max=64,
                                                 min=1)

    radius: bpy.props.FloatProperty(name="radius",
                                    description="Initial photon search radius",
                                    default=1,
                                    soft_max=10,
                                    min=0)

    # ToF properties
    depthrange: bpy.props.FloatProperty(name="depthrange",
                                        description="Depth range of the scene being rendered",
                                        default=400,
                                        soft_max=1000,
                                        min=0)
    
    toftype: bpy.props.IntProperty(name="toftype",
                                    description="Time of Flight camera type",
                                    default=0,
                                    soft_max=0,
                                    min=0)


class PBRT_PT_integrator(bpy.types.Panel):
    bl_label = "Integrator"
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

        integrator_props = context.scene.pbrt_integrator_props
        integrator_type = integrator_props.integrator_type
        layout.row().prop(integrator_props, "integrator_type", text="Integrator Type")
        layout.row().prop(integrator_props, "max_depth", text="Max Depth")

        if integrator_type in ["path", "directlighting", "bdpt", "tof_path", "tof_bdpt", "depth"]:
            layout.row().prop(integrator_props, "pixelbound_x_min", text="Pixelbound X Min")
            layout.row().prop(integrator_props, "pixelbound_x_max", text="Pixelbound X Max")
            layout.row().prop(integrator_props, "pixelbound_y_min", text="Pixelbound Y Min")
            layout.row().prop(integrator_props, "pixelbound_y_max", text="Pixelbound Y Max")

        if integrator_type in ["path", "bdpt", "tof_path", "tof_bdpt"]:
            layout.row().prop(integrator_props, "light_sample_strategy", text="Light Sample Strategy")

        if integrator_type in ["path", "tof_path"]:
            layout.row().prop(integrator_props, "rr_threshold", text="RR Threshold")

        if integrator_type == "directlightingg":
            layout.row().prop(integrator_props, "strategy", text="Strategy")

        if integrator_type in ["bdpt", "tof_bdpt"]:
            layout.row().prop(integrator_props, "visualize_strategies", text="Visualize Strategies")
            layout.row().prop(integrator_props, "visualize_weights", text="Visualize Weights")

        if integrator_type in ["mlt", "tof_mlt"]:
            layout.row().prop(integrator_props, "bootstrap_samples", text="Bootstrap Samples")
            layout.row().prop(integrator_props, "chains", text="Chains")
            layout.row().prop(integrator_props, "mutations_per_pixel", text="Mutations Per Pixel")
            layout.row().prop(integrator_props, "largest_step_probability", text="Largest Step Probability")
            layout.row().prop(integrator_props, "sigma", text="Sigma")

        if integrator_type in ["sppm", "tof_sppm"]:
            layout.row().prop(integrator_props, "iterations", text="Iterations")
            layout.row().prop(integrator_props, "photons_per_iteration", text="Photons Per Iteration")
            layout.row().prop(integrator_props, "image_write_frequency", text="Image Write Frequency")
            layout.row().prop(integrator_props, "radius", text="Radius")

        if integrator_type in ["tof_path", "tof_bdpt", "tof_mlt"]:
            layout.row().prop(integrator_props, "depthrange", text="Depth range in the scene") 
            layout.row().prop(integrator_props, "toftype", text="ToF type")

def register():
    # Register property group
    bpy.utils.register_class(PBRTIntegratorProperties)
    bpy.types.Scene.pbrt_integrator_props = bpy.props.PointerProperty(type=PBRTIntegratorProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_integrator)


def unregister():
    # Unregister property group
    del bpy.types.Scene.pbrt_integrator_props
    bpy.utils.unregister_class(PBRTIntegratorProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_integrator)
