import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // Organization ID, find or create in your organization settings

async function main(): Promise<void> {
    // Create Viam client
    const client = await createViamClient({
        credentials: {
            type: "api-key",
            authEntity: API_KEY_ID,
            payload: API_KEY,
        },
    });


    const pipelines = await client.dataClient.listDataPipelines(ORG_ID);
    for (const pipeline of pipelines) {
        console.log(`Pipeline: ${pipeline.name}, ID: ${pipeline.id}, schedule: ${pipeline.schedule}, data_source_type: ${pipeline.dataSourceType}`);
    }

}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
