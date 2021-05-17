import bpy
from math import *
from . settings import safe_list, safe_dict


from bpy.types import (Operator)

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       PointerProperty)


def xyz_function_surface_faces(self, x_eq, y_eq, z_eq,
            range_u_min, range_u_max, range_u_step, wrap_u,
            range_v_min, range_v_max, range_v_step, wrap_v,
            a_eq, b_eq, c_eq, f_eq, g_eq, h_eq, n, close_v):

    verts = []
    faces = []

    # Distance of each step in Blender Units
    uStep = (range_u_max - range_u_min) / range_u_step
    vStep = (range_v_max - range_v_min) / range_v_step

    # Number of steps in the vertex creation loops.
    # Number of steps is the number of faces
    #   => Number of points is +1 unless wrapped.
    uRange = range_u_step + 1
    vRange = range_v_step + 1

    if wrap_u:
        uRange = uRange - 1

    if wrap_v:
        vRange = vRange - 1

    try:
        expr_args_x = (
            compile(x_eq, __file__.replace(".py", "_x.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_y = (
            compile(y_eq, __file__.replace(".py", "_y.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_z = (
            compile(z_eq, __file__.replace(".py", "_z.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_a = (
            compile(a_eq, __file__.replace(".py", "_a.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_b = (
            compile(b_eq, __file__.replace(".py", "_b.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_c = (
            compile(c_eq, __file__.replace(".py", "_c.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_f = (
            compile(f_eq, __file__.replace(".py", "_f.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_g = (
            compile(g_eq, __file__.replace(".py", "_g.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
        expr_args_h = (
            compile(h_eq, __file__.replace(".py", "_h.py"), 'eval'),
            {"__builtins__": None},
            safe_dict)
    except:
        import traceback
        self.report({'WARNING'}, "Error parsing expression(s) - "
                    "Check the console for more info")
        print("\n[Add X, Y, Z Function Surface]:\n\n", traceback.format_exc(limit=1))
        return [], []

    for vN in range(vRange):
        v = range_v_min + (vN * vStep)

        for uN in range(uRange):
            u = range_u_min + (uN * uStep)

            safe_dict['u'] = u
            safe_dict['v'] = v

            safe_dict['n'] = n

            # Try to evaluate the equations.
            try:
                safe_dict['a'] = float(eval(*expr_args_a))
                safe_dict['b'] = float(eval(*expr_args_b))
                safe_dict['c'] = float(eval(*expr_args_c))
                safe_dict['f'] = float(eval(*expr_args_f))
                safe_dict['g'] = float(eval(*expr_args_g))
                safe_dict['h'] = float(eval(*expr_args_h))

                verts.append((
                    float(eval(*expr_args_x)),
                    float(eval(*expr_args_y)),
                    float(eval(*expr_args_z))))
            except:
                import traceback
                self.report({'WARNING'}, "Error evaluating expression(s) - "
                             "Check the console for more info")
                print("\n[Add X, Y, Z Function Surface]:\n\n", traceback.format_exc(limit=1))
                return [], []

    for vN in range(range_v_step):
        vNext = vN + 1

        if wrap_v and (vNext >= vRange):
            vNext = 0

        for uN in range(range_u_step):
            uNext = uN + 1

            if wrap_u and (uNext >= uRange):
                uNext = 0

            faces.append([(vNext * uRange) + uNext,
                (vNext * uRange) + uN,
                (vN * uRange) + uN,
                (vN * uRange) + uNext])

    if close_v and wrap_u and (not wrap_v):
        for uN in range(1, range_u_step - 1):
            faces.append([
                range_u_step - 1,
                range_u_step - 1 - uN,
                range_u_step - 2 - uN])
            faces.append([
                range_v_step * uRange,
                range_v_step * uRange + uN,
                range_v_step * uRange + uN + 1])

    return verts, faces


# Original Script "Parametric.py" by Ed Mackey.
# -> http://www.blinken.com/blender-plugins.php
# Partly converted for Blender 2.5 by tuga3d.
#
# Sphere:
# x = sin(2*pi*u)*sin(pi*v)
# y = cos(2*pi*u)*sin(pi*v)
# z = cos(pi*v)
# u_min = v_min = 0
# u_max = v_max = 1
#
# "Snail shell"
# x = 1.2**v*(sin(u)**2 *sin(v))
# y = 1.2**v*(sin(u)*cos(u))
# z = 1.2**v*(sin(u)**2 *cos(v))
# u_min = 0
# u_max = pi
# v_min = -pi/4,
# v max = 5*pi/2

class AddXYZFunctionSurface(Operator):
    bl_idname = "mesh.primitive_xyz_function_surface"
    bl_label = "Add X, Y, Z Function Surface"
    bl_description = ("Add a surface defined defined by 3 functions:\n"
                      "x=F1(u,v), y=F2(u,v) and z=F3(u,v)")
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        for n in range(0, self.n_eq):
            verts, faces = xyz_function_surface_faces(
                                self,
                                mytool.x_eq,
                                mytool.y_eq,
                                mytool.z_eq,
                                mytool.range_u_min,
                                mytool.range_u_max,
                                mytool.range_u_step,
                                mytool.wrap_u,
                                mytool.range_v_min,
                                mytool.range_v_max,
                                mytool.range_v_step,
                                mytool.wrap_v,
                                mytool.a_eq,
                                mytool.b_eq,
                                mytool.c_eq,
                                mytool.f_eq,
                                mytool.g_eq,
                                mytool.h_eq,
                                n,
                                self.close_v
                                )
            if not verts:
                return {'CANCELLED'}

            obj = create_mesh_object(context, verts, [], faces, "XYZ Function")

            if self.show_wire:
                obj.show_wire = True

        if self.edit_mode:
            bpy.ops.object.mode_set(mode = 'EDIT')
        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}
