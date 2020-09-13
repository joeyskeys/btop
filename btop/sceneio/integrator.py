# todo : license

import bpy


class IntegratorIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):
        integrator_props = bpy.context.scene.pbrt_integrator_props
        integrator_type = integrator_props.integrator_type
        integrator_line_comps = ['Integrator "{}"'.format(integrator_type)]
        integrator_line_comps.append('maxdepth {}'.format(integrator_props.max_depth))

        if integrator_type in ["path", "directlighting", "bdpt"]:
            p_x_min = integrator_props.pixelbound_x_min
            p_x_max = integrator_props.pixelbound_x_max
            p_y_min = integrator_props.pixelbound_y_min
            p_y_max = integrator_props.pixelbound_y_max

            film_props = bpy.context.scene.pbrt_film_props
            film_x_resolution = film_props.x_resolution
            film_y_resolution = film_props.y_resolution

            integrator_line_comps.append('integer[4] pixelbounds [{} {} {} {}]'.format(p_x_min,
                                                                                       min(p_x_max, film_x_resolution),
                                                                                       p_y_min,
                                                                                       min(p_y_max, film_y_resolution)))

        if integrator_type in ["path", "bdpt"]:
            integrator_line_comps.append('lightsamplestrategy "{}"'.format(integrator_props.light_sample_strategy))

        if integrator_type == "path":
            integrator_line_comps.append('rrthreshold {}'.format(integrator_props.rr_threshold))

        if integrator_type == "directlighting":
            integrator_line_comps.append('strategy "{}"'.format(integrator_props.strategy))

        if integrator_type == "bdpt":
            integrator_line_comps.append('visualizestrategies {}'.format(integrator_props.visualizestrategies))
            integrator_line_comps.append('visualizeweights {}'.format(integrator_props.visualizeweights))

        if integrator_type == "mlt":
            integrator_line_comps.append('bootstrapsamples {}'.format(integrator_props.bootstrap_samples))
            integrator_line_comps.append('chains {}'.format(integrator_props.chains))
            integrator_line_comps.append('mutationsperpixel {}'.format(integrator_props.mutations_per_pixel))
            integrator_line_comps.append('largestepprobability {}'.format(integrator_props.largest_step_probability))
            integrator_line_comps.append('sigma {}'.format(integrator_props.sigma))

        if integrator_type == "sppm":
            integrator_line_comps.append('iterations {}'.format(integrator_props.iterations))
            integrator_line_comps.append('photonsperiteration {}'.format(integrator_props.photons_per_iteration))
            integrator_line_comps.append('imagewritefrequency {}'.format(integrator_props.image_write_frequency))
            integrator_line_comps.append('radius {}'.format(integrator_props.radius))

        writer.write(' '.join(integrator_line_comps) + '\n\n')

    def read_from_file(self, parser):
        pass