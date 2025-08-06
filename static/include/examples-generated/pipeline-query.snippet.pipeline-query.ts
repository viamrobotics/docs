import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // Organization ID, find or create in your organization settings
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

    const tabularData = await client.dataClient.tabularDataByMQL(
        ORG_ID,
        [
            { "$match": { "component_name": "sensor-1" } },
            { "$group": { "_id": "$location_id", "avg_val": { "$avg": "$data.readings.a" }, "count": { "$sum": 1 } } },
            { "$project": { "location": "$_id", "avg_val": 1, "count": 1 } }
        ],
        {
            tabularDataSourceType: 3,
            pipelineId: PIPELINE_ID,
        }
    );
    console.log(tabularData);
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
