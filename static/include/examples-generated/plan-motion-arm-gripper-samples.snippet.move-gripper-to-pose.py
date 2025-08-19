# This will move the gripper in the -Z direction with respect to its own
# reference frame
gripper_pose_rev = Pose(x=0.0,
                        y=0.0,
                        z=-50.0,
                        o_x=0.0,
                        o_y=0.0,
                        o_z=1.0,
                        theta=0.0)
# Note the change in frame name
gripper_pose_rev_in_frame = PoseInFrame(
    reference_frame=my_gripper_resource.name,
    pose=gripper_pose_rev)

await motion_service.move(component_name=my_gripper_resource,
                          destination=gripper_pose_rev_in_frame,
                          world_state=world_state)
