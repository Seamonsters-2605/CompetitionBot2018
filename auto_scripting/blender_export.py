import bpy

FRAME_STEP = 25

scene = bpy.data.scenes['Scene']

robot_obj = bpy.data.objects['TheRobot']

with open("C:\\Temp\\Path.txt", "w") as file:
    for frame in range(scene.frame_start, scene.frame_end + FRAME_STEP, FRAME_STEP):
        scene.frame_current = frame
        bpy.ops.object.paths_calculate()
        # frame number, x, y
        line = "{} {} {}\n".format(frame, robot_obj.location[0], robot_obj.location[1])
        print(line)
        file.write(line)
