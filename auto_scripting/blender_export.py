import bpy
#from setup import rotateWheels, 
FRAME_STEP = 25
#if rotateWheels = True:
#wheels_obj = bpy.data.objects['theWheels']
#else:
 #   wheels_obj = " "
scene = bpy.data.scenes['Scene']

robot_obj = bpy.data.objects['TheRobot']

robot_path = bpy.data.objects['NurbsPath']

markers = sorted(scene.timeline_markers, key=lambda m: m.frame)
marker_i = 0
#set frame
#pathTime = 0 #start pointe of curve. also keep marker_i and dab two different things.
#when increasing from 100 to x end the curve end always needs to stay as >= 1 or <=100
#bpy.data.objects['NurbsPath'].eval_time = pathTime	#beggining of curve path thing

print(robot_obj.rotation_euler) #debugging
robot_obj.select = True
robot_path.select = True
bpy.context.scene.objects.active = robot_obj
#bpy.ops.object.parent_set(type='FOLLOW_PATH')
empty = robot_obj.constraints.new('FOLLOW_PATH')
empty.target = robot_path
#robot_obj.constraints["FOLLOW_PATH"].use_curve_follow
K = robot_obj.constraints["Follow Path"] #or "FollowPathConstraint.use_curve_follow
K.offset = 10 #arbitrary amount it worked when i did ten so im using ten
K.influence = 0 #the new path time
for obj in bpy.data.objects:
    obj.select = False

with open("C:\\Users\**YOURNAME000***\Desktop\path.txt", "w") as file:
    for frame in range(scene.frame_start, scene.frame_end + FRAME_STEP, FRAME_STEP):
        bpy.ops.object.paths_calculate()
        if K.influence > 1:
            K.influence -=.1 #check. when path time is more than 100 increment it down to keep it at 100 which is the max value
        if marker_i < len(markers) and frame >= markers[marker_i].frame:
            file.write("{} {}\n".format(markers[marker_i].frame, ":" + markers[marker_i].name))
            marker_i += 1
            K.influence += .1  # change for sensitivity/ speed of robot          
        scene.frame_current = frame
        # frame number, x, y , z Rotation
        file.write("{} {} {} {}\n".format(frame, robot_obj.location[0], robot_obj.location[1], robot_obj.rotation_euler[2]))
        
