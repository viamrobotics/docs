// :snippet-start: tag-images
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
let CLASSIFIER_NAME = "";  // the name of the classifier you want to use
let BINARY_DATA_ID = "";  // the ID of the image you want to label
// :remove-start:
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
CLASSIFIER_NAME = "classifier-1";
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
    const viamClient = await connect();
    const dataClient = viamClient.dataClient;
    const machine = await connectMachine();
    const classifier = new VisionClient(machine, CLASSIFIER_NAME);
    // :remove-start:
    // remove existing tags if present
    const data_remove = await dataClient.binaryDataByIds([BINARY_DATA_ID]);

    // Access the tags from the annotations
    if (data_remove[0].metadata.annotations?.tags) {
        for (const tag of data_remove[0].metadata.annotations.tags) {
            await dataClient.removeTagFromBinaryDataById(
                BINARY_DATA_ID,
                tag.id
            );
            console.log(`Deleted tag: ${tag.id}`);
        }
    }
    // :remove-end:

    // Get image from data in Viam
    const data = await dataClient.binaryDataByIds([BINARY_DATA_ID]);
    const binaryData = data[0];

    // Convert binary data to image
    const image = binaryData.binary; // This should be Uint8Array

    // Get tags using the image
    const tags = await classifier.getClassifications(
        image,
        binaryData.metadata.captureMetadata.width ?? 0,
        binaryData.metadata.captureMetadata.height ?? 0,
        binaryData.metadata.captureMetadata.mimeType ?? "",
        2
    );

    if (tags.length === 0) {
        console.log("No tags found");
        return 1;
    } else {
        for (const tag of tags) {
            await dataClient.addTagsToBinaryDataByIds(
                [tag.className ?? ""],
                [BINARY_DATA_ID]
            );
            console.log(`Added tag to image: ${tag.className}`);
        }
    }

    // :remove-start:
    // Teardown - delete the tags
    const data3 = await dataClient.binaryDataByIds([BINARY_DATA_ID]);
    console.log(data3[0].metadata.annotations);

    // Access the classifications from the annotations
    if (data3[0].metadata.annotations?.classifications) {
        for (const tag of data3[0].metadata.annotations.classifications) {
            await dataClient.removeTagsFromBinaryDataByIds(
                [tag.label ?? ""],
                [BINARY_DATA_ID]
            );
            console.log(`Deleted tag: ${tag.label}`);
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
}, 10000); // 10 second timeout
// :remove-end:
main().catch((error) => {
    // :remove-start:
    clearTimeout(timeout);
    // :remove-end:
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: