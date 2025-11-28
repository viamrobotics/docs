import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let LOCATION_ID = "";  // the ID of the location you want to add metadata to

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
    const appClient = viamClient.appClient;
    await appClient.updateLocationMetadata(LOCATION_ID, {
        TEST_API_KEY: "ABC123",
    });

    return 0;
}

main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
