---
linkTitle: "Create a web app"
title: "Create a web app"
weight: 10
layout: "docs"
type: "docs"
description: "Create a custom user interface for interacting with machines from a browser."
---

You can use Viam's [TypeScript SDK](https://ts.viam.dev/) to create a custom web application to interact with your devices.
The TypeScript SDK includes:

- Implementation of the standard component and service APIs to control your hardware and software
- Authentication tools so users can log in securely

{{< alert title="Tip: Host your application on Viam" color="tip" >}}
You can host most apps by [deploying them as Viam applications](/operate/control/viam-applications/).
If your application requires server-side rendering or other back-end functionality, self-host your application instead.
{{< /alert >}}

## Install the TypeScript SDK

Run the following command in your terminal to install the Viam TypeScript SDK:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
```

## Connect to your machine

You can find sample connection code on each [machine's](/operate/install/setup/) **CONNECT** tab.
Select **TypeScript** to display a code snippet, with connection code as well as some calls to the APIs of the resources you've configured on your machine.

You can use the toggle to include the machine API key and API key ID, though we strongly recommend storing your API keys in environment variables to reduce the risk of accidentally sharing your API key and granting access to your machines.

If your code will connect to multiple machines or use [Platform APIs](/dev/reference/apis/#platform-apis) you can create an API key with broader access.

## Write your app

Refer to the [Viam TypeScript SDK](https://ts.viam.dev/) documentation for available methods.

### Example: A camera and sensor dashboard

The following files create an example TypeScript web app that connects to a machine and displays the latest image from the machine's camera, and the latest sensor readings.

{{<imgproc src="/operate/ts-dashboard.png" resize="x1100" declaredimensions=true alt="A web browser displaying a dashboard with a camera feed and sensor readings." style="width:450px" class="imgzoom" >}}

{{< tabs >}}
{{% tab name="main.ts" %}}

<file>main.ts</file> connects to the machine and accesses the camera and sensor:

```ts {class="line-numbers linkable-line-numbers"}
// This code must be run in a browser environment.
import * as VIAM from "@viamrobotics/sdk";
import { CameraClient, SensorClient, StreamClient } from "@viamrobotics/sdk";

let isStreaming = false;
let camera: CameraClient;
let stream: StreamClient;
let animationFrameId: number;
let machine: VIAM.RobotClient;

