# Get the pose of myArm from the motion service
my_arm_motion_pose = await motion_service.get_pose(my_arm_resource_name,
                                                   "world")
print(f"Pose of myArm from the motion service: {my_arm_motion_pose}")
