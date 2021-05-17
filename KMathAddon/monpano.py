import bpy

class MonPano(bpy.types.Panel):
    bl_label = "Mon_PT_Pano"
    bl_idname = "MON_PT_Pano"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MonPano"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "equationc")
        layout.operator("mon.operateur")

        row = layout.row(align=True)
        row.prop(mytool, "size_x")
        row = layout.row(align=True)
        row.prop(mytool, "size_y")
        row = layout.row(align=True)
        row.prop(mytool, "div_x")
        row = layout.row(align=True)
        row.prop(mytool, "div_y")
        props = self.layout.operator("mesh.primitive_z_function_surface")

        props.equation = mytool.equation
        props.size_x = mytool.size_x
        props.size_y = mytool.size_y
        props.div_x = mytool.div_x
        props.div_y = mytool.div_y
        row = layout.row()
        row.prop(mytool, "x_eq")
        layout.row().prop(mytool, "y_eq")
        layout.row().prop(mytool, "y_eq")
        layout.row().prop(mytool, "z_eq")
        layout.row().prop(mytool, "range_u_min")
        layout.row().prop(mytool, "range_u_max")
        layout.row().prop(mytool, "range_u_step")
        layout.row().prop(mytool, "wrap_u")
        layout.row().prop(mytool, "range_v_min")
        layout.row().prop(mytool, "range_v_max")
        layout.row().prop(mytool, "range_v_step")
        layout.row().prop(mytool, "wrap_v")
        layout.row().prop(mytool, "n_eq")
        layout.row().prop(mytool, "a_eq")
        layout.row().prop(mytool, "b_eq")
        layout.row().prop(mytool, "c_eq")
        layout.row().prop(mytool, "f_eq")
        layout.row().prop(mytool, "g_eq")
        layout.row().prop(mytool, "h_eq")
        layout.row().prop(mytool, "show_wire")
        layout.row().prop(mytool, "edit_mode")
        props1 = self.layout.operator("mesh.primitive_xyz_function_surface")
