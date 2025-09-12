// :snippet-start: run-vision-service
import { createRobotClient, RobotClient, VisionClient, CameraClient } from "@viamrobotics/sdk";
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
let CLASSIFIER_NAME = "";  // the name of the classifier you want to use
let CAMERA_NAME = "";  // the name of the camera you want to capture images from
// :remove-start:
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
CAMERA_NAME = "camera-1";
CLASSIFIER_NAME = "classifier-1";
// :remove-end:

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

    // :remove-start:
    if (tags.length === 0) {
        console.log("No tags found");
        return 1;
    } else {
        for (const tag of tags) {
            console.log(`Found tag: ${tag.className}`);
        }
    }

    // Force exit after cleanup
    process.exit(0);
    // :remove-end:
    return 0;
}

// :remove-start:
// Run the script with timeout
const timeout = setTimeout(() => {
    console.log("Script timed out, forcing exit");
    process.exit(1);
}, 20000); // 10 second timeout
// :remove-end:
main().catch((error) => {
    // :remove-start:
    clearTimeout(timeout);
    // :remove-end:
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: