import { createViamClient, createRobotClient, RobotClient, VisionClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
let CLASSIFIER_NAME = "";  // the name of the classifier you want to use
let BINARY_DATA_ID = "";  // the ID of the image you want to label

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

    return 0;
}

main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
