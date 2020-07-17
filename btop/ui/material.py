# todo : license

import bpy

# It's not quite clever to add material properties this way...
class PBRTMaterialProperties(bpy.types.PropertyGroup):
    material_type: bpy.props.EnumProperty(name="material_type",
                                          items=[
                                              ("disney", "Disney", ""),
                                              ("fourier", "Fourier", ""),
                                              ("glass", "Glass", ""),
                                              ("hair", "Hair", ""),
                                              ("kdsubsurface", "KdSubsurface", ""),
                                              ("matte", "Matte", ""),
                                              ("mirror", "Mirror", ""),
                                              ("mix", "Mix", ""),
                                              ("none", "None", ""),
                                              ("plastic", "Plastic", ""),
                                              ("substrate", "Substrate", ""),
                                              ("subsurface", "Subsurface", ""),
                                              ("translucent", "Translucent", ""),
                                              ("uber", "Uber", "")
                                          ],
                                          default="disney")

    disney_color:\
        bpy.props.FloatVectorProperty(name="disney_color",
                                      description="Base color of the material",
                                      default=[0.5, 0.5, 0.5],
                                      min=[0, 0, 0],
                                      max=[1, 1, 1],
                                      subtype='COLOR')

    disney_anisotropic:\
        bpy.props.FloatProperty(name="disney_anisotropic",
                                description="Controls degree of anisotropy in the specular highlight",
                                default=0,
                                min=0,
                                max=1)

    disney_clearcoat:\
        bpy.props.FloatProperty(name="disney_clearcoat",
                                description="")


class PBRT_PT_materialslots(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_label = 'Material'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return (context.material or context.object) and renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout

        mat = context.material
        slot = context.material_slot
        obj = context.object
        space = context.space_data

        if obj:
            is_sortable = len(obj.material_slots) > 1
            rows = 3
            if is_sortable:
                rows = 5

            row = layout.row()

            row.template_list("MATERIAL_UL_matslots", "", obj, "material_slots", obj, "active_material_index", rows=rows)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ZOOMIN', text="")
            col.operator("object.material_slot_remove", icon="ZOOMOUT", text="")

            col.menu("MATERIAL_MT_specials", icon="DOWNARROW_HLT", text="")

            if is_sortable:
                col.separator()

                col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
                col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

            if obj.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        split = layout.split(percentage=0.65)

        if obj:
            split.template_ID(obj, "active_material", new="material.new")
            row = split.row()

            if slot:
                row.prop(slot, "link", text="")
            else:
                row.label()
        elif mat:
            split.template_ID(space, "pin_id")
            split.separator()


class PBRT_PT_materialdetails(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_label = 'Details'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return (context.material or context.object) and renderer.engine == 'PBRT_RENDER'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        material_props = context.scene.pbrt_material_props


def register():
    # Register property group
    bpy.utils.register_class()

    # Register UIs
    bpy.utils.register_class(PBRT_PT_materialslots)


def unregister():
    # Unregister property group
    bpy.utils.unregister_class()

    # Unregister UIs
    bpy.utils.unregister_class(PBRT_PT_materialslots)