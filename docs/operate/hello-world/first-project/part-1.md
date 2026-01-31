---
linkTitle: "Part 1: Vision Pipeline"
title: "Part 1: Vision Pipeline"
weight: 10
layout: "docs"
type: "docs"
description: "Set up a camera, ML model, and vision service to detect defects."
date: "2025-01-30"
---

**Goal:** Get a working detection pipeline on one camera.

**Skills:** Connecting a machine to Viam, component configuration, adding services.

**Time:** ~15 min

## Prerequisites

Before starting this tutorial, you need the can inspection simulation running. Follow the **[Gazebo Simulation Setup Guide](../gazebo-setup/)** to:

1. Build the Docker image with Gazebo Harmonic
2. Create a machine in Viam and get credentials
3. Start the container with your Viam credentials

Once you see "Can Inspection Simulation Running!" in the container logs and your machine shows **Online** in the Viam app, return here to continue.

{{< alert title="What you're working with" color="info" >}}
The simulation runs Gazebo Harmonic inside a Docker container. It simulates a conveyor belt with cans (some dented) passing under an inspection camera. viam-server runs on the Linux vm inside the container and connects to Viam's cloud, just like it would on a physical machine. Everything you configure in the Viam app applies to the simulated hardware.
{{< /alert >}}

## 1.1 Verify Your Machine is Online

If you followed the [setup guide](../gazebo-setup/), your machine should already be online.

1. Open [app.viam.com](https://app.viam.com)
2. Navigate to your machine (for example, `inspection-station-1`)
3. Verify the status indicator shows **Live**
4. Click the **Configure** tab if not already selected

[SCREENSHOT: Machine page showing Online status]

Ordinarily, after creating a machine in Viam, you would download and install `viam-server` together with the cloud credentials for your machine. For this tutorial, we've have already installed `viam-server` and launched it in the simulation Docker container.

## 1.2 Locate Your Machine Part

Your machine is online but empty. To configure your machine you will add components and services to your machine part in the Viam user interface. Your machine part is the compute hardware for your robot. This might be a PC, Mac, Raspberry Pi, or another computer.

In the case of this tutorial, your machine part is a virtual machine running Linux in the Docker container.

Find `inspection-station-1-main` in the **Configuration** tab.

## 1.3 Configure the Camera

You'll now add the camera as a _component_.

{{< expand "What's a component?" >}}
In Viam, a **component** is any piece of hardware: cameras, motors, arms, sensors, grippers. You configure components by declaring what they are, and Viam handles the drivers and communication.

**The power of Viam's component model:** All cameras expose the same API—USB webcams, Raspberry Pi camera modules, IP cameras, simulated cameras. Your application code uses the same `GetImages()` method regardless of the underlying hardware. Swap hardware by changing configuration, not code.
{{< /expand >}}

### Add a camera component

To add components to a machine

1. Click the **+** button and select **Component or service**
2. Click **Camera**
3. Search for `gz-camera`
4. Select `gz-camera:rgb-camera`
5. Click **Add module**
6. Enter `inspection-cam` for the name

After adding the camera component, you will see two items appear in
[SCREENSHOT: Add component dialog with camera settings]

### Configure the camera

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

### Open the test panel

1. You should still be on the **Configure** tab with your `inspection-cam` selected
2. Look for the **Test** section at the bottom of the camera's configuration panel
3. Click **Toggle stream** to start the live feed

You should see a live video feed from the simulated camera—an overhead view of the conveyor/staging area.

[SCREENSHOT: Camera test panel showing live feed in Configure tab]

This pattern applies to all components. Motors have test controls for setting velocity. Arms have controls for moving joints. You can test any component directly from its configuration panel.

**Checkpoint:** Your camera is working. You can stream video and capture images from the simulated inspection station.

## 1.5 Add an ML Model Service

Now you'll add machine learning to your camera. You'll configure two services:

1. **ML model service** — Loads the trained model
2. **Vision service** — Connects the camera to the model and returns detections

{{< expand "Components versus services" >}}

- **Components** are hardware: cameras, motors, arms
- **Services** are capabilities: vision (ML inference), navigation (path planning), motion (arm kinematics)

Services often _use_ components. A **vision service** takes images from a camera, runs them through an ML model, and returns structured results—detections with bounding boxes and labels, or classifications with confidence scores.

The **ML model service** loads a trained model (TensorFlow, ONNX, or PyTorch) and exposes an `Infer()` method. The vision service handles the rest: converting camera images to tensors, calling the model, and interpreting outputs into usable detections.
{{< /expand >}}

### Create the ML model service

1. In the Viam app, click the **Configure** tab
2. Click **+** next to your machine in the left sidebar
3. Select **Service**, then **ML model**
4. Search for `TFLite CPU` and select it
5. Name it `can-classifier`
6. Click **Create**

[SCREENSHOT: Add service dialog for ML model]

### Select a model from the registry

1. In the `can-classifier` configuration panel, click **Select model**
2. Click the **Registry** tab
3. Search for `can-defect-detection` (a model we created for this tutorial that detects cans and classifies them as PASS or FAIL based on dent detection)
4. Select it from the list
5. Click **Save config**

[SCREENSHOT: Select model dialog showing registry models]

{{< alert title="Your own models" color="tip" >}}
For a different application, you'd train a model on your specific data and upload it to the registry. The registry handles versioning and deployment of ML models across your fleet.
{{< /alert >}}

## 1.6 Add a Vision Service

Now add a vision service that connects your camera to the ML model service.

### Create the vision service

1. Click **+** next to your machine
2. Select **Service**, then **Vision**
3. Search for `ML model` and select it
4. Name it `can-detector`
5. Click **Create**

### Link the vision service to the camera and model

1. In the `can-detector` configuration panel, find the **Default Camera** dropdown
2. Select `inspection-cam`
3. Find the **ML Model** dropdown
4. Select `can-classifier` (the ML model service you just created)
5. Click **Save config**

[SCREENSHOT: Vision service configuration linked to ML model]

### Test the vision service

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
