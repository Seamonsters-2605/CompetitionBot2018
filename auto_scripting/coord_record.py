import bpy, bmesh

robot_obj = bpy.data.objects['TheRobot']

#robot_path = bpy.data.objects['NurbsPath']

obj = bpy.context.active_object

robot_obj.select = True
data = obj.data
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
print( plain_verts)

for x in range(0,len(data.vertices)):
    coords = plain_verts[x]
    coordsX = coords[0]
    coordsY = coords[1]
    print(coordsX,coordsY)

with open("C:\\Users\TANALE000\Desktop\path.txt", "w") as file:
    file.write("{} {} {}\n".format(b,coordsX, coordsY))
    for x in range(0, len(data.vertices)):
        coords = plain_verts[x]
        coordsX = coords[0]
        coordsY = coords[1]
        file.write(f"\nCoords: {coordsX},{coordsY}")
