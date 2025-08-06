import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let PIPELINE_ID = "";

async function main(): Promise<void> {
    // Create Viam client
    const client = await createViamClient({
        credentials: {
            type: "api-key",
            authEntity: API_KEY_ID,
            payload: API_KEY,
        },
    });

    await client.dataClient.deleteDataPipeline(PIPELINE_ID);
    console.log(`Pipeline deleted with ID: ${PIPELINE_ID}`);
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
