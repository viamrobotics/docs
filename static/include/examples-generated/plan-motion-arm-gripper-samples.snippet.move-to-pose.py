# Generate a sample "start" pose to demonstrate motion
test_start_pose = Pose(x=510.0,
                       y=0.0,
                       z=526.0,
                       o_x=0.7071,
                       o_y=0.0,
                       o_z=-0.7071,
                       theta=0.0)
test_start_pose_in_frame = PoseInFrame(reference_frame="world",
                                       pose=test_start_pose)

await motion_service.move(component_name=ARM_NAME,
                          destination=test_start_pose_in_frame,
                          world_state=world_state)
