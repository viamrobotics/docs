// :snippet-start: pipeline-execution
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let PIPELINE_ID = "";
// :remove-start:
let ORG_ID = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1";
API_KEY = process.env.VIAM_API_KEY_DATA_REGIONS || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID_DATA_REGIONS || "";
PIPELINE_ID = "16b8a3e5-7944-4e1c-8ccd-935c1ba3be59";
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

    const pipelineRuns = await client.dataClient.listDataPipelineRuns(PIPELINE_ID, 10);
    for (const run of pipelineRuns.runs) {
        console.log(
            `Run: ID: ${run.id}, status: ${run.status}, start_time: ${run.startTime}, ` +
            `end_time: ${run.endTime}, data_start_time: ${run.dataStartTime}, data_end_time: ${run.dataEndTime}`
        );
    }
    // :remove-start:
    if (pipelineRuns.runs.length !== 10) {
        throw new Error("Expected 10 runs, got " + pipelineRuns.runs.length);
    }
    // :remove-end:
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: