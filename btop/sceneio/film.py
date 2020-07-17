
# todo : license

import bpy
import mathutils


class FilmIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):

        render_obj = bpy.context.scene.render
        film_props = bpy.context.scene.pbrt_film_props

        # Currently image is the only film type
        # Hard coded here
        film_line_comps = ['Film "image"']

        film_line_comps.append('integer xresolution {}'.format(render_obj.resolution_x))
        film_line_comps.append('integer yresolution {}'.format(render_obj.resolution_y))

        crop_win_x_min = film_props.crop_window_x_min
        crop_win_x_max = film_props.crop_window_x_max
        crop_win_y_min = film_props.crop_window_y_min
        crop_win_y_max = film_props.crop_window_y_max
        film_line_comps.append('float[4] cropwindow [{} {} {} {}]'.format(crop_win_x_min,
                                                                            crop_win_x_max,
                                                                            crop_win_y_min,
                                                                            crop_win_y_max))

        film_line_comps.append('float scale {}'.format(film_props.scale))
        film_line_comps.append('float maxsampleluminance {}'.format(film_props.max_sample_luminance))
        film_line_comps.append('float diagonal {}'.format(film_props.diagonal))
        film_line_comps.append('float filename "{}"'.format(film_props.filename))

        writer.write(' '.join(film_line_comps) + '\n\n')

    def read_from_file(self, parser):
        pass