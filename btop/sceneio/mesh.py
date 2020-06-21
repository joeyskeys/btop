

import bpy

import math

class MeshIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer, meshobj):
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
        writer.write('Translate {} {} {}'.format(*translation))
        writer.write('Scale {} {} {}'.format(*scale))
        writer.write('Rotate {} {} {} {}'.format(rotate_angle, *rotate_vec))

        # Get mesh data
        mesh = meshobj.data
        verts = mesh.vertices
        faces = mesh.polygons

        # Triangulate the mesh
        # ...

        writer.write('Shape "trianglemesh" ')

    def read_from_file(self, parser):
        pass

