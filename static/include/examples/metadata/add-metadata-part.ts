// :snippet-start: add-metadata-part
import { createViamClient } from "@viamrobotics/sdk";
// :remove-start:
import pkg from "@koush/wrtc";
const {
    RTCPeerConnection,
    RTCSessionDescription,
    RTCIceCandidate,
    MediaStream,
    MediaStreamTrack
} = pkg;

// Set up global WebRTC classes
global.RTCPeerConnection = RTCPeerConnection;
global.RTCSessionDescription = RTCSessionDescription;
global.RTCIceCandidate = RTCIceCandidate;
global.MediaStream = MediaStream;
global.MediaStreamTrack = MediaStreamTrack;
// :remove-end:

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let PART_ID = "";  // the ID of the machine part you want to add metadata to
// :remove-start:
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77";
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

async function main(): Promise<number> {
    const viamClient = await connect();
    const appClient = viamClient.appClient;
    await appClient.updateRobotPartMetadata(PART_ID, {
        TEST_API_KEY: "ABC123",
    });

    // :remove-start:
    const metadata = await appClient.getRobotPartMetadata(PART_ID);
    if (metadata.TEST_API_KEY !== "ABC123") {
        throw new Error("Metadata mismatch");
    }
    await appClient.updateRobotPartMetadata(PART_ID, {});
    const metadata2 = await appClient.getRobotPartMetadata(PART_ID);
    if (Object.keys(metadata2).length !== 0) {
        console.log(metadata2);
        throw new Error("Metadata should be {}");
    }
    // Force exit after cleanup
    process.exit(0);
    // :remove-end:
    return 0;
}

// :remove-start:
// Run the script with timeout
const timeout = setTimeout(() => {
    console.log("Script timed out, forcing exit");
    process.exit(1);
}, 20000); // 10 second timeout
// :remove-end:
main().catch((error) => {
    // :remove-start:
    clearTimeout(timeout);
    // :remove-end:
    console.error("Script failed:", error);
    process.exit(1);
});
// :snippet-end: