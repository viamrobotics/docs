// :snippet-start: capture-annotate-dataset
import { createViamClient, createRobotClient, RobotClient, VisionClient, CameraClient } from "@viamrobotics/sdk";
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
let DATASET_ID = "";  // the ID of the dataset you want to add the image to
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
let CLASSIFIER_NAME = "";  // the name of the classifier you want to use
let CAMERA_NAME = "";  // the name of the camera you want to capture images from
let PART_ID = "";  // the part ID of the binary data you want to add to the dataset
// :remove-start:
let DATASET_NAME = "test-" + new Date().toISOString().replace(/[-:]/g, '').slice(0, 14);
let ORG_ID = process.env.TEST_ORG_ID || "";
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
CAMERA_NAME = "camera-1";
CLASSIFIER_NAME = "classifier-1";
PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77";
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
    const camera = new CameraClient(machine, CAMERA_NAME);
    const classifier = new VisionClient(machine, CLASSIFIER_NAME);
    // :remove-start:
    console.log("Creating dataset...");
    try {
        DATASET_ID = await dataClient.createDataset(
            DATASET_NAME,
            ORG_ID
        );
        console.log(`Created dataset: ${DATASET_ID}`);
    } catch (error) {
        console.log("Error creating dataset. It may already exist.");
        console.log("See: https://app.viam.com/data/datasets");
        console.log(`Exception: ${error}`);
        return 1;
    }
    // :remove-end:

    // Capture image
    const imageFrame = await camera.getImage();

    // Upload data
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

    // Annotate image
    await dataClient.addTagsToBinaryDataByIds(
        ["test"],
        [fileId]
    );

    // Get image from data in Viam
    const data = await dataClient.binaryDataByIds([fileId]);
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
    }

    for (const tag of tags) {
        await dataClient.addTagsToBinaryDataByIds(
            [tag.className ?? ""],
            [fileId]
        );
        console.log(`Added tag to image: ${tag}`);
    }

    console.log("Adding image to dataset...");
    await dataClient.addBinaryDataToDatasetByIds(
        [fileId],
        DATASET_ID
    );
    console.log(`Added image to dataset: ${fileId}`);

    // :remove-start:
    // Teardown - delete the tags
    const data3 = await dataClient.binaryDataByIds([fileId]);
    console.log(data3[0].metadata.annotations);

    // Access the classifications from the annotations
    if (data3[0].metadata.annotations?.classifications) {
        for (const tag of data3[0].metadata.annotations.classifications) {
            await dataClient.removeTagsFromBinaryDataByIds(
                [tag.label ?? ""],
                [fileId]
            );
            console.log(`Deleted tag: ${tag.label}`);
        }
    }

    // Teardown - delete the image
    await dataClient.deleteBinaryDataByIds([fileId]);
    console.log(`Deleted image: ${fileId}`);

    // Teardown - delete the dataset
    await dataClient.deleteDataset(DATASET_ID);
    console.log(`Deleted dataset: ${DATASET_ID}`);

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