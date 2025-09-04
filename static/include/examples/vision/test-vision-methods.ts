import {
  createViamClient,
  createRobotClient,
  RobotClient,
  VisionClient,
  CameraClient,
} from "@viamrobotics/sdk";

import pkg from "@koush/wrtc";
const {
  RTCPeerConnection,
  RTCSessionDescription,
  RTCIceCandidate,
  MediaStream,
  MediaStreamTrack,
} = pkg;

// Set up global WebRTC classes
global.RTCPeerConnection = RTCPeerConnection;
global.RTCSessionDescription = RTCSessionDescription;
global.RTCIceCandidate = RTCIceCandidate;
global.MediaStream = MediaStream;
global.MediaStreamTrack = MediaStreamTrack;

// Configuration constants – replace with your actual values
let API_KEY = ""; // API key, find or create in your organization settings
let API_KEY_ID = ""; // API key ID, find or create in your organization settings
let MACHINE_ADDRESS = ""; // the address of the machine you want to capture images from
let CLASSIFIER_NAME = ""; // the name of the classifier you want to use
let DETECTOR_NAME = ""; // the name of the detector you want to use
let CAMERA_NAME = ""; // the name of the camera you want to capture images from
let PART_ID = ""; // the part ID of the binary data you want to add to the dataset

API_KEY = process.env.VIAM_API_KEY || "";
API_KEY_ID = process.env.VIAM_API_KEY_ID || "";
MACHINE_ADDRESS = "auto-machine-main.pg5q3j3h95.viam.cloud";
CAMERA_NAME = "camera-1";
CLASSIFIER_NAME = "classifier-1";
DETECTOR_NAME = "detector-1";
PART_ID = "deb8782c-7b48-4d35-812d-2caa94b61f77";

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
      type: "api-key",
      payload: API_KEY,
      authEntity: API_KEY_ID,
    },
    signalingAddress: "https://app.viam.com:443",
  });
}

async function main(): Promise<number> {
  const machine = await connectMachine();
  const camera = new CameraClient(machine, CAMERA_NAME);
  const classifier = new VisionClient(machine, CLASSIFIER_NAME);
  const detector = new VisionClient(machine, DETECTOR_NAME);
  const vision = new VisionClient(machine, "vision-1");

  // resource name
  console.log("resource name");
  console.log(vision.name);
  if (vision.name !== "vision-1") {
    throw new Error("vision-1 is not the name of the vision service");
  }

  // resource properties
  console.log("resource properties");
  let properties = await vision.getProperties();
  console.log(properties);
  if (properties["detectionsSupported"] !== true) {
    throw new Error("detectionsSupported is not true");
  }
  if (properties["classificationsSupported"] !== true) {
    throw new Error("classifications_supported is not true");
  }
  if (properties["objectPointCloudsSupported"] !== false) {
    throw new Error("objectPointClouds_supported is not false");
  }

  // capture all from camera
  console.log("capture all from classifier");
  let captureAll = await vision.captureAllFromCamera(CAMERA_NAME, {
    returnImage: true,
    returnDetections: true,
    returnClassifications: true,
    returnObjectPointClouds: true,
  });
  console.log(captureAll);
  if (!captureAll) {
    throw new Error("captureAll is empty");
  }

  // get detections from camera
  let detections1 = await vision.getDetectionsFromCamera(CAMERA_NAME);
  console.log("detections from camera");
  console.log(detections1);
  if (!detections1) {
    throw new Error("detections1 is empty");
  }

  // get detections
  let imageFrame = await camera.getImage();
  console.log(imageFrame);
  console.log("detections from image");
  let detections2 = await vision.getDetections(
    imageFrame,
    600,
    600,
    "image/jpeg",
  );
  console.log(detections2);
  if (!detections2) {
    throw new Error("detections2 is empty");
  }

  // get classifications
  let classifications1 = await vision.getClassificationsFromCamera(
    CAMERA_NAME,
    2,
  );
  console.log("classifications from camera");
  console.log(classifications1);

  if (!classifications1) {
    throw new Error("classifications1 is empty");
  }

  // get classifications from image
  console.log("classifications from image");
  let classifications2 = await vision.getClassifications(
    imageFrame,
    600,
    600,
    "image/jpeg",
    2,
  );
  console.log(classifications2);

  if (!classifications2) {
    throw new Error("classifications2 is empty");
  }

  // get object point clouds
  // console.log("object point clouds from camera");
  // let objectPointClouds = await vision.getObjectPointClouds(CAMERA_NAME);
  // console.log(objectPointClouds);

  process.exit(0);
  return 0;
}

// Run the script with timeout
const timeout = setTimeout(() => {
  console.log("Script timed out, forcing exit");
  process.exit(1);
}, 20000); // 10 second timeout
main().catch((error) => {
  clearTimeout(timeout);
  console.error("Script failed:", error);
  process.exit(1);
});
