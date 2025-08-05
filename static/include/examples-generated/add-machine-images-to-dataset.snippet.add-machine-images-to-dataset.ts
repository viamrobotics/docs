import { createViamClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let ORG_ID = "";  // your organization ID, find in your organization settings
let PART_ID = "";  // the part ID of the binary data you want to add to the dataset
let DATASET_ID = "";  // the ID of the dataset you want to add the image to
const MAX_MATCHES = 50;  // the maximum number of binary data objects to fetch

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

    await dataClient.addBinaryDataToDatasetByIds(
        matchingData.map(obj => obj.metadata.binaryDataId),
        DATASET_ID
    );

    console.log("Added files to dataset:");
    console.log(`https://app.viam.com/data/datasets?id=${DATASET_ID}`);

    return 0;
}

// Run the script
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
