import bpy
from . settings import update_fonc



class MonOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mon.operateur"
    bl_label = "label operateur"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        self.equationc = mytool.equationc
        #print(mytool.equationc, 'par bouton operateur')
        update_fonc(self, context)
        return {'FINISHED'}
