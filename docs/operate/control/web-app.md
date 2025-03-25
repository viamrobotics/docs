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

## Install the TypeScript SDK

Run the following command in your terminal to install the Viam TypeScript SDK:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
```

## Connect to your machine

You can find sample connection code on each [machine's](/operate/get-started/setup/) **CONNECT** tab in the [Viam app](https://app.viam.com).
Select **TypeScript** to display a code snippet, with connection code as well as some calls to the APIs of the resources you've configured on your machine.

You can use the toggle to include the machine API key and API key ID, though we strongly recommend storing your API keys in environment variables to reduce the risk of accidentally sharing your API key and granting access to your machines.

If your code will connect to multiple machines or use [Platform APIs](/dev/reference/apis/#platform-apis) you can create an API key with broader access.

## Write your app

Refer to the [Viam TypeScript SDK](https://ts.viam.dev/) documentation for available methods.

### Example usage

{{< expand "Example camera and sensor code" >}}

The following files are an example of a TypeScript web app that connects to a machine and displays the latest image from the machine's camera, and the latest sensor readings.

{{<imgproc src="/operate/ts-dashboard.png" resize="x1100" declaredimensions=true alt="A web browser displaying a dashboard with a camera feed and sensor readings." style="max-width:500px" class="imgzoom" >}}

<file>main.ts</file>:

```ts {class="line-numbers linkable-line-numbers"}
// This code must be run in a browser environment.
import * as VIAM from "@viamrobotics/sdk";
import { CameraClient, SensorClient } from "@viamrobotics/sdk";

const main = async () => {
  const host = "demo-main.abcdefg1234.viam.cloud";

  const machine = await VIAM.createRobotClient({
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
    // Get the camera
    const camera = new CameraClient(machine, "camera-1");

    // Get the sensor
    const sensor = new SensorClient(machine, "sensor-1");

    // Get image from camera
    const image = await camera.getImage();

    // Convert Uint8Array to base64
    const base64Image = btoa(
      Array.from(image)
        .map((byte) => String.fromCharCode(byte))
        .join(""),
    );

    // Convert image to base64 and display it
    const imageElement = document.createElement("img");
    imageElement.src = `data:image/jpeg;base64,${base64Image}`;
    const imageContainer = document.getElementById("insert-image");
    if (imageContainer) {
      imageContainer.innerHTML = "";
      imageContainer.appendChild(imageElement);
    }

    // Get readings from sensor
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
      refreshButton.onclick = main;
    }
  } catch (error) {
    console.error("Error:", error);
    const errorMessage = `<p>Error: ${error instanceof Error ? error.message : "Failed to get data"}</p>`;

    const imageContainer = document.getElementById("insert-image");
    if (imageContainer) {
      imageContainer.innerHTML = errorMessage;
    }

    const readingsContainer = document.getElementById("insert-readings");
    if (readingsContainer) {
      readingsContainer.innerHTML = errorMessage;
    }
  } finally {
    // Close the connection
    await machine.disconnect();
  }
};

main().catch((error: unknown) => {
  console.error("encountered an error:", error);
});
```

<file>static/index.html</file>:

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
        <p>Recent image from the machine's camera:</p>
      </div>
      <div id="insert-image">
        <p>
          <i
            >Loading image... It may take a few moments for the image to load.
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
      <p>
        Click the refresh button above to get the latest image and readings.
      </p>
    </div>
  </body>
</html>
```

<file>static/style.css</file>:

```css {class="line-numbers linkable-line-numbers"}
body {
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

div {
  background-color: rgb(218, 220, 221);
}

#main {
  max-width: 1200px auto;
  margin: 10px 10px auto;
  padding: 20px;
}

img {
  max-width: 100%;
  height: auto;
}

button#refresh-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button#refresh-button:hover {
  background-color: #0056b3;
}
```

<file>package.json</file>:

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

{{< /expand >}}

<br>

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
