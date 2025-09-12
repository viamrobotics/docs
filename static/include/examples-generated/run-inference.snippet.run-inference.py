import asyncio
import numpy as np

from PIL import Image
from viam.components.camera import Camera
from viam.media.utils.pil import viam_to_pil_image
from viam.robot.client import RobotClient
from viam.services.mlmodel import MLModelClient

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
MACHINE_ADDRESS = ""  # the address of the machine you want to capture images from
ML_MODEL_NAME = ""  # the name of the ML model you want to use
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
    ml_model = MLModelClient.from_robot(machine, ML_MODEL_NAME)

    # Get ML model metadata to understand input requirements
    metadata = await ml_model.metadata()

    # Capture image
    image_frame = await camera.get_image()

    # Convert ViamImage to PIL Image first
    pil_image = viam_to_pil_image(image_frame)
    # Convert PIL Image to numpy array
    image_array = np.array(pil_image)

    # Get expected input shape from metadata
    expected_shape = list(metadata.input_info[0].shape)
    expected_dtype = metadata.input_info[0].data_type
    expected_name = metadata.input_info[0].name

    if not expected_shape:
        print("No input info found for 'image'")
        return 1

    if len(expected_shape) == 4 and expected_shape[0] == 1 and expected_shape[3] == 3:
        expected_height = expected_shape[1]
        expected_width = expected_shape[2]

        # Resize to expected dimensions
        if image_array.shape[:2] != (expected_height, expected_width):
            pil_image_resized = pil_image.resize((expected_width, expected_height))
            image_array = np.array(pil_image_resized)
    else:
        print(f"Unexpected input shape format.")
        return 1

    # Add batch dimension and ensure correct shape
    image_data = np.expand_dims(image_array, axis=0)

    # Ensure the data type matches expected type
    if expected_dtype == "uint8":
        image_data = image_data.astype(np.uint8)
    elif expected_dtype == "float32":
        # Convert to float32 and normalize to [0, 1] range
        image_data = image_data.astype(np.float32) / 255.0
    else:
        # Default to float32 with normalization
        image_data = image_data.astype(np.float32) / 255.0

    # Create the input tensors dictionary
    input_tensors = {
        expected_name: image_data
    }

    output_tensors = await ml_model.infer(input_tensors)
    print(f"Output tensors:")
    for key, value in output_tensors.items():
        print(f"{key}: shape={value.shape}, dtype={value.dtype}")

    await machine.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