const main = async () => {
  const host = "demo-main.abcdefg1234.viam.cloud";

  machine = await VIAM.createRobotClient({
    host,
    credentials: {
      type: "api-key",
      /* Replace "<API-KEY>" (including brackets) with your machine's API key */
      payload: "<API-KEY>",
      /* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
      authEntity: "<API-KEY-ID>",
    },
    signalingAddress: "https://app.viam.com:443",
  });

  try {
    // Get the camera and stream clients
    camera = new CameraClient(machine, "camera-1");

    // Start the camera stream
    startStream();

    // Get readings from sensor
    const sensor = new SensorClient(machine, "sensor-1");
    const readings = await sensor.getReadings();

    // Create HTML to display sensor readings
    const readingsHtml = document.createElement("div");
    for (const [key, value] of Object.entries(readings)) {
      const reading = document.createElement("p");
      reading.textContent = `${key}: ${value}`;
      readingsHtml.appendChild(reading);
    }

    // Display the readings
    const readingsContainer = document.getElementById("insert-readings");
    if (readingsContainer) {
      readingsContainer.innerHTML = "";
      readingsContainer.appendChild(readingsHtml);
    }

    // Add refresh button functionality
    const refreshButton = document.getElementById("refresh-button");
    if (refreshButton) {
      refreshButton.onclick = async () => {
        try {
          const newReadings = await sensor.getReadings();
          const readingsHtml = document.createElement("div");
          for (const [key, value] of Object.entries(newReadings)) {
            const reading = document.createElement("p");
            reading.textContent = `${key}: ${value}`;
            readingsHtml.appendChild(reading);
          }

          if (readingsContainer) {
            readingsContainer.innerHTML = "";
            readingsContainer.appendChild(readingsHtml);
          }
        } catch (error) {
          console.error("Error refreshing sensor data:", error);
        }
      };
    }
  } catch (error) {
    console.error("Error:", error);
    const errorMessage = `<p>Error: ${error instanceof Error ? error.message : "Failed to get data"}</p>`;

    const imageContainer = document.getElementById("insert-stream");
    if (imageContainer) {
      imageContainer.innerHTML = errorMessage;
    }

    const readingsContainer = document.getElementById("insert-readings");
    if (readingsContainer) {
      readingsContainer.innerHTML = errorMessage;
    }
  }

  // Add cleanup on page unload
  window.addEventListener("beforeunload", () => {
    stopStream();
    machine.disconnect();
  });
};

const updateCameraStream = async () => {
  if (!isStreaming) return;

  try {
    const imageContainer = document.getElementById("insert-stream");
    if (imageContainer) {
      // Create or update video element
      let videoElement = imageContainer.querySelector("video");
      if (!videoElement) {
        videoElement = document.createElement("video");
        videoElement.autoplay = true;
        videoElement.muted = true;
        imageContainer.innerHTML = "";
        imageContainer.appendChild(videoElement);
      }

      // Get and set the stream every frame
      const mediaStream = await stream.getStream("camera-1");
      videoElement.srcObject = mediaStream;

      // Ensure video plays
      try {
        await videoElement.play();
      } catch (playError) {
        console.error("Error playing video:", playError);
      }
    }

    // Request next frame
    animationFrameId = requestAnimationFrame(() => updateCameraStream());
  } catch (error) {
    console.error("Stream error:", error);
    stopStream();
  }
};

const startStream = () => {
  // Initialize stream client
  stream = new StreamClient(machine);
  isStreaming = true;
  updateCameraStream();
};

const stopStream = () => {
  isStreaming = false;
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
};

main().catch((error: unknown) => {
  console.error("encountered an error:", error);
});
```

{{% /tab %}}
{{% tab name="index.html" %}}

<file>static/index.html</file> defines the HTML structure of the web app:

```html {class="line-numbers linkable-line-numbers"}
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="style.css" />
  </head>

  <body>
    <div id="main">
      <div>
        <h1>My Dashboard</h1>
      </div>
      <script type="module" src="main.js"></script>
      <div>
        <h2>Camera Feed</h2>
        <p>Live view from the machine's camera:</p>
      </div>
      <div id="insert-stream">
        <p>
          <i
            >Loading stream... It may take a few moments for the stream to load.
            Do not refresh page.</i
          >
        </p>
      </div>
      <div>
        <h2>Sensor Data</h2>
        <p>Recent readings from the machine's sensor:</p>
      </div>
      <div id="insert-readings">
        <p>
          <i
            >Loading data... It may take a few moments for the data to load. Do
            not refresh page.</i
          >
        </p>
      </div>
      <br />
      <button id="refresh-button">Refresh Data</button>
    </div>
  </body>
</html>
```

{{% /tab %}}
{{% tab name="style.css" %}}

<file>static/style.css</file> defines the CSS styles for the web app:

```css {class="line-numbers linkable-line-numbers"}
body {
  margin: 0;
  padding: 0;
  background-color: #f0f2f5;
  font-family: "Segoe UI", Arial, sans-serif;
  color: #1a1a1a;
}

#main {
  max-width: 1200px;
  margin: 20px 20px;
  padding: 30px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 2.2em;
}

h2 {
  color: #34495e;
  margin-top: 30px;
  font-size: 1.5em;
}

div {
  background-color: transparent;
}

video {
  background: black;
  border-radius: 8px;
}

button#refresh-button {
  padding: 12px 24px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

button#refresh-button:hover {
  background-color: #45a049;
}

p {
  line-height: 1.6;
  color: #4a4a4a;
}
```

{{% /tab %}}
{{% tab name="package.json" %}}

<file>package.json</file> defines the dependencies and scripts for the web app:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-ts-dashboard",
  "description": "A dashboard for getting an image from a machine.",
  "scripts": {
    "start": "esbuild ./main.ts --bundle --outfile=static/main.js --servedir=static --format=esm",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "<YOUR NAME>",
  "license": "ISC",
  "devDependencies": {
    "esbuild": "*"
  },
  "dependencies": {
    "@viamrobotics/sdk": "^0.38.0",
    "bson": "^6.10.0"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

### More examples

For an example using Vite to connect to a machine, see [Viam's vanilla TypeScript quickstart example on GitHub](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples/vanilla).

The following tutorial uses the Viam TypeScript SDK to query data that has been uploaded to the Viam cloud from a sensor, and display it in a web dashboard.

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}

## Test your app

You can run your app directly on the machine's single-board computer (SBC) if applicable, or you can run it from a separate computer connected to the internet or to the same local network as your machine's SBC or microcontroller.
The connection code will establish communication with your machine over LAN or WAN.

You can also host your app on a server or hosting service of your choice.

## Set up user authentication through Viam

Viam uses [FusionAuth](https://fusionauth.io/) for authentication and authorization.

You can [use Viam to authenticate end users](/manage/manage/oauth/) while using a branded login screen.
