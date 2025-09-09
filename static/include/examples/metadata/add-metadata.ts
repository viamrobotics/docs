// :snippet-start: add-metadata
import { createViamClient, createRobotClient, RobotClient } from "@viamrobotics/sdk";
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
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from
// :remove-start:
API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
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

async function connectMachine(): Promise<RobotClient> {
    // Establish a connection to the robot using the machine address
    return await createRobotClient({
        host: MACHINE_ADDRESS,
        credentials: {
          type: 'api-key',
          payload: API_KEY,
          authEntity: API_KEY_ID,
        },
        signalingAddress: 'https://app.viam.com:443',
      });
}

async function main(): Promise<number> {
    const viamClient = await connect();
    const appClient = viamClient.appClient;
    const machine = await connectMachine();
    const machineId = (await machine.getCloudMetadata()).machineId;
    await appClient.updateRobotMetadata(machineId, {
        TEST_API_KEY: "ABC123",
    });

    // :remove-start:
    const metadata = await appClient.getRobotMetadata(machineId);
    if (metadata.TEST_API_KEY !== "ABC123") {
        throw new Error("Metadata mismatch");
    }
    await appClient.updateRobotMetadata(machineId, {});
    const metadata2 = await appClient.getRobotMetadata(machineId);
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