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


class FilmIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):

        film_props = bpy.context.scene.pbrt_film_props

        # Currently image is the only film type
        # Hard coded here
        film_line_comps = ['Film "image"']

        film_line_comps.append('"integer xresolution" {}'.format(film_props.x_resolution))
        film_line_comps.append('"integer yresolution" {}'.format(film_props.y_resolution))

        crop_win_x_min = film_props.crop_window_x_min
        crop_win_x_max = film_props.crop_window_x_max
        crop_win_y_min = film_props.crop_window_y_min
        crop_win_y_max = film_props.crop_window_y_max
        film_line_comps.append('"float cropwindow" [{} {} {} {}]'.format(crop_win_x_min,
                                                                         crop_win_x_max,
                                                                         crop_win_y_min,
                                                                         crop_win_y_max))

        film_line_comps.append('"float scale" {}'.format(film_props.scale))
        film_line_comps.append('"float maxsampleluminance" {}'.format(film_props.max_sample_luminance))
        film_line_comps.append('"float diagonal" {}'.format(film_props.diagonal))
        #film_line_comps.append('"string filename" "{}"'.format(film_props.filename))

        writer.write(' '.join(film_line_comps) + '\n\n')

    def read_from_file(self, parser):
        pass