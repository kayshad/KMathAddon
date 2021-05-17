import bpy

from . settings import safe_list, safe_dict

from bpy.types import (Operator)

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       PointerProperty)



# Create a new mesh (object) from verts/edges/faces
# verts/edges/faces ... List of vertices/edges/faces for the
#                       new mesh (as used in from_pydata)
# name ... Name of the new mesh (& object)

def create_mesh_object(context, verts, edges, faces, name):

    # Create new mesh
    mesh = bpy.data.meshes.new(name)

    # Make a mesh from a list of verts/edges/faces
    mesh.from_pydata(verts, edges, faces)

    # Update mesh geometry after adding stuff
    mesh.update()

    from bpy_extras import object_utils
    return object_utils.object_data_add(context, mesh, operator=None)


# A very simple "bridge" tool

def createFaces(vertIdx1, vertIdx2, closed=False, flipped=False):
    faces = []

    if not vertIdx1 or not vertIdx2:
        return None

    if len(vertIdx1) < 2 and len(vertIdx2) < 2:
        return None

    fan = False
    if (len(vertIdx1) != len(vertIdx2)):
        if (len(vertIdx1) == 1 and len(vertIdx2) > 1):
            fan = True
        else:
            return None

    total = len(vertIdx2)

    if closed:
        # Bridge the start with the end
        if flipped:
            face = [
                vertIdx1[0],
                vertIdx2[0],
                vertIdx2[total - 1]]
            if not fan:
                face.append(vertIdx1[total - 1])
            faces.append(face)

        else:
            face = [vertIdx2[0], vertIdx1[0]]
            if not fan:
                face.append(vertIdx1[total - 1])
            face.append(vertIdx2[total - 1])
            faces.append(face)

    # Bridge the rest of the faces
    for num in range(total - 1):
        if flipped:
            if fan:
                face = [vertIdx2[num], vertIdx1[0], vertIdx2[num + 1]]
            else:
                face = [vertIdx2[num], vertIdx1[num],
                    vertIdx1[num + 1], vertIdx2[num + 1]]
            faces.append(face)
        else:
            if fan:
                face = [vertIdx1[0], vertIdx2[num], vertIdx2[num + 1]]
            else:
                face = [vertIdx1[num], vertIdx2[num],
                    vertIdx2[num + 1], vertIdx1[num + 1]]
            faces.append(face)

    return faces


class AddZFunctionSurface(Operator):
    bl_idname = "mesh.primitive_z_function_surface"
    bl_label = "Add Z Function Surface"
    bl_description = "Add a surface defined defined by a function z=f(x,y)"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}



    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        equation = mytool.equation
        div_x = mytool.div_x
        div_y = mytool.div_y
        size_x = mytool.size_x
        size_y = mytool.size_y
        equation = self.equation

        verts = []
        faces = []

        delta_x = size_x / (div_x - 1)
        delta_y = size_y / (div_y - 1)
        start_x = -(size_x / 2.0)
        start_y = -(size_y / 2.0)

        edgeloop_prev = []

        if equation:
            try:
                expr_args = (
                    compile(equation, __file__, 'eval'),
                    {"__builtins__": None},
                    safe_dict)
            except:
                import traceback
                # WARNING is used to prevent the constant pop-up spam
                self.report({'WARNING'},
                            "Error parsing expression: {} "
                            "(Check the console for more info)".format(equation))
                print("\n[Add Z Function Surface]:\n\n", traceback.format_exc(limit=1))

                return {'CANCELLED'}

            for row_x in range(div_x):
                edgeloop_cur = []
                x = start_x + row_x * delta_x

                for row_y in range(div_y):
                    y = start_y + row_y * delta_y
                    z = 0.0

                    safe_dict['x'] = x
                    safe_dict['y'] = y

                    # Try to evaluate the equation.
                    try:
                        z = float(eval(*expr_args))
                    except:
                        import traceback
                        self.report({'WARNING'},
                                    "Error evaluating expression: {} "
                                    "(Check the console for more info)".format(equation))
                        print("\n[Add Z Function Surface]:\n\n", traceback.format_exc(limit=1))

                        return {'CANCELLED'}

                    edgeloop_cur.append(len(verts))
                    verts.append((x, y, z))

                if len(edgeloop_prev) > 0:
                    faces_row = createFaces(edgeloop_prev, edgeloop_cur)
                    faces.extend(faces_row)

                edgeloop_prev = edgeloop_cur

            base = create_mesh_object(context, verts, [], faces, "Z Function")
        else:
            self.report({'WARNING'}, "Z Equation - No expression is given")

            return {'CANCELLED'}

        return {'FINISHED'}
