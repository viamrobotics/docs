// :snippet-start: pipeline-list
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // Organization ID, find or create in your organization settings
// :remove-start:
ORG_ID = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1";
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
    // :remove-end:

    const pipelines = await client.dataClient.listDataPipelines(ORG_ID);
    for (const pipeline of pipelines) {
        console.log(`Pipeline: ${pipeline.name}, ID: ${pipeline.id}, schedule: ${pipeline.schedule}, data_source_type: ${pipeline.dataSourceType}`);
    }
    // :remove-start:
    // Teardown - delete the pipeline
    await client.dataClient.deleteDataPipeline(pipelineId);
    console.log(`Pipeline deleted with ID: ${pipelineId}`);
    // :remove-end:
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: