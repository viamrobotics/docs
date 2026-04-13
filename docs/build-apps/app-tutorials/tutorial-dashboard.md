---
linkTitle: "Tutorial: single-machine dashboard"
title: "Build a single-machine dashboard"
weight: 10
layout: "docs"
type: "docs"
description: "Build a TypeScript web dashboard for a single Viam machine. Displays a camera feed, a live sensor reading, and a motor control button, with a connection status indicator."
date: "2026-04-10"
---

In this tutorial, you will build a browser-based dashboard for a single Viam machine. The finished dashboard shows:

- A live camera feed
- The most recent reading from a sensor
- A start/stop button for a motor
- A connection status indicator

You will learn the four patterns that almost every Viam client app uses: opening a connection, reading state from a component, changing state on a component, and reacting to connection events. The dashboard runs locally in your browser by the end; deployment is out of scope for this tutorial.

The tutorial uses vanilla TypeScript and Vite without any frontend framework. The patterns work the same in React, Vue, or Svelte; a vanilla setup keeps the SDK calls visible without framework ceremony.

## What you need

- A configured Viam machine with a camera, a sensor, and a motor. Any models work. If you do not have the physical hardware, add fake components in the Viam app's **CONFIGURE** tab: `fake:camera`, `fake:sensor`, and `fake:motor`. The fake components respond to SDK calls the same way real ones do.
- A completed [TypeScript setup](../setup/typescript/). You should have a project directory with `@viamrobotics/sdk` installed, a `.env` file holding your machine credentials, and `index.html` plus `src/main.ts` files from the setup page.
- Two browser windows side by side, or two tabs you can switch between. One window runs your dashboard; the other opens the Viam app's **CONTROL** tab for the same machine so you can see server-side state change when your code runs.

Before continuing, confirm your setup by running `npx vite` and verifying that the page from the setup step shows `Connected. Found N resources.` in the browser. If it does not, go back to [TypeScript setup](../setup/typescript/) and fix the connection before continuing.

## Step 1: Replace the HTML

Open `index.html` and replace its contents with a layout that has slots for each piece of the dashboard:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My Viam Dashboard</title>
    <style>
      body {
        font-family: system-ui, sans-serif;
        padding: 1rem;
      }
      #status {
        font-weight: bold;
      }
      #status.connected {
        color: green;
      }
      #status.disconnected {
        color: red;
      }
      #camera {
        width: 640px;
        max-width: 100%;
        background: #222;
      }
      .panel {
        margin: 1rem 0;
        padding: 1rem;
        border: 1px solid #ccc;
      }
      button {
        padding: 0.5rem 1rem;
        font-size: 1rem;
      }
    </style>
  </head>
  <body>
    <h1>My Viam Dashboard</h1>
    <p>Status: <span id="status">Connecting...</span></p>

    <div class="panel">
      <h2>Camera</h2>
      <video id="camera" autoplay playsinline muted></video>
    </div>

    <div class="panel">
      <h2>Sensor readings</h2>
      <pre id="sensor">—</pre>
    </div>

    <div class="panel">
      <h2>Motor</h2>
      <button id="start">Start motor</button>
      <button id="stop">Stop motor</button>
    </div>

    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

Save the file. If Vite is still running, it reloads automatically. You should see the page layout in your browser with empty values and non-functional buttons.

## Step 2: Connect to your machine

Open `src/main.ts` and replace its contents with a connection that stores the machine client as a module-level variable. You will add the dashboard logic on top of this connection in the steps that follow.

```ts
import * as VIAM from "@viamrobotics/sdk";

const statusEl = document.getElementById("status") as HTMLSpanElement;
const cameraEl = document.getElementById("camera") as HTMLVideoElement;
const sensorEl = document.getElementById("sensor") as HTMLPreElement;
const startBtn = document.getElementById("start") as HTMLButtonElement;
const stopBtn = document.getElementById("stop") as HTMLButtonElement;

let machine: VIAM.RobotClient;

async function main() {
  machine = await VIAM.createRobotClient({
    host: import.meta.env.VITE_HOST,
    credentials: {
      type: "api-key",
      authEntity: import.meta.env.VITE_API_KEY_ID,
      payload: import.meta.env.VITE_API_KEY,
    },
    signalingAddress: "https://app.viam.com:443",
  });

  statusEl.textContent = "Connected";
  statusEl.className = "connected";
}

main().catch((err) => {
  statusEl.textContent = `Connection failed: ${err.message ?? err}`;
  statusEl.className = "disconnected";
});
```

Save the file. Refresh the browser. The status line should change from `Connecting...` to `Connected` in green. If it shows `Connection failed:`, check that your `.env` file has the right credentials and that your machine is online in the Viam app.

## Step 3: Display the camera feed

Add a camera stream to the dashboard. Use a `StreamClient` to attach the camera's WebRTC stream to the `<video>` element:

```ts
async function startCamera() {
  const streamClient = new VIAM.StreamClient(machine);
  const mediaStream = await streamClient.getStream("camera");
  cameraEl.srcObject = mediaStream;
}
```

Call `startCamera()` at the end of `main()`, after the connection is established:

```ts
async function main() {
  machine = await VIAM.createRobotClient({
    // ... (unchanged)
  });

  statusEl.textContent = "Connected";
  statusEl.className = "connected";

  await startCamera();
}
```

The string `"camera"` is the component name you gave the camera in your machine config. If you named it something else (like `my_webcam` or `fake_camera`), change the argument to match.

Save and refresh. The camera panel should now show a live feed. For a real camera, you will see the camera's image; for `fake:camera`, you will see a test pattern.

## Step 4: Poll the sensor

Sensors do not push data; you call `getReadings()` on a timer and display whatever you get back:

```ts
function startSensorPolling() {
  const sensor = new VIAM.SensorClient(machine, "sensor");

  setInterval(async () => {
    try {
      const readings = await sensor.getReadings();
      sensorEl.textContent = JSON.stringify(readings, null, 2);
    } catch (err) {
      sensorEl.textContent = `Error: ${err}`;
    }
  }, 1000);
}
```

Call `startSensorPolling()` after `startCamera()` in `main()`. Change the sensor name `"sensor"` if yours is configured differently.

Save and refresh. The sensor panel now updates every second with the current readings from your sensor. For `fake:sensor`, this is usually a single key like `"reading": 0.5` that changes over time. For a real sensor, you see whatever values the component exposes.

## Step 5: Control the motor

Wire the Start and Stop buttons to `motor.setPower(1)` and `motor.stop()`:

```ts
function wireMotorButtons() {
  const motor = new VIAM.MotorClient(machine, "motor");

  startBtn.addEventListener("click", async () => {
    try {
      await motor.setPower(1);
    } catch (err) {
      console.error("setPower failed:", err);
    }
  });

  stopBtn.addEventListener("click", async () => {
    try {
      await motor.stop();
    } catch (err) {
      console.error("stop failed:", err);
    }
  });
}
```

Call `wireMotorButtons()` after `startSensorPolling()` in `main()`. Change the motor name `"motor"` if yours is configured differently.

Save and refresh. Now open a second browser window to the Viam app's **CONTROL** tab for the same machine. Arrange the two windows side by side.

Click **Start motor** in your dashboard. In the Viam app's Control tab, the motor's power slider moves to 1 (full power). Click **Stop motor**. The slider returns to 0. You just made a server-side state change from your own app code, and you can see it reflected in another client watching the same machine.

For a `fake:motor`, the motor has no physical effect, but the state change is real. The same API call on a real motor would spin it at full power.

## Step 6: Add connection state handling

The dashboard is functional, but it does not react if the connection drops. Add a connection-state listener so the status indicator updates when the network changes:

```ts
function watchConnection() {
  machine.on("connectionstatechange", (event) => {
    const { eventType } = event as { eventType: VIAM.MachineConnectionEvent };
    switch (eventType) {
      case VIAM.MachineConnectionEvent.CONNECTED:
        statusEl.textContent = "Connected";
        statusEl.className = "connected";
        break;
      case VIAM.MachineConnectionEvent.DIALING:
      case VIAM.MachineConnectionEvent.CONNECTING:
        statusEl.textContent = "Connecting...";
        statusEl.className = "";
        break;
      case VIAM.MachineConnectionEvent.DISCONNECTING:
      case VIAM.MachineConnectionEvent.DISCONNECTED:
        statusEl.textContent = "Disconnected";
        statusEl.className = "disconnected";
        break;
    }
  });
}
```

Call `watchConnection()` at the end of `main()`, after the motor buttons are wired.

Save and refresh. The status indicator still says `Connected` on load. To test the state change, turn off your machine or disconnect your computer from the network briefly. The indicator switches to `Disconnected` (red). Restore connectivity and the SDK reconnects automatically, switching the indicator back to `Connected` (green). The camera stream may or may not resume on its own depending on how long the disconnection lasted; see [Handle disconnection and reconnection](../tasks/handle-connection-state/) for the rebuild-after-reconnect pattern.

## What you built

You now have a single-file TypeScript dashboard that:

- Opens a connection to a Viam machine at startup
- Displays a live camera feed
- Polls and displays sensor readings every second
- Controls a motor through start and stop buttons
- Reflects connection state in a status indicator

The full `src/main.ts` is around 80 lines of code. The four patterns you used (connect, read state, change state, react to events) cover almost every interactive Viam client app. When you build a larger app, you structure it around the same four operations, just with more components and a UI framework layered on top.

## Next steps

Extend the dashboard in one of these directions:

- **Auto-stop the motor when the sensor crosses a threshold.** In the sensor polling loop, check the reading's value and call `motor.stop()` when it exceeds a limit. This is the smallest useful control loop: reads drive writes. Combining observation with action is the core pattern of all robotics software.
- **Add a second camera.** Instantiate another `StreamClient.getStream("second_camera")` call and attach the result to a second `<video>` element. See [Stream video](../tasks/stream-video/) for the multi-camera section and its bandwidth caveats.
- **Rebuild state after reconnection.** The current dashboard does not re-attach the camera stream after a long disconnection. Follow [Handle disconnection and reconnection](../tasks/handle-connection-state/) to add the rebuild pattern.
- **Deploy the dashboard to Viam Applications.** Follow [Deploy a Viam application](../hosting/deploy/) to host the dashboard at a public URL with authentication and cookie-injected credentials. The code you wrote here works the same when deployed, except you read credentials from cookies instead of `import.meta.env`.
- **Build a multi-machine version.** See [the fleet tutorial](./tutorial-fleet/) for a dashboard that connects to the Viam cloud and aggregates data across several machines.
