import { createRobotClient, RobotClient, VisionClient, CameraClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
let CLASSIFIER_NAME = "";  // the name of the classifier you want to use
let CAMERA_NAME = "";  // the name of the camera you want to capture images from

async function connectMachine(): Promise<RobotClient> {
    // Establish a connection to the robot using the machine address
    return await createRobotClient({
        host: MACHINE_ADDRESS,
        credentials: {
          type: 'api-key',
          payload: API_KEY,
          authEntity: API_KEY_ID,
        },
        signalingAddress: 'https://app.viam.com:443',
      });
}

async function main(): Promise<number> {
    const machine = await connectMachine();
    const camera = new CameraClient(machine, CAMERA_NAME);
    const classifier = new VisionClient(machine, CLASSIFIER_NAME);

    // Capture image
    const imageFrame = await camera.getImage();

    // Get tags using the image
    const tags = await classifier.getClassifications(
        imageFrame,
        imageFrame.width ?? 0,
        imageFrame.height ?? 0,
        imageFrame.mimeType ?? "",
        2
    );

    return 0;
}

main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
