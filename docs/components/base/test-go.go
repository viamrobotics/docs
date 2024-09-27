import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions, dial
from viam.proto.common import Pose, PoseInFrame

from viam.proto.robot import DiscoveryQuery

# async def connect() -> RobotClient:
#     opts = RobotClient.Options.with_api_key(
#         # Replace "<API-KEY>" (including brackets) with your machine's API key
#         api_key='koynhlo9bbhio2x0buf662guu5c9vsna',
#         # Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
#         api_key_id='460d789f-3d13-48bc-b6f9-f995d6fb9b42',
#         dial_options = DialOptions(
#           timeout=10


async def connect(address) -> RobotClient:
    opts = RobotClient.Options(
        disable_sessions=True, dial_options=DialOptions(timeout=10)).with_api_key(
            api_key='koynhlo9bbhio2x0buf662guu5c9vsna',
            api_key_id='460d789f-3d13-48bc-b6f9-f995d6fb9b42'
        )
    return await RobotClient.at_address(address=address, options=opts)

# async def connect():

#     opts = RobotClient.Options.with_api_key(
#         # Replace "<API-KEY>" (including brackets) with your machine's API key
#         api_key='koynhlo9bbhio2x0buf662guu5c9vsna',
#         # Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
#         api_key_id='460d789f-3d13-48bc-b6f9-f995d6fb9b42'
#     )
#     return await RobotClient.at_address('cool-new-machine-main.0b2qnylnp0.viam.cloud', opts)


async def main():
    # Make a RobotClient
    machine = await connect()

async def main():
    # Make a RobotClient
    machine = await connect('cool-new-machine-main.0b2qnylnp0.viam.cloud')
    # machine = await connect()
    # print('Resources:')
    # print(machine.resource_names)


    operations = await machine.get_operations()
    print(operations)

    # BUG: unimplemented error: raise GRPCError(status, message, details)
    # grpclib.exceptions.GRPCError: (<Status.UNIMPLEMENTED: 12>, 'Unimplemented', None)
    machine_status = await machine.get_machine_status()
    print(machine_status)
    resource_statuses = machine_status.resources
    print(resource_statuses)

    # BUG: can't test bc can't get operations from get_operations-- always prints empty array
    # await machine.cancel_operation("INSERT OPERATION ID")
    # await machine.block_for_operation("INSERT OPERATION ID")

    #BUG: unimplemented error: raise GRPCError(status, message, details)
    # grpclib.exceptions.GRPCError: (<Status.UNIMPLEMENTED: 12>, 'Unimplemented', None)
    result = await machine.get_version()
    # print(result.platform)
    # print(result.version)
    # print(result.api_version)

    # Define a new discovery query.
    # q = DiscoveryQuery(subtype="camera", model="webcam")

    # # Define a list of discovery queries.
    # qs = [q]

    # # Get component configurations with these queries.
    # component_configs = await machine.discover_components(qs)
    # print(component_configs)

    # frame_system = await machine.get_frame_system_config()
    # print(f"frame system configuration: {frame_system}")

    # pose = Pose(
    #     x=1.0,    # X coordinate in meters
    #     y=2.0,    # Y coordinate in meters
    #     z=3.0,    # Z coordinate in meters
    #     o_x=0.0,  # Orientation quaternion X
    #     o_y=0.0,  # Orientation quaternion Y
    #     o_z=0.0,  # Orientation quaternion Z
    #     theta=0.0 # Orientation angle in radians
    # )

    # pose_in_frame = PoseInFrame(
    #     reference_frame="world",  # The reference frame in which this pose is expressed
    #     pose=pose                # The pose in that reference frame
    # )

    # pose = await machine.transform_pose(pose_in_frame, "world")

    # statuses = await machine.get_status()
    # print(statuses)

    # await machine.stop_all()

    # metadata = await machine.get_cloud_metadata()
    # print(metadata.machine_id)
    # print(metadata.machine_part_id)
    # print(metadata.primary_org_id)
    # print(metadata.location_id)

    # await machine.refresh()
    # await machine.shutdown()

    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())