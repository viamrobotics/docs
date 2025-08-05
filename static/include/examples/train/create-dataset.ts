// :snippet-start: create-dataset
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // your organization ID, find in your organization settings
let DATASET_NAME = "";  // a unique, new name for the dataset you want to create

// :remove-start:
DATASET_NAME = "test-" + new Date().toISOString().replace(/[-:]/g, '').slice(0, 14);
ORG_ID = process.env.TEST_ORG_ID || "";
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
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

    console.log("Creating dataset...");
    try {
        const datasetId = await dataClient.createDataset(
            DATASET_NAME,
            ORG_ID
        );
        console.log(`Created dataset: ${datasetId}`);
        // :remove-start:
        // Teardown - delete the dataset
        await dataClient.deleteDataset(datasetId);
        console.log(`Deleted dataset: ${datasetId}`);
        // :remove-end:
    } catch (error) {
        console.log("Error creating dataset. It may already exist.");
        console.log("See: https://app.viam.com/data/datasets");
        console.log(`Exception: ${error}`);
        return 1;
    }

    return 0;
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: