import bpy

FRAME_STEP = 25

scene = bpy.data.scenes['Scene']

robot_obj = bpy.data.objects['TheRobot']

markers = sorted(scene.timeline_markers, key=lambda m: m.frame)
marker_i = 0

with open("C:\\Temp\\Path.txt", "w") as file:
    for frame in range(scene.frame_start, scene.frame_end + FRAME_STEP, FRAME_STEP):
        if marker_i < len(markers) and frame >= markers[marker_i].frame:
            file.write("{} {}\n".format(markers[marker_i].frame, ":" + markers[marker_i].name))
            marker_i += 1
        scene.frame_current = frame
        bpy.ops.object.paths_calculate()
        # frame number, x, y
        file.write("{} {} {}\n".format(frame, robot_obj.location[0], robot_obj.location[1]))
