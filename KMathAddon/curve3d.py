import bpy
import math
import numpy
import sympy

from bpy.props import (StringProperty)





# List of safe functions for eval()
safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'gcd']

# Use the list to filter the local namespace
safe_dict = dict((k, globals().get(k, None)) for k in safe_list)
safe_dict['math'] = math
safe_dict['numpy'] = safe_dict['np'] = numpy
safe_dict['sympy'] = sympy
safe_dict['lcm'] = numpy.lcm
safe_dict['max'] = max
safe_dict['min'] = min

def update_fonc(self, context):
    wm = context.window_manager
    #print(wm.equation)
    equation = wm.equation
    if equation:
        try:
            expr_args = (compile(equation, __file__, 'eval'),{"__builtins__": None},safe_dict)


        except:
            import traceback
            # WARNING is used to prevent the constant pop-up spam
            print("\n[Add Function Curve]:\n\n", traceback.format_exc(limit=1))



        # Try to evaluate the equation.
        try:
            name = 'fonction'
            bname = 'fonction'

            for cur in bpy.data.curves:
                if bname in cur.name:
                    bpy.data.curves.remove(cur)
            for o in bpy.data.objects:
                if bname in o.name:
                    bpy.data.objects.remove(o)
            for c in bpy.data.collections:
                if 'MaCollection' in c.name:
                    bpy.data.collections.remove(c)

            MaColl = bpy.data.collections.new('MaCollection'+name)
            context.scene.collection.children.link(MaColl)
            curveData = bpy.data.curves.new(name, type='CURVE')
            curveData.dimensions = '3D'
            curveData.resolution_u = 2
            curveData.bevel_depth = 0.01
            curveOB = bpy.data.objects.new(name, curveData)
            MaColl.objects.link(curveOB)
            n = 200
            yVals = []
            xVals = numpy.linspace(-5,5,n)
            zoom = 1
            for x in xVals:
                safe_dict['x'] = x
                y = float(eval(*expr_args))
                yVals.append((zoom*x,0.0,zoom*float(eval(*expr_args)),1))
            bpy.data.curves[name].splines.new('POLY')
            p = bpy.data.curves[name].splines[0].points
            p.add(len(yVals)-1)
            for i, coord in enumerate(yVals):
                p[i].co = coord


        except:
            import traceback
            print("\n[Add Z Function Surface]:\n\n", traceback.format_exc(limit=1))




    else:
        print("No expression is given")

bpy.types.WindowManager.equation = bpy.props.StringProperty(
        name="Equation",
        description="Equation for y=f(x)",
        default="x",
        update=update_fonc
        )
