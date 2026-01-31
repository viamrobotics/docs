---
linkTitle: "Part 1: Vision Pipeline"
title: "Part 1: Vision Pipeline"
weight: 10
layout: "docs"
type: "docs"
description: "Set up a camera, ML model, and vision service to detect defects."
date: "2025-01-30"
---

**Goal:** Get a working detection pipeline on one simulated camera.

**Skills:** Connecting a machine to Viam, component configuration, adding services.

**Time:** ~15 min

## Prerequisites

Before starting this tutorial, you need the can inspection simulation running. Follow the **[Gazebo Simulation Setup Guide](../gazebo-setup/)** to:

1. Build the Docker image with Gazebo Harmonic
2. Create a machine in Viam and get credentials
3. Start the container with your Viam credentials

Once you see "Can Inspection Simulation Running!" in the container logs and your machine shows **Online** in the Viam app, return here to continue.

{{< alert title="What you're working with" color="info" >}}
The simulation runs Gazebo Harmonic inside a Docker container. It simulates a conveyor belt with cans (some dented) passing under an inspection camera. viam-server runs inside the container and connects to Viam's cloud, just like it would on a Raspberry Pi or any physical device. Everything you configure in the Viam app applies to the simulated hardware.
{{< /alert >}}

{{< alert title="Tip" color="tip" >}}
If you haven't already, open **http://localhost:8081** in your browser to see the simulation cameras. The overview camera shows the entire work cell, helping you understand what's happening as you work through the tutorial.
{{< /alert >}}

## 1.1 Understand viam-server

Every Viam-managed device runs **viam-server**—the software that connects your hardware to Viam's cloud. viam-server is the foundation of the platform:

- **Connects to the cloud** — Receives configuration updates, syncs data, enables remote access
- **Manages hardware** — Loads drivers for cameras, motors, sensors, and other components
- **Exposes APIs** — Provides a consistent interface for controlling any hardware
- **Runs modules** — Executes custom logic you deploy to the machine

On real hardware, installing viam-server is simple—a single command:

```bash
curl -fsSL https://app.viam.com/install | sh -s -- --apisecret <your-secret>
```

This downloads viam-server, configures it with credentials for your machine, and starts it as a background service. You'd run this on a Raspberry Pi, Jetson, or any Linux device.

**For this tutorial, we've done this for you.** The Docker container already has viam-server installed and running with your credentials. When you started the container with your config file mounted, viam-server connected automatically.

## 1.2 Verify Your Machine is Online

If you followed the [setup guide](../gazebo-setup/), your machine should already be online.

