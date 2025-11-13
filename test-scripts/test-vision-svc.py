import asyncio

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient
from viam.components.camera import Camera

API_KEY = ''
API_KEY_ID = ''
MACHINE_ADDRESS = ''

async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's api key
        api_key=API_KEY,
        # Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
        api_key_id=API_KEY_ID
    )
    return await RobotClient.at_address(MACHINE_ADDRESS, opts)

async def main():
    async with await connect() as machine:
        # detector
        vision_1 = VisionClient.from_robot(machine, "my_detector")
        vision_1_return_value = await vision_1.get_properties()
        print(f"my_detector get_properties return value: {vision_1_return_value}")

        camera_name = "cam"

        # Grab the detector you configured on your machine
        my_detector = VisionClient.from_robot(machine, "my_detector")
        # Get detections from the next image from the camera
        detections = await my_detector.get_detections_from_camera(camera_name)
        print(detections)


        # Grab camera from the machine
        cam1 = Camera.from_robot(machine, "cam")

        # Get the detector you configured on your machine
        my_detector = VisionClient.from_robot(machine, "my_detector")

        # Get an image from the camera
        images, _ = await cam1.get_images()
        img = images[0]

        # Get detections from that image
        detections = await my_detector.get_detections(img)

        # classifier
        vision_2 = VisionClient.from_robot(machine, "my_classifier")
        vision_2_return_value = await vision_2.get_properties()
        print(f"vision-1 get_properties return value: {vision_2_return_value}")

        # Grab the classifier you configured on your machine
        my_classifier = VisionClient.from_robot(machine, "my_classifier")

        # Get the 2 classifications with the highest confidence scores from the next image from the camera
        classifications = await my_classifier.get_classifications_from_camera(
            "cam", 2)
        print(classifications)

        # Grab camera from the machine
        cam1 = Camera.from_robot(machine, "camera-1")

        # Get the classifier you configured on your machine
        my_classifier = VisionClient.from_robot(machine, "my_classifier")

        # Get an image from the camera
        images, _ = await cam1.get_images()
        img = images[0]

        # Get the 2 classifications with the highest confidence scores
        classifications = await my_classifier.get_classifications(img, 2)

        # segmenter
        vision_3 = VisionClient.from_robot(machine, "my_segmenter")
        vision_3_return_value = await vision_2.get_properties()
        print(f"vision-3 get_properties return value: {vision_3_return_value}")

        import numpy as np
        import open3d as o3d

        # Grab the object segmenter you configured on your machine
        my_segmenter = VisionClient.from_robot(machine, "my_segmenter")
        # Get the objects from the camera output
        objects = await my_segmenter.get_object_point_clouds("cam")
        # write the first object point cloud into a temporary file
        with open("/tmp/pointcloud_data.pcd", "wb") as f:
            f.write(objects[0].point_cloud)
        pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
        points = np.asarray(pcd.points)

        # Grab the detector you configured on your machine
        my_detector = VisionClient.from_robot(machine, "my_detector")

        # capture all from the next image from the camera
        result = await my_detector.capture_all_from_camera(
            "cam",
            return_image=True,
            return_detections=True,
        )
        print(result.image)
        print(result.detections)


if __name__ == '__main__':
    asyncio.run(main())

