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
import bmesh

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

    # Generate new transformed vertices to consider the bone animation of the object
    # From https://odederell3d.blog/2020/09/28/blender-python-access-animated-vertices-data/
    depgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.verts.ensure_lookup_table()
    bm.from_object( meshobj, depgraph )

    hasUVs = meshobj.data.uv_layers != None and len(meshobj.data.uv_layers) > 0
    if hasUVs:
        verts, normals, uvs, faces = triangulateUV(meshobj, bm)
        mesh_comps.append(indent * '\t' + '# Num verts: {}  Num normals: {}  Num uvs: {}  Num faces: {}'.format( len(verts), len(normals), len(uvs), len(faces) ) )
    else:
        verts, faces = triangulate(meshobj, bm)
        mesh_comps.append(indent * '\t' + '# Num verts: {}  Num faces: {}'.format( len(verts), len(faces) ) )


    mesh_comps.append(indent * '\t' + 'Shape "trianglemesh"')



    if not hasUVs:
        vert_str = ''
        for vert in verts:
            vert_str += '{} {} {} '.format(*vert.to_tuple())
        mesh_comps.append((indent + 1) * '\t' + '"point P" [' + vert_str[:-1] + ' ]')

        face_str = ''
        for face in faces:
            face_str += '{} {} {} '.format(*face)
        mesh_comps.append((indent + 1) * '\t' + '"integer indices" [ ' + face_str[:-1] + ' ]')
    else:
        vert_str = ''
        for vert in verts:
            vert_str += '{} {} {} '.format(*vert)
        mesh_comps.append((indent + 1) * '\t' + '"point P" [' + vert_str[:-1] + ' ]')

        normal_str = ''
        for n in normals:
            normal_str += '{} {} {} '.format(*n)
            # n0 = n[0]
            # n1 = n[1]
            # n2 = n[2]
            # normal_str += '{} {} {} '.format(n0[0], n0[1], n0[2])
            # normal_str += '{} {} {} '.format(n1[0], n1[1], n1[2])
            # normal_str += '{} {} {} '.format(n2[0], n2[1], n2[2])
        mesh_comps.append((indent + 1) * '\t' + '"normal N" [' + normal_str[:-1] + ' ]')

        uv_str = ''
        for uv in uvs:
            uv_str += '{} {} '.format(*uv)
            # uv0 = uv[0]
            # uv1 = uv[1]
            # uv2 = uv[2]
            # uv_str += '{} {} '.format(uv0[0], uv0[1])
            # uv_str += '{} {} '.format(uv1[0], uv1[1])
            # uv_str += '{} {} '.format(uv2[0], uv2[1])
        mesh_comps.append((indent + 1) * '\t' + '"float uv" [' + uv_str[:-1] + ' ]')

        face_str = ''
        for face in faces:
            #face_str += '{} {} {} '.format(*face)
            face_str += '{} '.format(face)
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

