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

from collections import deque


def get_normal(verts):
    n = mathutils.Vector((0, 0, 0))
    for i in range(len(verts)):
        vert_curr = verts[i - 1]
        vert_next = verts[i]
        #n += (vert_curr - vert_next) * (vert_curr + vert_next)
        vec_a = vert_curr - vert_next
        vec_b = vert_curr + vert_next
        n += mathutils.Vector((vec_a.x * vec_b.x, vec_a.y * vec_b.y, vec_a.z * vec_b.z))

    n.normalize()
    return n


def get_local_frame(normal):
    #normal.normalize()
    const_front = mathutils.Vector((0, 1, 0))
    right_vec = const_front.cross(normal)

    if right_vec.length < 0.0000001:
        right_vec = mathutils.Vector((1, 0, 0))
        front_vec = mathutils.Vector((0, 0, -1))
    else:
        front_vec = normal.cross(right_vec)

    return mathutils.Matrix((right_vec, front_vec, normal))


def is_convex(vert_prev, vert_curr, vert_next):
    vec_a = mathutils.Vector((*((vert_curr - vert_prev).to_tuple()), 0))
    vec_b = mathutils.Vector((*((vert_next - vert_curr).to_tuple()), 0))

    if vec_a.cross(vec_b).z > -1:
        return True
    else:
        return False


def is_in_triangle(v1, v2, v3, vert):
    def singed_area(v1, v2, v3):
        return v1.x * (v2.y - v3.y) + v2.y * (v3.y - v1.y) + v3.y * (v1.y - v2.y) > 0

    # print("handling", v1, v2, v3, vert)
    # print("test v1 v2", singed_area(v1, v2, vert))
    # print("test v2 v3", singed_area(v2, v3, vert))
    # print("test v3 v1", singed_area(v3, v1, vert))

    return singed_area(v1, v2, vert) and singed_area(v2, v3, vert) and singed_area(v3, v1, vert)


def triangulate_a_quat(verts, vert_indices):
    diagonal_a = (verts[0] - verts[2]).length
    diagonal_b = (verts[1] - verts[3]).length

    if diagonal_a < diagonal_b:
        return [(vert_indices[0], vert_indices[1], vert_indices[2]),
                (vert_indices[0], vert_indices[2], vert_indices[3])]
    else:
        return [(vert_indices[0], vert_indices[1], vert_indices[3]),
                (vert_indices[3], vert_indices[1], vert_indices[2])]

def triangulate_a_quat_UV(verts, normals, uvs, new_polyvert_idx):
    diagonal_a = (verts[0] - verts[2]).length
    diagonal_b = (verts[1] - verts[3]).length

    if diagonal_a < diagonal_b:
        new_verts = [verts[0], verts[1], verts[2], 
                    verts[0], verts[2], verts[3]]
        new_normals = [normals[0], normals[1], normals[2],
                    normals[0], normals[2], normals[3]]
        new_uvs = [uvs[0], uvs[1], uvs[2],
                    uvs[0], uvs[2], uvs[3]]
        tri_vert_indx = [new_polyvert_idx+0, new_polyvert_idx+1, new_polyvert_idx+2,
                        new_polyvert_idx+3, new_polyvert_idx+4, new_polyvert_idx+5]
    else:
        new_verts = [verts[0], verts[1], verts[3],
                    verts[3], verts[1], verts[2]]
        new_normals = [normals[0], normals[1], normals[3],
                    normals[3], normals[1], normals[2]]
        new_uvs = [uvs[0], uvs[1], uvs[3], 
                    uvs[3], uvs[1], uvs[2]]
        tri_vert_indx = [new_polyvert_idx+0, new_polyvert_idx+1, new_polyvert_idx+2,
                        new_polyvert_idx+3, new_polyvert_idx+4, new_polyvert_idx+5]
        
    return new_verts, new_normals, new_uvs, tri_vert_indx

def triangulate_a_ngon(verts, vert_indices):
    normal = get_normal(verts)
    frame = get_local_frame(normal)

    projected_verts = []
    convex_flags = []
    for vert in verts:
        projected = frame @ vert
        projected_verts.append(projected.xy)

    for i in range(len(projected_verts)):
        vert_curr = projected_verts[i]
        vert_prev = projected_verts[i - 1]
        vert_next = projected_verts[(i + 1) % len(projected_verts)]
        convex_flags.append(is_convex(vert_prev, vert_curr, vert_next))

    verts_queue = deque()
    for i in range(len(verts)):
        verts_queue.append((verts[i], vert_indices[i], i))

    new_triangles = []

    #counter = 0
    #while len(verts_queue) > 3 and counter < 15:

    while len(verts_queue) > 3:

        #counter += 1

        vert, vert_index, i = verts_queue.popleft()

        if convex_flags[i]:
            is_ear = True
            for i in range(1, len(verts_queue) - 1):
                if is_in_triangle(verts_queue[-1][0], vert, verts_queue[0][0], verts_queue[i][0]):
                    is_ear = False
                    break

            if is_ear:
                new_triangles.append((verts_queue[-1][2], i, verts_queue[0][2]))

                idx_a = verts_queue[-1][2]
                convex_flags[idx_a] = is_convex(projected_verts[verts_queue[-2][2]],
                                                projected_verts[verts_queue[-1][2]],
                                                projected_verts[verts_queue[0][2]])
                idx_b = verts_queue[0][2]
                convex_flags[idx_b] = is_convex(projected_verts[verts_queue[-1][2]],
                                                projected_verts[verts_queue[0][2]],
                                                projected_verts[verts_queue[1][2]])

            else:
                verts_queue.append((vert, vert_index, i))

        else:
            verts_queue.append((vert, vert_index, i))

    new_triangles.append((verts_queue[0][2], verts_queue[1][2], verts_queue[2][2]))

    return new_triangles

