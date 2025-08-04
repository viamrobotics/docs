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

    // Check organization region
    const org = await client.appClient.getOrganization(ORG_ID);
    console.log(`Current region: ${org.defaultRegion}`);

    // Update organization region
    try {
        const updatedOrg = await client.appClient.updateOrganization(ORG_ID, "us-central");
        console.log(`Organization region updated to: ${updatedOrg?.defaultRegion}`);
    } catch (e) {
        console.log(`Error updating organization region: ${e}`);
    }
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
