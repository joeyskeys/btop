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

import math

from ..misc import triangulate


class MeshIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer, meshobj, indent=0):

        def write_with_indent(idnt, content):
            writer.write('\t' * idnt + content)

        # Get translation and scale
        matrix = meshobj.matrix_world
        translation = matrix.translation.to_tuple()
        scale = matrix.to_scale().to_tuple()

        # Get rotation
        rot = matrix.to_quaternion()
        if rot[0] == 0:
            rotate_angle = math.pi
            x_fac = rot[1]
            y_fac = rot[2]
            z_fac = rot[3]
        elif rot[0] == 1:
            rotate_angle = 0
            x_fac = 0
            y_fac = 0
            z_fac = 1
        else:
            rotate_angle = 2 * math.acos(rot[0])
            denom = math.sqrt(1 - rot[0] * rot[0])
            x_fac = rot[1] / denom
            y_fac = rot[2] / denom
            z_fac = rot[3] / denom
        rotate_vec = (x_fac, y_fac, z_fac)

        # Write out transformation
        write_with_indent(indent, 'Translate {} {} {}\n'.format(*translation))
        write_with_indent(indent, 'Scale {} {} {}\n'.format(*scale))
        write_with_indent(indent, 'Rotate {} {} {} {}\n'.format(rotate_angle, *rotate_vec))

        # Triangulate the mesh
        verts, faces = triangulate(meshobj)

        write_with_indent(indent, 'Shape "trianglemesh"\n')

        vert_str = ''
        for vert in verts:
            vert_str += '{} {} {} '.format(*vert.to_tuple())
            #vert_str += '{} {} {} '.format(vert.x, vert.y, -vert.z)
        write_with_indent(indent + 1, ('"point P" [ ' + vert_str[:-1] + ' ]\n'))

        face_str = ''
        for face in faces:
            face_str += '{} {} {} '.format(*face)
        write_with_indent(indent + 1, ('"integer indices" [ ' + face_str[:-1] + ' ]\n'))

    def read_from_file(self, parser):
        pass

