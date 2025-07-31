# :snippet-start: capture-annotate-dataset
import asyncio
import time
# :remove-start:
import os
# :remove-end:

from datetime import datetime
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.components.camera import Camera
from viam.media.video import ViamImage
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
DATASET_ID = ""  # the ID of the dataset you want to add the image to
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from
CLASSIFIER_NAME = ""  # the name of the classifier you want to use
CAMERA_NAME = ""  # the name of the camera you want to capture images from
PART_ID = ""  # the part ID of the binary data you want to add to the dataset

# :remove-start:
DATASET_NAME = "test-" + time.strftime("%Y%m%d%H%M%S")
ORG_ID = os.environ["TEST_ORG_ID"]
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud"
CAMERA_NAME = "camera-1"
CLASSIFIER_NAME = "classifier-1"
PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77"
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
    viam_client = await connect()
    data_client = viam_client.data_client
    machine = await connect_machine()

    # :remove-start:
    print("Creating dataset...")
    try:
        DATASET_ID = await data_client.create_dataset(
            name=DATASET_NAME,
            organization_id=ORG_ID,
        )
        print(f"Created dataset: {DATASET_ID}")
    except Exception as e:
        print("Error creating dataset. It may already exist.")
        print("See: https://app.viam.com/data/datasets")
        print(f"Exception: {e}")
        return 1
    # :remove-end:
    camera = Camera.from_robot(machine, CAMERA_NAME)
    classifier = VisionClient.from_robot(machine, CLASSIFIER_NAME)

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

    # Annotate image
    await data_client.add_tags_to_binary_data_by_ids(
        tags=["test"],
        binary_ids=[file_id]
    )

    # Get image from data in Viam
    data = await data_client.binary_data_by_ids([file_id])
    binary_data = data[0]

    # Convert binary data to ViamImage
    image = ViamImage(binary_data.binary, binary_data.metadata.capture_metadata.mime_type)

    # Get tags using the image
    tags = await classifier.get_classifications(
        image=image, image_format=binary_data.metadata.capture_metadata.mime_type, count=2)

    if not len(tags):
        print("No tags found")
        return 1

    for tag in tags:
        await data_client.add_tags_to_binary_data_by_ids(
            tags=[tag.class_name],
            binary_ids=[file_id]
        )
        print(f"Added tag to image: {tag}")

    print("Adding image to dataset...")
    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=[file_id],
        dataset_id=DATASET_ID
    )
    print(f"Added image to dataset: {file_id}")

    # :remove-start:
    # Teardown - delete the tags
    data = await data_client.binary_data_by_ids([file_id])
    print(data[0].metadata.annotations)
    # Access the bounding boxes from the annotations
    if hasattr(data[0].metadata.annotations, 'classifications'):
        for tag in data[0].metadata.annotations.classifications:
            await data_client.remove_tags_from_binary_data_by_ids(
                binary_ids=[file_id],
                tags=[tag.label]
            )
            print(f"Deleted tag: {tag.label}")
    # Teardown - delete the image
    await data_client.delete_binary_data_by_ids([file_id])
    print(f"Deleted image: {file_id}")
    # Teardown - delete the dataset
    await data_client.delete_dataset(DATASET_ID)
    print(f"Deleted dataset: {DATASET_ID}")
    # :remove-end:
    viam_client.close()
    await machine.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
# :snippet-end: