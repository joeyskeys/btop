# todo : license

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

    print("handling", v1, v2, v3, vert)
    print("test v1 v2", singed_area(v1, v2, vert))
    print("test v2 v3", singed_area(v2, v3, vert))
    print("test v3 v1", singed_area(v3, v1, vert))

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


def triangulate(obj):
    obj_data = obj.data
    vert_objs = obj_data.vertices
    face_objs = obj_data.polygons

    verts = []
    for vert_obj in vert_objs:
        verts.append(vert_obj.co)

    faces = []
    for face_obj in face_objs:
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
