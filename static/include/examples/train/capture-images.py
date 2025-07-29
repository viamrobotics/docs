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
PART_ID = ""  # the part ID of the binary data you want to add to the dataset
CAMERA_NAME = ""  # the name of the camera you want to capture images from

# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud"
PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77"
CAMERA_NAME = "camera-1"

if not ORG_ID or not API_KEY or not API_KEY_ID:
    print("Environment variables not set")
    if ORG_ID:
        print("ORG_ID is set")
        print(ORG_ID)
    exit(1)
else:
    print(ORG_ID)

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
    """Main execution function."""
    viam_client = await connect()
    data_client = viam_client.data_client
    machine_client = await connect_machine()

    camera = Camera.from_robot(machine_client, CAMERA_NAME)

    # Capture image
    image_frame = await camera.get_image()

    # Upload data
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
    viam_client.close()
    await machine_client.close()

    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: