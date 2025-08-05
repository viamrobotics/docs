// :snippet-start: label-images
import { createViamClient, createRobotClient, RobotClient, VisionClient } from "@viamrobotics/sdk";
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
let DETECTOR_NAME = "";  // the name of the detector you want to use
let BINARY_DATA_ID = "";  // the ID of the image you want to label
// :remove-start:
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
DETECTOR_NAME = "detector-1";
BINARY_DATA_ID = "83da9642-3785-4db3-9d60-a3662a03bb04/cj53ft1jy1/fJFzEoxrv459YUxbH3gC9YNzgm8SfEjyLt70aNJbL1GxOovyU7gf69vQSCcMNNV5";
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
    const detector = new VisionClient(machine, DETECTOR_NAME);
    // :remove-start:
    // remove existing bounding boxes if present
    const data_remove = await dataClient.binaryDataByIds([BINARY_DATA_ID]);

    // Access the bounding boxes from the annotations
    if (data_remove[0].metadata.annotations?.bboxes) {
        for (const bbox of data_remove[0].metadata.annotations.bboxes) {
            await dataClient.removeBoundingBoxFromImageById(
                BINARY_DATA_ID,
                bbox.id
            );
            console.log(`Deleted bounding box: ${bbox.id}`);
        }
    }
    // :remove-end:

    // Get image from data in Viam
    const data = await dataClient.binaryDataByIds([BINARY_DATA_ID]);
    const binaryData = data[0];

    // Convert binary data to image
    const image = binaryData.binary; // This should be Uint8Array

    // Get detections using the image
    const detections = await detector.getDetections(
        image,
        binaryData.metadata.captureMetadata.width ?? 0,
        binaryData.metadata.captureMetadata.height ?? 0,
        binaryData.metadata.captureMetadata.mimeType ?? ""
    );

    if (detections.length === 0) {
        console.log("No detections found");
        return 1;
    } else {
        for (const detection of detections) {
            // Ensure bounding box is big enough to be useful
            if (detection.xMaxNormalized - detection.xMinNormalized <= 0.01 ||
                detection.yMaxNormalized - detection.yMinNormalized <= 0.01) {
                continue;
            }
            const bboxId = await dataClient.addBoundingBoxToImageById(
                BINARY_DATA_ID,
                detection.className,
                detection.xMinNormalized,
                detection.yMinNormalized,
                detection.xMaxNormalized,
                detection.yMaxNormalized
            );
            console.log(`Added bounding box to image: ${bboxId}`);
        }
    }

    // :remove-start:
    // Teardown - delete the bounding boxes
    const data3 = await dataClient.binaryDataByIds([BINARY_DATA_ID]);

    // Access the bounding boxes from the annotations
    if (data3[0].metadata.annotations?.bboxes) {
        for (const bbox of data3[0].metadata.annotations.bboxes) {
            await dataClient.removeBoundingBoxFromImageById(
                BINARY_DATA_ID,
                bbox.id
            );
            console.log(`Deleted bounding box: ${bbox.id}`);
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