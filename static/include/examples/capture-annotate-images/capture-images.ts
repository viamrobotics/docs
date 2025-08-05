// :snippet-start: capture-images
import { createViamClient, createRobotClient, RobotClient, CameraClient } from "@viamrobotics/sdk";
// :remove-start:
import pkg from "@koush/wrtc";
const {
    RTCPeerConnection,
    RTCSessionDescription,
    RTCIceCandidate,
    MediaStream,
    MediaStreamTrack
} = pkg;

// Set up global WebRTC classes
global.RTCPeerConnection = RTCPeerConnection;
global.RTCSessionDescription = RTCSessionDescription;
global.RTCIceCandidate = RTCIceCandidate;
global.MediaStream = MediaStream;
global.MediaStreamTrack = MediaStreamTrack;
// :remove-end:

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
let CAMERA_NAME = "";  // the name of the camera you want to capture images from
let PART_ID = "";  // the part ID of the binary data you want to add to the dataset

// :remove-start:
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
CAMERA_NAME = "camera-1";
PART_ID = "824b6570-7b1d-4622-a19d-37c472dba467";
// :remove-end:

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

    // :remove-start:
    // Teardown - delete the image
    await dataClient.deleteBinaryDataByIds([fileId]);
    console.log(`Deleted image: ${fileId}`);

    // Force exit after cleanup to avoid hanging processes
    process.exit(0);
    // :remove-end:
    return 0;
}

// :remove-start:
// Run the script with timeout
const timeout = setTimeout(() => {
    console.log("Script timed out, forcing exit");
    process.exit(0);
}, 10000); // 5 second timeout
// :remove-end:

main().catch((error) => {
    // :remove-start:
    clearTimeout(timeout);
    // :remove-end:
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: