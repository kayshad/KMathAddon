bl_info = {
    "name": "KMathAddon",
    "blender": (3, 0, 0),
    "category": "Object",
}



import bpy


from . settings import *
from . surf3dz import *
from . surf3dxyz import *
from . monop import *
from . monpano import MonPano

classes = [Settings, MonOp, MonPano]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= Settings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
