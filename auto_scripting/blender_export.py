import bpy

FRAME_STEP = 25

scene = bpy.data.scenes['Scene']

robot_obj = bpy.data.objects['TheRobot']
robot_path = bpy.data.curves('NurbsPath')
markers = sorted(scene.timeline_markers, key=lambda m: m.frame)
marker_i = 0
#set frame
dab = 0 #start pointe of curve. also keep marker_i and dab two different things.
#when increasing from 100 to x end the curve end always needs to stay as >= 1 or <=100
bpy.data.curves['NurbsPath'].eval_time = dab	#beggining of curve path thing

print(robot_obj.rotation_euler) #debugging

with open("C:\\Temp\\Path.txt", "w") as file:
    for frame in range(scene.frame_start, scene.frame_end + FRAME_STEP, FRAME_STEP):
        if marker_i < len(markers) and frame >= markers[marker_i].frame:
            file.write("{} {}\n".format(markers[marker_i].frame, ":" + markers[marker_i].name))
            bpy.data.curves['NurbsPath'].eval_time = dab
            marker_i += 1
            dab += 1            
        scene.frame_current = frame
        bpy.ops.object.paths_calculate()
        # frame number, x, y , z Rotation
        file.write("{} {} {} {} {}\n".format(frame, robot_obj.location[0], robot_obj.location[1] robot_obj.rotation_euler[2])
