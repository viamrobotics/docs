import asyncio
import numpy as np

from PIL import Image
from viam.components.camera import Camera
from viam.media.utils.pil import viam_to_pil_image
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from
CLASSIFIER_NAME = ""  # the name of the classifier you want to use
CAMERA_NAME = ""  # the name of the camera you want to capture images from


async def connect_machine() -> RobotClient:
    """Establish a connection to the robot using the robot address."""
    machine_opts = RobotClient.Options.with_api_key(
        api_key=API_KEY,
        api_key_id=API_KEY_ID
    )
    return await RobotClient.at_address(MACHINE_ADDRESS, machine_opts)

async def main() -> int:
    machine = await connect_machine()

    camera = Camera.from_robot(machine, CAMERA_NAME)
    classifier = VisionClient.from_robot(machine, CLASSIFIER_NAME)

    # Capture image
    images, _ = await camera.get_images(mime_type="image/jpeg")
    image_frame = images[0]

    # Get tags using the ViamImage (not the PIL image)
    tags = await classifier.get_classifications(
        image=image_frame, image_format="image/jpeg", count=2)

    await machine.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
