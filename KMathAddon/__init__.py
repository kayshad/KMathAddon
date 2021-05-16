bl_info = {
    "name": "KMathAddon",
    "blender": (3, 0, 0),
    "category": "Object",
}



import bpy



from . props import Settings
from . curve3d import safe_list, safe_dict, update_fonc
from . surf3dz import *
from . surf3dxyz import *
#from . monpano import Settings, MonPano
from . monpano import MonPano




classes = [MonPano, Settings]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mesdata = PointerProperty(type=Settings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mesdata
