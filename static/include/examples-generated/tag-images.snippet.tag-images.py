import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.media.video import ViamImage
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient
from grpclib.exceptions import GRPCError

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from
CLASSIFIER_NAME = ""  # the name of the classifier you want to use
BINARY_DATA_ID = ""  # the ID of the image you want to label


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
    viam_client = await connect()
    data_client = viam_client.data_client
    machine = await connect_machine()

    classifier = VisionClient.from_robot(machine, CLASSIFIER_NAME)

    # Get image from data in Viam
    data = await data_client.binary_data_by_ids([BINARY_DATA_ID])
    binary_data = data[0]

    # Convert binary data to ViamImage
    image = ViamImage(binary_data.binary, binary_data.metadata.capture_metadata.mime_type)

    # Get tags using the image
    tags = await classifier.get_classifications(image=image, image_format=binary_data.metadata.capture_metadata.mime_type, count=2)

    if not len(tags):
        print("No tags found")
        return 1
    else:
        for tag in tags:
            await data_client.add_tags_to_binary_data_by_ids(
                tags=[tag.class_name],
                binary_ids=[BINARY_DATA_ID]
            )
            print(f"Added tag to image: {tag}")

    viam_client.close()
    await machine.close()

    return 0

if __name__ == "__main__":
    asyncio.run(main())
