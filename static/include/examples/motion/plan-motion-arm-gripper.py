# :snippet-start: plan-motion-arm-gripper-full
import asyncio
# :remove-start:
import os
# :remove-end:

from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.proto.common import Geometry, GeometriesInFrame, Pose, PoseInFrame, \
    RectangularPrism, Vector3, WorldState
from viam.proto.component.arm import JointPositions
from viam.robot.client import RobotClient
from viam.services.motion import MotionClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from
ARM_NAME = ""  # the name of the arm you want to plan motion for
GRIPPER_NAME = ""  # the name of the gripper attached to the arm
# :remove-start:
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud"
ARM_NAME = "arm-1"
GRIPPER_NAME = "gripper-1"
# :remove-end:

async def connect_machine() -> RobotClient:
    """Establish a connection to the robot using the robot address."""
    machine_opts = RobotClient.Options.with_api_key(
        api_key=API_KEY,
        api_key_id=API_KEY_ID
    )
    return await RobotClient.at_address(MACHINE_ADDRESS, machine_opts)

async def main() -> int:
    machine_client = await connect_machine()

   # Access myArm
    my_arm_component = Arm.from_robot(machine_client, ARM_NAME)

    # End Position of myArm
    my_arm_end_position = await my_arm_component.get_end_position()
    print(f"myArm get_end_position return value: {my_arm_end_position}")

    # Joint Positions of myArm
    my_arm_joint_positions = await my_arm_component.get_joint_positions()
    print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")

    # :remove-start:
    cmd_joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 0])
    await my_arm_component.move_to_joint_positions(
        positions=cmd_joint_positions)
    # :remove-end:
    # Command a joint position move: move the forearm of the arm slightly up
    cmd_joint_positions = JointPositions(values=[0, 0, -30.0, 0, 0, 0])
    await my_arm_component.move_to_joint_positions(
        positions=cmd_joint_positions)

    # Generate a simple pose move +100mm in the +Z direction of the arm
    cmd_arm_pose = await my_arm_component.get_end_position()
    cmd_arm_pose.z += 100.0
    await my_arm_component.move_to_position(pose=cmd_arm_pose)

    # Access the motion service
    motion_service = MotionClient.from_robot(machine_client, "builtin")

    # Get the pose of myArm from the motion service
    my_arm_motion_pose = await motion_service.get_pose(ARM_NAME,
                                                       "world")
    print(f"Pose of myArm from the motion service: {my_arm_motion_pose}")

    # Add a table obstacle to a WorldState
    table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
    table_dims = Vector3(x=635.0, y=1271.0, z=38.0)
    table_object = Geometry(center=table_origin,
                            box=RectangularPrism(dims_mm=table_dims))

    obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                           geometries=[table_object])

    # Create a WorldState that has the GeometriesInFrame included
    world_state = WorldState(obstacles=[obstacles_in_frame])

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
        reference_frame=GRIPPER_NAME,
        pose=gripper_pose_rev)

    await motion_service.move(component_name=GRIPPER_NAME,
                              destination=gripper_pose_rev_in_frame,
                              world_state=world_state)

    # Don't forget to close the robot when you're done!
    await machine_client.close()

    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: