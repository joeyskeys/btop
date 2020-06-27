

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
        rot = matrix.to_quternion()
        rotate_angle = 2 * math.acos(rot[0])
        denom = math.sqrt(1 - rot[0] * rot[0])
        x_fac = rot[1] / denom
        y_fac = rot[2] / denom
        z_fac = rot[3] / denom
        rotate_vec = (x_fac, y_fac, z_fac)

        # Write out transformation
        write_with_indent(indent, 'Translate {} {} {}'.format(*translation))
        write_with_indent(indent, 'Scale {} {} {}'.format(*scale))
        write_with_indent(indent, 'Rotate {} {} {} {}'.format(rotate_angle, *rotate_vec))

        # Get mesh data
        #mesh = meshobj.data
        #verts = mesh.vertices
        #faces = mesh.polygons

        # Triangulate the mesh
        verts, faces = triangulate(meshobj)

        write_with_indent(indent, 'Shape "trianglemesh" ')

        vert_str = ''
        for vert in verts:
            vert_str += '{} {} {} '.format(*vert.to_tuple())
        write_with_indent(indent + 1, ('"integer indices [ ' + vert_str[:-1] + ' ]'))

        face_str = ''
        for face in faces:
            face_str += '{} {} {} '.format(*face)
        write_with_indent(indent + 1, ('"point P" [ ' +  + ' ]'))

    def read_from_file(self, parser):
        pass

