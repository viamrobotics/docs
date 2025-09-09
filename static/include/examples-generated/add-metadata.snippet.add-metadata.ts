import { createViamClient, createRobotClient, RobotClient } from "@viamrobotics/sdk";

// Configuration constants – replace with your actual values
let API_KEY = "";  // API key, find or create in your organization settings
let API_KEY_ID = "";  // API key ID, find or create in your organization settings
let MACHINE_ADDRESS = "";  // the address of the machine you want to capture images from

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

    return 0;
}

main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
