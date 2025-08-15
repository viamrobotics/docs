import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let DATASET_ID = "";  // the ID of the dataset you want to add the image to
let BINARY_DATA_ID = "";  // the ID of the image you want to add to the dataset

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


    console.log("Adding image to dataset...");
    await dataClient.addBinaryDataToDatasetByIds(
        [BINARY_DATA_ID],
        DATASET_ID
    );

    return 0;
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
