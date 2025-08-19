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

    const tabularDataMQL = await client.dataClient.tabularDataByMQL(
        ORG_ID,
        [
            { "$match": { "component_name": "sensor-1" } },
            { "$limit": 5 }
        ],
        false
    );
    console.log(tabularDataMQL);

    const tabularDataSQL = await client.dataClient.tabularDataBySQL(
        ORG_ID,
        "SELECT * FROM readings WHERE component_name = 'sensor-1' LIMIT 5"
    );
    console.log(tabularDataSQL);
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
