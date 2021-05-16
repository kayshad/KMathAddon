import bpy
from math import *

from bpy.types import (PropertyGroup)

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       PointerProperty)



class Settings(PropertyGroup):
    
    equation: StringProperty(
                name="Equation pour z=f(x,y)",
                description="Equation for z=f(x,y)",
                default="1 - ( x**2 + y**2 )"
                )
    
    div_x: IntProperty(
                name="X Subdivisions",
                description="Number of vertices in x direction",
                default=16,
                min=3,
                max=256
                )
    div_y: IntProperty(
                name="Y Subdivisions",
                description="Number of vertices in y direction",
                default=16,
                min=3,
                max=256
                )
    size_x: FloatProperty(
                name="X taille",
                description="Size of the x axis",
                default=2.0,
                min=0.01,
                max=100.0,
                unit="LENGTH"
                )
    size_y: FloatProperty(
                name="Y taille",
                description="Size of the y axis",
                default=2.0,
                min=0.01,
                max=100.0,
                unit="LENGTH"
                )
                
                
    x_eq: StringProperty(
                name="X equation",
                description="Equation for x=F(u,v). "
                            "Also available: n, a, b, c, f, g, h",
                default="cos(v)*(1+cos(u))*sin(v/8)"
                )
    y_eq: StringProperty(
                name="Y equation",
                description="Equation for y=F(u,v). "
                            "Also available: n, a, b, c, f, g, h",
                default="sin(u)*sin(v/8)+cos(v/8)*1.5"
                )
    z_eq: StringProperty(
                name="Z equation",
                description="Equation for z=F(u,v). "
                            "Also available: n, a, b, c, f, g, h",
                default="sin(v)*(1+cos(u))*sin(v/8)"
                )
    range_u_min: FloatProperty(
                name="U min",
                description="Minimum U value. Lower boundary of U range",
                min=-100.00,
                max=0.00,
                default=0.00
                )
    range_u_max: FloatProperty(
                name="U max",
                description="Maximum U value. Upper boundary of U range",
                min=0.00,
                max=100.00,
                default=2 * pi
                )
    range_u_step: IntProperty(
                name="U step",
                description="U Subdivisions",
                min=1,
                max=1024,
                default=32
                )
    wrap_u: BoolProperty(
                name="U wrap",
                description="U Wrap around",
                default=True
                )
    range_v_min: FloatProperty(
                name="V min",
                description="Minimum V value. Lower boundary of V range",
                min=-100.00,
                max=0.00,
                default=0.00
                )
    range_v_max: FloatProperty(
                name="V max",
                description="Maximum V value. Upper boundary of V range",
                min=0.00,
                max=100.00,
                default=4 * pi
                )
    range_v_step: IntProperty(
                name="V step",
                description="V Subdivisions",
                min=1,
                max=1024,
                default=128
                )
    wrap_v: BoolProperty(
                name="V wrap",
                description="V Wrap around",
                default=False
                )
    close_v: BoolProperty(
                name="Close V",
                description="Create faces for first and last "
                            "V values (only if U is wrapped)",
                default=False
                )
    n_eq: IntProperty(
                name="Number of objects (n=0..N-1)",
                description="The parameter n will be the index "
                            "of the current object, 0 to N-1",
                min=1,
                max=100,
                default=1
                )
    a_eq: StringProperty(
                name="A helper function",
                description="Equation for a=F(u,v). Also available: n",
                default="0"
                )
    b_eq: StringProperty(
                name="B helper function",
                description="Equation for b=F(u,v). Also available: n",
                default="0"
                )
    c_eq: StringProperty(
                name="C helper function",
                description="Equation for c=F(u,v). Also available: n",
                default="0"
                )
    f_eq: StringProperty(
                name="F helper function",
                description="Equation for f=F(u,v). Also available: n, a, b, c",
                default="0"
                )
    g_eq: StringProperty(
                name="G helper function",
                description="Equation for g=F(u,v). Also available: n, a, b, c",
                default="0"
                )
    h_eq: StringProperty(
                name="H helper function",
                description="Equation for h=F(u,v). Also available: n, a, b, c",
                default="0"
                )
    show_wire : BoolProperty(
            name="Show wireframe",
            default=True,
            description="Add the object’s wireframe over solid drawing"
            )
    edit_mode : BoolProperty(
            name="Show in edit mode",
            default=True,
            description="Show in edit mode"
            )