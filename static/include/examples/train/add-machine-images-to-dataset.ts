// :snippet-start: add-machine-images-to-dataset
import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // your organization ID, find in your organization settings
let PART_ID = "";  // the part ID of the binary data you want to add to the dataset
let DATASET_ID = "";  // the ID of the dataset you want to add the image to
const MAX_MATCHES = 50;  // the maximum number of binary data objects to fetch
// :remove-start:
let DATASET_NAME = "test-" + new Date().toISOString().replace(/[-:]/g, '').slice(0, 14);
ORG_ID = process.env.TEST_ORG_ID || "";
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
PART_ID = "824b6570-7b1d-4622-a19d-37c472dba467";
// :remove-end:

async function connect(): Promise<any> {
    // Establish a connection to the Viam client using API credentials
    return await createViamClient({
        credentials: {
            type: "api-key",
            authEntity: API_KEY_ID,
            payload: API_KEY,
        },
    });
}

async function fetchBinaryDataIds(dataClient: any, partId: string): Promise<string[]> {
    /** Fetch binary data metadata and return a list of BinaryData objects. */
    const dataFilter = { partId: partId };
    const allMatches: any[] = [];
    let last: string | undefined = undefined;

    console.log("Getting data for part...");

    while (allMatches.length < MAX_MATCHES) {
        console.log("Fetching more data...");
        const result = await dataClient.binaryDataByFilter(
            dataFilter,
            50,
            0,
            last,
            false  // includeBinary = false to allow limit > 1
        );

        const data = result.data || result;
        const newLast = result.last;

        if (!data || data.length === 0) {
            break;
        }
        allMatches.push(...data);
        last = newLast;
    }

    return allMatches;
}

async function main(): Promise<number> {
    const viamClient = await connect();
    const dataClient = viamClient.dataClient;

    const matchingData = await fetchBinaryDataIds(dataClient, PART_ID);
    console.log(`Found ${matchingData.length} matching data objects`);
    console.log(matchingData);
    // :remove-start:
    console.log("Creating dataset...");
    try {
        DATASET_ID = await dataClient.createDataset(
            DATASET_NAME,
            ORG_ID
        );
        console.log(`Created dataset: ${DATASET_ID}`);
    } catch (error) {
        console.log("Error creating dataset. It may already exist.");
        console.log("See: https://app.viam.com/data/datasets");
        console.log(`Exception: ${error}`);
        return 1;
    }
    // :remove-end:

    await dataClient.addBinaryDataToDatasetByIds(
        matchingData.map(obj => obj.metadata.binaryDataId),
        DATASET_ID
    );

    console.log("Added files to dataset:");
    console.log(`https://app.viam.com/data/datasets?id=${DATASET_ID}`);

    // :remove-start:
    // Teardown - delete the dataset
    await dataClient.deleteDataset(DATASET_ID);
    console.log(`Deleted dataset: ${DATASET_ID}`);
    // :remove-end:
    return 0;
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: