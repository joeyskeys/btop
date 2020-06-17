# todo : license

import bpy


class PBRTCameraProperties(bpy.types.PropertyGroup):
    camera_type: bpy.props.EnumProperty(name="camera_type",
                                        items=[
                                            ("perspective", "Perspective", ""),
                                            ("orthographic", "Orthographic", ""),
                                            ("environment", "Environment", ""),
                                            ("realistic", "Realistic", "")],

                                        default="perspective")

    shutter_open: bpy.props.FloatProperty(name="shutter_open",
                                          description="Shutter open time point of a frame",
                                          default=0,
                                          max=1,
                                          min=0)

    shutter_close: bpy.props.FloatProperty(name="shutter_close",
                                           description="Shutter close time point of a frame",
                                           default=1,
                                           max=1,
                                           min=0)

    # persp, ortho, env
    frame_ratio: bpy.props.FloatProperty(name="frame_ratio",
                                         description="The aspect ratio of the film",
                                         default=1,
                                         max=10,
                                         min=0.1)

    # For persp, ortho, env
    screen_window: bpy.props.FloatProperty(name="screen_window",
                                           description="The bounds of the film plane in screen space",
                                           default=1,
                                           max=1,
                                           min=0.1)

    # For persp, ortho
    lens_radius: bpy.props.FloatProperty(name="lens_radius",
                                         description="The radius of the lens",
                                         default=0,
                                         soft_max=100,
                                         min=0)

    # For persp, ortho
    focal_distance: bpy.props.FloatProperty(name="focal_distance",
                                            description="The focal distance of the lens",
                                            default=10,
                                            max=10**30,
                                            min=0)

    # For persp
    fov: bpy.props.FloatProperty(name="fov",
                                 description="Specifies the field of view for the perspective camera",
                                 default=90,
                                 max=180,
                                 min=1)

    # Below are for realistic
    lens_file: bpy.props.StringProperty(name="lens_file",
                                        description="Specifies the name of a lens description file",
                                        default="",
                                        subtype='FILE_PATH')

    aperture_diameter: bpy.props.FloatProperty(name="aperture_diameter",
                                               description="Diameter of the lens system's aperture in mm",
                                               default=1,
                                               soft_max=100,
                                               min=0)

    focus_distance: bpy.props.FloatProperty(name="focus_distance",
                                            description="Distance in meters at which the lens system is focused",
                                            default=10,
                                            soft_max=1000,
                                            min=0)

    simple_weighting: bpy.props.BoolProperty(name="simple_weighting",
                                             description="Indicate whether to use simple weight or not",
                                             default=True)


class PBRT_PT_camera(bpy.types.Panel):
    bl_label = "Camera"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER' and context.active_object.type == 'CAMERA'

    def draw(self, context):
        layout = self.layout

        # Need to test what is for this line
        layout.use_property_split = True

        cam_props = context.camera.pbrt_camera_props
        layout.row().prop(cam_props, "camera_type", text="Camera Type")

        col = layout.column()

        if cam_props.camera_type != "realistic":
            layout.row().prop(cam_props, "frame_ratio", text="Frame Ratio")
            layout.row().prop(cam_props, "screen_window", text="Screen Window")
            
            if cam_props.camera_type != "environment":
                layout.row().prop(cam_props, "lens_radius", text="Lens Radius")
                layout.row().prop(cam_props, "focal_distance", text="Focal Distance")

            if cam_props.camera_type == "perspective":
                layout.row().prop(cam_props, "fov", text="FOV")

        else:
            layout.row().prop(cam_props, "lens_file", text="Lens File")
            layout.row().prop(cam_props, "aperture_diameter", text="Aperture Diameter")
            layout.row().prop(cam_props, "focus_distance", text="Focus Distance")
            layout.row().prop(cam_props, "simple_weighting", text="Simple Weighting")


class PBRT_PT_shutter(bpy.types.Panel):
    bl_label = "Shutter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER' and context.active_object.type == 'CAMERA'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam_props = context.camera.pbrt_camera_props
        layout.row().prop(cam_props, "shutter_open", text="Shutter Open")
        layout.row().prop(cam_props, "shutter_close", text="Shutter Close")


def register():
    # Register property group
    bpy.utils.register_class(PBRTCameraProperties)
    bpy.types.Camera.pbrt_camera_props = bpy.props.PointerProperty(type=PBRTCameraProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_camera)
    bpy.utils.register_class(PBRT_PT_shutter)


def unregister():
    # Unregister property group
    del bpy.types.Camera.pbrt_camera_props
    bpy.utils.unregister_class(PBRTCameraProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_camera)
    bpy.utils.unregister_class(PBRT_PT_shutter)