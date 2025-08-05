import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // your organization ID, find in your organization settings
let DATASET_NAME = "";  // a unique, new name for the dataset you want to create


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
