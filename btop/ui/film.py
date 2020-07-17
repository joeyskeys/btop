# todo : license

import bpy


class PBRTFilmProperties(bpy.types.PropertyGroup):
    x_resolution: bpy.props.IntProperty(name="x_resolution",
                                        description="The number of pixels in the x direction",
                                        default=640,
                                        soft_max=4096,
                                        min=1)

    y_resolution: bpy.props.IntProperty(name="y_resolution",
                                        description="The number of pixels in the y direction",
                                        default=480,
                                        soft_max=2160,
                                        min=1)

    crop_window_x_min: bpy.props.FloatProperty(name="crop_window_x_min",
                                               description="The minimum x of subregion of the image to render",
                                               default=0,
                                               max=1,
                                               min=0)

    crop_window_x_max: bpy.props.FloatProperty(name="crop_window_x_max",
                                               description="The maximum x of subregion of the image to render",
                                               default=1,
                                               max=1,
                                               min=0)

    crop_window_y_min: bpy.props.FloatProperty(name="crop_window_y_min",
                                               description="The minimum y of subregion of the image to render",
                                               default=0,
                                               max=1,
                                               min=0)

    crop_window_y_max: bpy.props.FloatProperty(name="crop_window_y_max",
                                               description="The maximum y of subregion of the image to render",
                                               default=1,
                                               max=1,
                                               min=0)

    scale: bpy.props.FloatProperty(name="scale",
                                   description="Scale factor to apply to film pixel values before saving the image",
                                   default=1,
                                   max=1,
                                   min=0)

    max_sample_luminance: bpy.props.FloatProperty(name="max_sample_luminance",
                                                  description="The maximum limit of image sample values",
                                                  default=10**10,
                                                  max=10**10,
                                                  min=1)

    diagonal: bpy.props.FloatProperty(name="diagonal",
                                      description="Diagonal length of the film, in mm",
                                      default=35,
                                      soft_max=90,
                                      soft_min=15)

    filename: bpy.props.StringProperty(name="filename",
                                       description="The output filename",
                                       default="",
                                       subtype="FILE_PATH")


class PBRT_PT_film(bpy.types.Panel):
    bl_label = "Film"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "output"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        film_props = context.scene.pbrt_film_props
        layout.row().prop(film_props, "x_resolution", text="Resolution X")
        layout.row().prop(film_props, "y_resolution", text="Resolution Y")
        layout.row().prop(film_props, "crop_window_x_min", text="Crop Window X Min")
        layout.row().prop(film_props, "crop_window_x_max", text="Crop Window X Max")
        layout.row().prop(film_props, "crop_window_y_min", text="Crop Window Y Min")
        layout.row().prop(film_props, "crop_window_y_max", text="Crop Window Y Max")
        layout.row().prop(film_props, "scale", text="Scale")
        layout.row().prop(film_props, "max_sample_luminance", text="Max Sample Luminance")
        layout.row().prop(film_props, "diagonal", text="Diagonal")
        layout.row().prop(film_props, "filename", text="Filename")


def register():
    # Register property group
    bpy.utils.register_class(PBRTFilmProperties)
    bpy.types.Scene.pbrt_film_props = bpy.props.PointerProperty(type=PBRTFilmProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_film)


def unregister():
    # Unregister property group
    del bpy.types.Scene.pbrt_film_props
    bpy.utils.unregister_class(PBRTFilmProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_film)
