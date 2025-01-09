import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions, dial
from viam.proto.common import Pose, PoseInFrame


async def connect(address) -> RobotClient:
    opts = RobotClient.Options(
        disable_sessions=False, dial_options=DialOptions(timeout=10)).with_api_key(
            api_key='<API-KEY>',
            api_key_id='<API-KEY-ID>'
        )
    return await RobotClient.at_address(address=address, options=opts)

async def main():
    # Make a RobotClient
    machine = await connect('<INSERT REMOTE ADDRESS FROM CONNECT TAB>')
    print('Resources:')
    print(machine.resource_names)

    operations = await machine.get_operations()
    print(operations)

    machine_status = await machine.get_machine_status()
    print(machine_status)
    resource_statuses = machine_status.resources
    print(resource_statuses)

    # BUG: can't test bc can't get operations from get_operations-- always prints empty array
    await machine.cancel_operation("INSERT OPERATION ID")
    await machine.block_for_operation("INSERT OPERATION ID")

    result = await machine.get_version()
    print(result.platform)
    print(result.version)
    print(result.api_version)

    frame_system = await machine.get_frame_system_config()
    print(f"frame system configuration: {frame_system}")

    pose = Pose(
        x=1.0,    
        y=2.0,    
        z=3.0,    
        o_x=0.0,  
        o_y=0.0,  
        o_z=0.0,  
        theta=0.0 
    )

    pose_in_frame = PoseInFrame(
        reference_frame="world",  # The reference frame in which this pose is expressed
        pose=pose                # The pose in that reference frame
    )

    pose = await machine.transform_pose(pose_in_frame, "world")

    statuses = await machine.get_status()
    print(statuses)

    await machine.stop_all()

    metadata = await machine.get_cloud_metadata()
    print(metadata.machine_id)
    print(metadata.machine_part_id)
    print(metadata.primary_org_id)
    print(metadata.location_id)

    await machine.refresh()
    await machine.shutdown()
    
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
