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

    const pipelineRuns = await client.dataClient.listDataPipelineRuns(PIPELINE_ID, 10);
    for (const run of pipelineRuns.runs) {
        console.log(
            `Run: ID: ${run.id}, status: ${run.status}, start_time: ${run.startTime}, ` +
            `end_time: ${run.endTime}, data_start_time: ${run.dataStartTime}, data_end_time: ${run.dataEndTime}`
        );
    }
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
