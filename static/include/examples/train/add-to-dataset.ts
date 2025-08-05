// :snippet-start: add-to-dataset
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let DATASET_ID = "";  // the ID of the dataset you want to add the image to
let BINARY_DATA_ID = "";  // the ID of the image you want to add to the dataset
// :remove-start:
let DATASET_NAME = "test-" + new Date().toISOString().replace(/[-:]/g, '').slice(0, 14);
let ORG_ID = process.env.TEST_ORG_ID || "";
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
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

async function main(): Promise<number> {
    const viamClient = await connect();
    const dataClient = viamClient.dataClient;

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

    console.log("Adding image to dataset...");
    await dataClient.addBinaryDataToDatasetByIds(
        [BINARY_DATA_ID],
        DATASET_ID
    );

    // :remove-start:
    // Teardown - delete the dataset
    await dataClient.deleteDataset(DATASET_ID);
    console.log(`Deleted dataset: ${DATASET_ID}`);
    // :remove-end:
    return 0;
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: