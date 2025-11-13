# :snippet-start: capture-images
import asyncio
# :remove-start:
import os
# :remove-end:

from datetime import datetime
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.components.camera import Camera
from viam.robot.client import RobotClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from
CAMERA_NAME = ""  # the name of the camera you want to capture images from
PART_ID = ""  # the part ID of the machine part that captured the images
# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud"
CAMERA_NAME = "camera-1"
PART_ID = "824b6570-7b1d-4622-a19d-37c472dba467"
# :remove-end:

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
    async with await connect_machine() as machine_client:
        camera = Camera.from_robot(machine_client, CAMERA_NAME)

        # Capture image
        images, _ = await camera.get_images()
        image_frame = images[0]

    async with await connect() as viam_client:
        data_client = viam_client.data_client

        # Upload image
        file_id = await data_client.binary_data_capture_upload(
            part_id=PART_ID,
            component_type="camera",
            component_name=CAMERA_NAME,
            method_name="GetImage",
            data_request_times=[datetime.utcnow(), datetime.utcnow()],
            file_extension=".jpg",
            binary_data=image_frame.data
        )
        print(f"Uploaded image: {file_id}")

        # :remove-start:
        # Teardown - delete the image
        await data_client.delete_binary_data_by_ids([file_id])
        print(f"Deleted image: {file_id}")
        # :remove-end:

        return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: