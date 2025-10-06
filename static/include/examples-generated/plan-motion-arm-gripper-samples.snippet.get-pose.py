# Get the pose of myArm from the motion service
my_arm_motion_pose = await motion_service.get_pose(ARM_NAME,
                                                   "world")
print(f"Pose of myArm from the motion service: {my_arm_motion_pose}")
