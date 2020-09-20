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


class SamplerIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):
        # Get sampler properties
        sampler_props = bpy.context.scene.pbrt_sampler_props
        sampler_line_comps = ['Sampler "{}"'.format(sampler_props.sampler_type)]

        if sampler_props.sampler_type != "stratified":
            sampler_line_comps.append('"integer pixelsamples" {}'.format(sampler_props.pixel_samples))
        else:
            sampler_line_comps.append('"bool jitter" "{}"'.format(sampler_props.jitter))
            sampler_line_comps.append('"integer xsamples" {}'.format(sampler_props.xsamples))
            sampler_line_comps.append('"integer ysamples" {}'.format(sampler_props.ysamples))

        # Write out
        writer.write(' '.join(sampler_line_comps) + '\n\n')

    def read_from_file(self, parser):
        pass
