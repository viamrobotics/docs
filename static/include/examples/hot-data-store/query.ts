// :snippet-start: pipeline-query
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // Organization ID, find or create in your organization settings
// :remove-start:
ORG_ID = process.env.TEST_ORG_ID || "";
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
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

    const tabularData = await client.dataClient.tabularDataByMQL(
        ORG_ID,
        [
            { "$match": { "component_name": "sensor-1" } },
            { "$limit": 10 }
        ],
        {
            tabularDataSourceType: 2,
        }
    );
    console.log(tabularData);
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: