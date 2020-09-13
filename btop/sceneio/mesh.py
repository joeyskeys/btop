

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

        # Get mesh data
        #mesh = meshobj.data
        #verts = mesh.vertices
        #faces = mesh.polygons

        # Triangulate the mesh
        verts, faces = triangulate(meshobj)

        write_with_indent(indent, 'Shape "trianglemesh"\n')

        vert_str = ''
        for vert in verts:
            vert_str += '{} {} {} '.format(*vert.to_tuple())
        write_with_indent(indent + 1, ('"integer indices" [ ' + vert_str[:-1] + ' ]\n'))

        face_str = ''
        for face in faces:
            face_str += '{} {} {} '.format(*face)
        write_with_indent(indent + 1, ('"point P" [ ' + face_str[:-1] + ' ]\n'))

    def read_from_file(self, parser):
        pass

