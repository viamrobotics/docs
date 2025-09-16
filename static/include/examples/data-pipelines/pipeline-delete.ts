// :snippet-start: pipeline-delete
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let PIPELINE_ID = "";
// :remove-start:
let ORG_ID = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1";
API_KEY = process.env.VIAM_API_KEY_DATA_REGIONS || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID_DATA_REGIONS || "";
// :remove-end:

async function main(): Promise<void> {
    // Create Viam client
    const client = await createViamClient({
        credentials: {
            type: "api-key",
            authEntity: API_KEY_ID,
            payload: API_KEY,
        },
    });

    // :remove-start:
    const pipelinesToDelete = await client.dataClient.listDataPipelines(ORG_ID);
    for (const pipeline of pipelinesToDelete) {
        await client.dataClient.deleteDataPipeline(pipeline.id);
        console.log(`Pipeline deleted with ID: ${pipeline.id}`);
    }

    PIPELINE_ID = await client.dataClient.createDataPipeline(
        ORG_ID,
        "test-pipeline",
        [
            { "$match": { "component_name": "temperature-sensor" } },
            { "$group": { "_id": "$location_id", "avg_temp": { "$avg": "$data.readings.temperature" }, "count": { "$sum": 1 } } },
            { "$project": { "location": "$_id", "avg_temp": 1, "count": 1, "_id": 0 } }
        ],
        "0 * * * *",
        false,
        0,
    );

    console.log(`Pipeline created with ID: ${PIPELINE_ID}`);
    // :remove-end:
    await client.dataClient.deleteDataPipeline(PIPELINE_ID);
    console.log(`Pipeline deleted with ID: ${PIPELINE_ID}`);
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: