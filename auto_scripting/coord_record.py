import bpy, bmesh

robot_obj = bpy.data.objects['TheRobot']

robot_path = bpy.data.objects['NurbsPath']

obj = bpy.context.active_object

robot_obj.select = True

bpy.context.scene.objects.active = robot_obj

if obj.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(obj.data)
    vertices = bm.verts

else:
    vertices = obj.data.vertices

verts = [obj.matrix_world * vert.co for vert in vertices] 

# coordinates as tuples
plain_verts = [vert.to_tuple() for vert in verts]
print(plain_verts)
b = 0
fe = 256
increment = 25

with open("C:\\Users\**YOURNAME000***\Desktop\path.txt", "w") as file:
    for x in range(0,fe) and b in range(0,fe):
    coords = plainverts[x]
    coordsX = coords(1)
    coordsY = coords(2)
    b = b + increment
    print(b, coordsX, coordsY)
    file.write("{} {} {}\n".format(b,coordsX, coordsY)