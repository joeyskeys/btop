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


class IntegratorIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):
        integrator_props = bpy.context.scene.pbrt_integrator_props
        integrator_type = integrator_props.integrator_type
        integrator_line_comps = ['Integrator "{}"'.format(integrator_type)]
        integrator_line_comps.append('"integer maxdepth" {}'.format(integrator_props.max_depth))

        if integrator_type in ["path", "directlighting", "bdpt"]:
            p_x_min = integrator_props.pixelbound_x_min
            p_x_max = integrator_props.pixelbound_x_max
            p_y_min = integrator_props.pixelbound_y_min
            p_y_max = integrator_props.pixelbound_y_max

            film_props = bpy.context.scene.pbrt_film_props
            render = bpy.context.scene.render
            film_x_resolution = render.resolution_x
            film_y_resolution = render.resolution_y

            integrator_line_comps.append('"integer pixelbounds" [{} {} {} {}]'.format(p_x_min,
                                                                                      min(p_x_max, film_x_resolution),
                                                                                      p_y_min,
                                                                                      min(p_y_max, film_y_resolution)))

        if integrator_type in ["path", "bdpt"]:
            integrator_line_comps.append('"string lightsamplestrategy" "{}"'.format(integrator_props.light_sample_strategy))

        if integrator_type == "path":
            integrator_line_comps.append('"float rrthreshold" {}'.format(integrator_props.rr_threshold))

        if integrator_type == "directlighting":
            integrator_line_comps.append('"string strategy" "{}"'.format(integrator_props.strategy))

        if integrator_type == "bdpt":
            integrator_line_comps.append('"bool visualizestrategies" {}'.format(integrator_props.visualizestrategies))
            integrator_line_comps.append('"bool visualizeweights" {}'.format(integrator_props.visualizeweights))

        if integrator_type == "mlt":
            integrator_line_comps.append('"integer bootstrapsamples" {}'.format(integrator_props.bootstrap_samples))
            integrator_line_comps.append('"integer chains" {}'.format(integrator_props.chains))
            integrator_line_comps.append('"integer mutationsperpixel" {}'.format(integrator_props.mutations_per_pixel))
            integrator_line_comps.append('"float largestepprobability" {}'.format(integrator_props.largest_step_probability))
            integrator_line_comps.append('"float sigma" {}'.format(integrator_props.sigma))

        if integrator_type == "sppm":
            integrator_line_comps.append('"integer iterations" {}'.format(integrator_props.iterations))
            integrator_line_comps.append('"integer photonsperiteration" {}'.format(integrator_props.photons_per_iteration))
            integrator_line_comps.append('"integer imagewritefrequency" {}'.format(integrator_props.image_write_frequency))
            integrator_line_comps.append('"float radius" {}'.format(integrator_props.radius))

        writer.write(' '.join(integrator_line_comps) + '\n\n')

    def read_from_file(self, parser):
        pass