import { createViamClient, createRobotClient, RobotClient, VisionClient, CameraClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let DATASET_ID = "";  // the ID of the dataset you want to add the image to
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
let CLASSIFIER_NAME = "";  // the name of the classifier you want to use
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

    // Capture image
    const {images, metadata} = await camera.getImages();
    const imageFrame = images[0].image;

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

    return 0;
}

main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
