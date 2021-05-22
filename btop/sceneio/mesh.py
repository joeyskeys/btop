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
from ..misc import triangulateUV


# This part of code will be used by area light mesh export, make it a function
def get_mesh_comps(meshobj, indent=0):
    mesh_comps = []

    # Get translation and scale
    matrix = meshobj.matrix_world
    translation = matrix.translation.to_tuple()
    scale = matrix.to_scale().to_tuple()

    # Get rotation
    rot = matrix.to_quaternion()
    if rot.w == 0:
        rotate_angle = math.pi
        x_fac = rot.x
        y_fac = rot.y
        z_fac = rot.z
    elif rot.w == 1:
        rotate_angle = 0
        x_fac = 0
        y_fac = 0
        z_fac = 1
    else:
        rotate_angle = math.degrees(2 * math.acos(rot.w))
        denom = math.sqrt(1 - rot.w * rot.w)
        x_fac = rot.x / denom
        y_fac = rot.y / denom
        z_fac = rot.z / denom
    rotate_vec = (x_fac, y_fac, z_fac)

    # Write out transformation
    mesh_comps.append(indent * '\t' + 'Translate {} {} {}'.format(*translation))
    mesh_comps.append(indent * '\t' + 'Scale {} {} {}'.format(*scale))
    mesh_comps.append(indent * '\t' + 'Rotate {} {} {} {}'.format(rotate_angle, *rotate_vec))

    # Triangulate the mesh
    # 2021-05-20 TODO Output the UV coordinates

    if meshobj.data.uv_layers != None:
        verts, uvs, faces = triangulateUV(meshobj)
        mesh_comps.append(indent * '\t' + '# Num verts: {}  Num uvs: {}  Num faces: {}'.format( len(verts), len(uvs), len(faces) ) )
    else:
        verts, faces = triangulate(meshobj)
        mesh_comps.append(indent * '\t' + '# Num verts: {}  Num faces: {}'.format( len(verts), len(faces) ) )


    mesh_comps.append(indent * '\t' + 'Shape "trianglemesh"')

    vert_str = ''
    for vert in verts:
        vert0 = vert[0]
        vert1 = vert[1]
        vert2 = vert[2]
        vert_str += '{} {} {} '.format(vert0[0], vert0[1], vert0[2])
        vert_str += '{} {} {} '.format(vert1[0], vert1[1], vert1[2])
        vert_str += '{} {} {} '.format(vert2[0], vert2[1], vert2[2])
    mesh_comps.append((indent + 1) * '\t' + '"point P" [' + vert_str[:-1] + ' ]')

    if meshobj.data.uv_layers != None:
        uv_str = ''
        for uv in uvs:
            uv0 = uv[0]
            uv1 = uv[1]
            uv2 = uv[2]
            uv_str += '{} {} '.format(uv0[0], uv0[1])
            uv_str += '{} {} '.format(uv1[0], uv1[1])
            uv_str += '{} {} '.format(uv2[0], uv2[1])
        mesh_comps.append((indent + 1) * '\t' + '"float uv" [' + uv_str[:-1] + ' ]')

    face_str = ''
    for face in faces:
        face_str += '{} {} {} '.format(*face)
    mesh_comps.append((indent + 1) * '\t' + '"integer indices" [ ' + face_str[:-1] + ' ]')

    return mesh_comps


class MeshIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer, meshobj, indent=0):
        mesh_comps = get_mesh_comps(meshobj, indent)
        writer.write('\n'.join(mesh_comps) + '\n\n')

    def read_from_file(self, parser):
        pass

