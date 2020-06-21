# todo : license

import bpy


class SamplerIO(object):
    """

    """

    def __init__(self):
        pass

    def write_to_file(self, writer):
        # Get sampler properties
        sampler_props = bpy.context.scene.pbrt_sampler_props
        sampler_line_comps = ['Sampler "{}"'.format(sampler_props.sampler_type)]

        if sampler_props.sampler_type != "stratified":
            sampler_line_comps.append('integer pixelsamples {}'.format(sampler_props.pixel_samples))
        else:
            sampler_line_comps.append('bool jitter "{}"'.format(sampler_props.jitter))
            sampler_line_comps.append('integer xsamples {}'.format(sampler_props.xsamples))
            sampler_line_comps.append('integer ysamples {}'.format(sampler_props.ysamples))

        # Write out
        writer.write(' '.join(sampler_line_comps))

    def read_from_file(self, parser):
        pass
