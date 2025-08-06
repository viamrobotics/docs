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


    const pipelineId = await client.dataClient.createDataPipeline(
        ORG_ID,
        "test-pipeline",
        [
            { "$match": { "component_name": "temperature-sensor" } },
            { "$group": { "_id": "$location_id", "avg_temp": { "$avg": "$data.readings.temperature" }, "count": { "$sum": 1 } } },
            { "$project": { "location": "$_id", "avg_temp": 1, "count": 1 } }
        ],
        "0 * * * *",
        0,
        false,
    );

    console.log(`Pipeline created with ID: ${pipelineId}`);

}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
