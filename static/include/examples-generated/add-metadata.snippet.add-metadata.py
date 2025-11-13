import asyncio
import time

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.robot.client import RobotClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from


async def connect() -> ViamClient:
    """Establish a connection to the Viam client using API credentials."""
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def connect_machine() -> RobotClient:
    """Establish a connection to the robot using the robot address."""
    machine_opts = RobotClient.Options.with_api_key(
        api_key=API_KEY,
        api_key_id=API_KEY_ID
    )
    return await RobotClient.at_address(MACHINE_ADDRESS, machine_opts)

async def main() -> int:

    async with await connect_machine() as machine:
        machine_id = (await machine.get_cloud_metadata()).machine_id

    async with await connect() as viam_client:
        app_client = viam_client.app_client

        await app_client.update_robot_metadata(robot_id=machine_id, metadata={
            "TEST_API_KEY": "ABC123",
        })

        return 0

if __name__ == "__main__":
    asyncio.run(main())
