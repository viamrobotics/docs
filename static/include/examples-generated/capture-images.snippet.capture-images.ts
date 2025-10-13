import { createViamClient, createRobotClient, RobotClient, CameraClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
let CAMERA_NAME = "";  // the name of the camera you want to capture images from
let PART_ID = "";  // the part ID of the machine part that captured the images


async function connect(): Promise<any> {
    // Establish a connection to the Viam client using API credentials
    return await createViamClient({
        credentials: {
            type: "api-key",
            authEntity: API_KEY_ID,
            payload: API_KEY,
        },
    });
}

async function connectMachine(): Promise<RobotClient> {
    // Establish a connection to the robot using the robot address
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
    const viamClient = await connect();
    const dataClient = viamClient.dataClient;
    const machine = await connectMachine();
    const camera = new CameraClient(machine, CAMERA_NAME);

    // Capture image
    const imageFrame = await camera.getImage();

    // Upload image
    const fileId = await dataClient.binaryDataCaptureUpload(
        imageFrame,
        PART_ID,
        "camera",
        CAMERA_NAME,
        "GetImage",
        ".jpg",
        [new Date(), new Date()]
    );
    console.log(`Uploaded image: ${fileId}`);

    return 0;
}


main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