1. Open [app.viam.com](https://app.viam.com)
2. Navigate to your machine (e.g., `inspection-station-1`)
3. Verify the status indicator shows **Online** with a green dot

[SCREENSHOT: Machine page showing Online status]

This is the key moment: the Linux machine running in your Docker container is now connected to Viam's cloud. You can configure it, monitor it, and control it from anywhere in the world—exactly as you would with a physical device.

{{< expand "Troubleshooting" >}}

- **Still showing Offline?** Check the Docker container is running: `docker logs gz-viam`
- **Container not running?** Restart it: `docker start gz-viam`
- **Need to recreate?** Follow the [setup guide](../gazebo-setup/) again.
  {{< /expand >}}

## 1.3 Configure the Camera

Your machine is online but empty—it doesn't know about any hardware yet. You'll now add the camera as a _component_.

In Viam, a **component** is any piece of hardware: cameras, motors, arms, sensors, grippers. You configure components by declaring what they are, and Viam handles the drivers and communication.

**The power of Viam's component model:** All cameras expose the same API—USB webcams, Raspberry Pi camera modules, IP cameras, simulated cameras. Your application code uses the same `GetImage()` method regardless of the underlying hardware. Swap hardware by changing configuration, not code.

**Add the camera module:**

1. Click the **+** button and select **Module**
2. Search for `gz-camera` and select `viam:gz-camera`
3. Click **Add module**

**Add a camera component:**

1. Click the **+** button and select **Component**
2. For **Type**, select `camera`
3. For **Model**, select `viam:gz-camera:rgb-camera`
4. Name it `inspection-cam`
5. Click **Create**

[SCREENSHOT: Add component dialog with camera settings]

**Configure the camera:**

After creating the component, you'll see a configuration panel.

1. In the **Attributes** section, add:
   ```json
   {
     "id": "/inspection_camera"
   }
   ```
2. Click **Save** in the top right

[SCREENSHOT: Camera configuration panel with id attribute]

When you save, viam-server automatically reloads and applies the new configuration. You don't need to restart anything—the system picks up changes within seconds.

{{< alert title="What just happened" color="info" >}}
You declared "this machine has a camera called `inspection-cam`" by editing configuration in a web UI. Behind the scenes, viam-server loaded the camera module and made the camera available through Viam's standard camera API. The code you write in this tutorial will work identically with a $20 USB webcam or a $2,000 industrial camera—just change the model in your configuration.
{{< /alert >}}

## 1.4 Test the Camera

Let's verify the camera is working. Every component in Viam has a built-in test panel right in the configuration view.

**Open the test panel:**

1. You should still be on the **Configure** tab with your `inspection-cam` selected
2. Look for the **Test** section at the bottom of the camera's configuration panel
3. Click **Toggle stream** to start the live feed

You should see a live video feed from the simulated camera—an overhead view of the conveyor/staging area.

[SCREENSHOT: Camera test panel showing live feed in Configure tab]

**Capture an image:**

Click **Get image** to capture a single frame. The image appears in the panel and can be downloaded.

{{< alert title="What you're seeing" color="info" >}}
This isn't a special debugging view. The test panel uses the exact same APIs that your code will use. When you click "Get image," Viam calls the camera's `GetImage` method—the same method you'll call from Python or Go in a few minutes.
{{< /alert >}}

This pattern applies to all components. Motors have test controls for setting velocity. Arms have controls for moving joints. You can test any component directly from its configuration panel.

## 1.5 Add a Vision Service

Now you'll add machine learning to your camera. In Viam, ML capabilities are provided by _services_—higher-level functionality that operates on components.

**Components versus Services:**

- **Components** are hardware: cameras, motors, arms
- **Services** are capabilities: vision (ML inference), navigation (path planning), motion (arm kinematics)

Services often _use_ components. A **vision service** takes images from a camera, runs them through an ML model, and returns structured results—detections with bounding boxes and labels, or classifications with confidence scores. Your code calls the vision service API; the service handles everything else.

To work with ML models, the vision service needs an **ML model service**. The ML model service loads a trained model (TensorFlow, ONNX, or PyTorch) and exposes an `Infer()` method that takes input tensors and returns output tensors. The vision service handles the rest: converting camera images to the tensor format the model expects, calling the ML model service, and interpreting the raw tensor outputs into usable detections or classifications.

When using computer vision, as in this tutorial, you need to configure both: first the ML model service (which loads the model), then the vision service (which connects the camera to the model).

**Add the ML model service:**

The ML model service loads a trained model and makes it available for inference.

1. In the Viam app, click the **Configure** tab
2. Click **+** next to your machine in the left sidebar
3. Select **Service**, then **ML model**
4. Search for `TFLite CPU` and select it
5. Name it `can-classifier`
6. Click **Create**

[SCREENSHOT: Add service dialog for ML model]

**Select a model from the registry:**

1. In the `can-classifier` configuration panel, click **Select model**
2. Click the **Registry** tab
3. Search for `can-defect-detection` (a model we created for this tutorial that detects cans and classifies them as PASS or FAIL based on dent detection)
4. Select it from the list
5. Click **Save config**

[SCREENSHOT: Select model dialog showing registry models]

{{< alert title="Your own models" color="tip" >}}
For a different application, you'd train a model on your specific data and upload it to the registry. The registry handles versioning and deployment of ML models across your fleet.
{{< /alert >}}

**Add the vision service:**

Now add a vision service that connects your camera to the ML model service. The vision service captures images, sends them through the model, and returns detections you can use in your code.

1. Click **+** next to your machine
2. Select **Service**, then **Vision**
3. Search for `ML model` and select it
4. Name it `can-detector`
5. Click **Create**

**Link the vision service to the camera and model:**

1. In the `can-detector` configuration panel, find the **Default Camera** dropdown
2. Select `inspection-cam`
3. Find the **ML Model** dropdown
4. Select `can-classifier` (the ML model service you just created)
5. Click **Save config**

[SCREENSHOT: Vision service configuration linked to ML model]

**Test the vision service:**

1. You should still be on the **Configure** tab
2. Find the `can-detector` service you just created
3. Look for the **Test** section at the bottom of its configuration panel
4. If not already selected, select `inspection-cam` as the camera source
5. Click **Get detections**

You should see the camera image with detection results—bounding boxes around detected cans with labels (PASS or FAIL) and confidence scores.

[SCREENSHOT: Vision service test panel showing detection results with bounding boxes]

{{< alert title="What you've built" color="info" >}}
A complete ML inference pipeline. The vision service grabs an image from the camera, runs it through the TensorFlow Lite model, and returns structured detection results. This same pattern works for any ML task—object detection, classification, segmentation—you just swap the model.
{{< /alert >}}

**Checkpoint:** You've configured a complete ML inference pipeline—camera, model, and vision service—entirely through the Viam app. The system can detect dented cans. Next, you'll set up continuous data capture so every detection is recorded and queryable.

**[Continue to Part 2: Data Capture →](../part-2/)**