#
# 2021-05-21 James Tompkin
#
# pbrt only supports one set of uv coordinates per vertex.
# It does not support vertices with multiple uv coordinates
# Or, put another way, uv coordinates per polygon.
# 
# This restricts UV maps with cuts in the unwrapping.
# As such, we will duplicate vertices and give them unique
# UVs for each triangle, and then duplicate the polygon indices.
#
# This is inefficient, but works.
#
# Inputs:
# - obj: The object to draw
# - animated_mesh: The current animated state of the vertices.
#                  In Blender, to my knowledge, we can't access 
#                  the animated vert positions from obj, so instead
#                  we pass them in. Not ideal.
# 
def triangulateUV(obj, animated_mesh):
    obj_data = obj.data
    # Alternative way of accessing vertices that does not 
    # include animated positions.
    #vert_objs = obj_data.vertices
    # Access of vertices affected by animation
    vert_objs = animated_mesh.verts
    uv_objs = obj_data.uv_layers[0].data
    polygon_objs = obj_data.polygons

    ################
    # Collect all vert coordinates and uv coordinates into lists
    # to make them easier to index into
    # Also collect per-vertex normals
    ################
    verts = []
    normals = []
    for vert_obj in vert_objs:
        verts.append(vert_obj.co)
        normals.append(vert_obj.normal)

    uvs = []
    for uvx in uv_objs:
        uvs.append(uvx.uv)

    # Return structures
    all_new_vertices = []
    all_new_normals = []
    all_new_uvs = []
    all_new_triangles = []

    # Counters for the relabeling of the polygon indices
    c_antris = 0

    for polygon_obj in polygon_objs:
        ################
        # Collect all vert coordinates and uv coordinates
        # arranged by their polygon
        ################
        # Cycle through all vertex indices and add the vertex xyz to the list
        poly_verts = []
        poly_vertnormals = []
        for idx in polygon_obj.vertices:
            poly_verts.append(verts[idx])
            poly_vertnormals.append(normals[idx])

        # Cycle through all vertex indices and add the uv coordinate
        # that matches the vertex to the list
        poly_uvs = []
        for idx in polygon_obj.loop_indices:
            poly_uvs.append(uvs[idx])

        nVertsInPoly = len(polygon_obj.vertices)
        if nVertsInPoly > 4:
            # TODO: Add support for ngons
            print( "[btop.misc.triangulate.py: triangulateUV] ngons not yet implemented; only quads and tris." )
        
        elif nVertsInPoly == 4: # (a quad)
            # Split the quad into to tris
            new_verts, new_normals, new_uvs, new_triangles = triangulate_a_quat_UV(poly_verts, poly_vertnormals, poly_uvs, c_antris)
            all_new_vertices += new_verts
            all_new_normals += new_normals
            all_new_uvs += new_uvs
            all_new_triangles += new_triangles
            c_antris = c_antris + 6 # Increment polygon vertex index counter by two triangles

        else: 
            # nVertsInPoly == 3 (a triangle)
            # No need to split; just add the coordinates
            all_new_vertices += poly_verts
            all_new_normals += poly_vertnormals
            all_new_uvs += poly_uvs
            all_new_triangles += [c_antris+0, c_antris+1, c_antris+2]
            c_antris = c_antris + 3 # Increment polygon vertex index counter by one triangle

    # TODO
    # We add tuples to lists and then append them to a big list, 
    # then in mesh.py we decompose everything again. Not efficient.
    
    return all_new_vertices, all_new_normals, all_new_uvs, all_new_triangles

# Triangulate function that does not support UVs
#
# Inputs:
# - obj: The object to draw
# - animated_mesh: The current animated state of the vertices.
#                  In Blender, to my knowledge, we can't access 
#                  the animated vert positions from obj, so instead
#                  we pass them in. Not ideal.
# 
def triangulate(obj, animated_mesh):
    obj_data = obj.data
    # Alternative way of accessing vertices that does not 
    # include animated positions.
    #vert_objs = obj_data.vertices
    # Access of vertices affected by animation
    vert_objs = animated_mesh.verts
    face_objs = obj_data.polygons

    verts = []
    for vert_obj in vert_objs:
        verts.append(vert_obj.co)

    faces = []
    for face_obj in face_objs:
        # face_obj.vertices stores the vertex _indices_
        # of the polygon
        faces.append(face_obj.vertices)

    new_triangles = []
    for face in faces:
        if len(face) > 3:

            face_verts = []
            for idx in face:
                face_verts.append(verts[idx])

            if len(face) == 4:
                new_triangles += triangulate_a_quat(face_verts, face)
            else:
                new_triangles += triangulate_a_ngon(face_verts, face)

    return verts, new_triangles
