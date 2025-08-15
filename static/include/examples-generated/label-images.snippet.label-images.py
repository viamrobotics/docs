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
DETECTOR_NAME = ""  # the name of the detector you want to use
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

    detector = VisionClient.from_robot(machine, DETECTOR_NAME)

    # Get image from data in Viam
    data = await data_client.binary_data_by_ids([BINARY_DATA_ID])
    binary_data = data[0]

    # Convert binary data to ViamImage
    image = ViamImage(binary_data.binary, binary_data.metadata.capture_metadata.mime_type)

    # Get detections using the image
    detections = await detector.get_detections(
        image=image, image_format=binary_data.metadata.capture_metadata.mime_type)

    if not len(detections):
        print("No detections found")
        return 1
    else:
        for detection in detections:
            # Ensure bounding box is big enough to be useful
            if detection.x_max_normalized - detection.x_min_normalized <= 0.01 or \
                detection.y_max_normalized - detection.y_min_normalized <= 0.01:
                    continue
            bbox_id = await data_client.add_bounding_box_to_image_by_id(
                binary_id=BINARY_DATA_ID,
                label=detection.class_name,
                x_min_normalized=detection.x_min_normalized,
                y_min_normalized=detection.y_min_normalized,
                x_max_normalized=detection.x_max_normalized,
                y_max_normalized=detection.y_max_normalized
            )
            print(f"Added bounding box to image: {bbox_id}")

    viam_client.close()
    await machine.close()

    return 0

if __name__ == "__main__":
    asyncio.run(main())
