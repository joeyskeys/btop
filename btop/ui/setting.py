# todo : license

import bpy


class PBRTSettingProperties(bpy.types.PropertyGroup):
    pbrt_location: bpy.props.StringProperty(name="pbrt_location",
                                            description="PBRT executable location",
                                            default="",
                                            subtype='FILE_PATH')

    pbrt_cache_folder: bpy.props.StringProperty(name="pbrt_cache_folder",
                                                description="PBRT cache folder",
                                                default="",
                                                subtype='FILE_PATH')


class PBRT_PT_setting(bpy.types.Panel):
    bl_label = "Setting"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {'PBRT_RENDER'}
    bl_context = 'render'

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        setting_props = context.scene.pbrt_setting_props
        layout.row().prop(setting_props, "pbrt_location", text="PBRT Location")
        layout.row().prop(setting_props, "pbrt_cache_folder", text="Cache Folder")


def register():
    # Register property group
    bpy.utils.register_class(PBRTSettingProperties)
    bpy.types.Scene.pbrt_setting_props = bpy.props.PointerProperty(type=PBRTSettingProperties)

    # Register UIs
    bpy.utils.register_class(PBRT_PT_setting)


def unregister():
    # Unregister property group
    del bpy.types.Scene.pbrt_setting_props
    bpy.utils.unregister_class(PBRTSettingProperties)

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_setting)