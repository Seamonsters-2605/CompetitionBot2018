import bpy, bmesh
import math

path = bpy.data.objects['NurbsPath']

obj = bpy.context.active_object

path.select = True
data = obj.data
bpy.context.scene.objects.active = path


for obj in bpy.data.objects:
    obj.select = False
Num = 0
with open("C:\\Users\PIROSKAZ000\Desktop\path.txt", "w") as file:
    for x in range(0,len(obj.data.vertices)):      
        print(len(obj.data.vertices))
        if obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
            vertices = bm.verts 
        else:
            vertices = obj.data.vertices
        verts = [obj.matrix_world * vert.co for vert in vertices] 
        plain_verts = [vert.to_tuple() for vert in verts]
        print(plain_verts)
        
        rotPoints = plain_verts[x-1]
        coords = plain_verts[x];coords1 = plain_verts[x]
        coordsX1 = rotPoints[0];coordsY1 = rotPoints[1]
        coordsX = coords[0];coordsY = coords[1]
        diffX = abs(coordsX-coordsX1);diffY = abs(coordsY-coordsY1)
        Theta = math.atan2((diffY+.001),(diffX+.001))
        
        file.write("{} {} {} {}\n".format(x*25,coordsX, coordsY, Theta))
  
