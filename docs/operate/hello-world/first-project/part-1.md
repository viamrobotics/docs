---
linkTitle: "Part 1: Vision Pipeline"
title: "Part 1: Vision Pipeline"
weight: 10
layout: "docs"
type: "docs"
description: "Set up a camera, ML model, and vision service to detect defects."
date: "2025-01-30"
---

**Goal:** Get a computer vision pipeline working.

**Skills:** Connect a machine to Viam, configure components in the Viam UI, configure services in the Viam UI.

**Time:** ~15 min

## Prerequisites

Before starting this tutorial, you need the can inspection simulation running. Follow the **[Gazebo Simulation Setup Guide](../gazebo-setup/)** to:

1. Build the Docker image with Gazebo Harmonic
2. Create a machine in Viam and get credentials
3. Start the container with your Viam credentials

Once you see "Can Inspection Simulation Running!" in the container logs and your machine shows **Online** in the Viam app, return here to continue.

{{< alert title="What you're working with" color="info" >}}
The simulation runs Gazebo Harmonic inside a Docker container. It simulates a conveyor belt with cans (some dented) passing under an inspection camera. viam-server runs on the Linux virtual machine inside the container and connects to Viam's cloud, just like it would on a physical machine. Everything you configure in the Viam app applies to the simulated hardware.
{{< /alert >}}

## 1.1 Verify Your Machine is Online

If you followed the [setup guide](../gazebo-setup/), your machine should already be online.

1. Open [app.viam.com](https://app.viam.com) (the "Viam app")
2. Navigate to your machine (for example, `inspection-station-1`)
3. Verify the status indicator shows **Live**
4. Click the **Configure** tab if not already selected

![Machine page showing the green Live status indicator next to the machine name.](/tutorials/first-project/machine-live-status.png)

Ordinarily, after creating a machine in Viam, you would download and install `viam-server` together with the cloud credentials for your machine. For this tutorial, we've already installed `viam-server` and launched it in the simulation Docker container.

## 1.2 Locate Your Machine Part

Your machine is online but empty. To configure your machine, you will add components and services to your machine part in the Viam app. Your machine part is the compute hardware for your robot. This might be a PC, Mac, Raspberry Pi, or another computer.

In the case of this tutorial, your machine part is a virtual machine running Linux in the Docker container.

Find `inspection-station-1-main` in the **Configuration** tab.

## 1.3 Configure the Camera

You'll now add the camera as a _component_.

{{< expand "What's a component?" >}}
In Viam, a **component** is any piece of hardware: cameras, motors, arms, sensors, grippers. You configure components by declaring what they are, and Viam handles the drivers and communication.

**The power of Viam's component model:** All cameras expose the same API—USB webcams, Raspberry Pi camera modules, IP cameras, simulated cameras. Your application code uses the same `GetImages()` method regardless of the underlying hardware. Swap hardware by changing configuration, not code.
{{< /expand >}}

### Add a camera component

To add the camera component to your machine part:

1. Click the **+** button and select **Component or service**
2. Click **Camera**
3. Search for `gz-camera`
4. Select `gz-camera:rgb-camera`
5. Click **Add module**
6. Enter `inspection-cam` for the name

{{< expand "Why were two items added to my machine part?" >}}
After adding the camera component, you will see two items appear under your machine part. One is the actual camera hardware (`inspection-cam`) that you will use through the Viam camera API. The other is the software module (`gz-camera`) that implements this API for the specific model of camera you are using. All components that are supported through modules available in the Viam registry will appear this way in the **Configuration** tab. For built-in components, such as webcams, you will not also see a module appear in the configuration.
{{< /expand >}}

### Configure the camera

To configure your camera component to work with the camera in the simulation, you need to specify the correct camera ID. Most components require a few configuration parameters.

1. In the **Attributes** section, add:

   ```json
   {
     "id": "/inspection_camera"
   }
   ```

2. Click **Save** in the top right

{{< alert title="What happened behind the scenes" color="info" >}}
You declared "this machine has a camera called `inspection-cam`" by editing the configuration in the Viam app. When you clicked **Save**, `viam-server` loaded the camera module, added a camera component, and made the camera available through Viam's standard camera API. Software you write, other services, and user interface components will use the API to get the images they need. Using the API as an abstraction means that everything still works if you swap cameras.
{{< /alert >}}

## 1.4 Test the Camera

Verify the camera is working. Every component in Viam has a built-in test card right in the configuration view.

### Open the test panel

1. You should still be on the **Configure** tab with your `inspection-cam` selected
2. Look for the **Test** section at the bottom of the camera's configuration panel
3. Click **Test** to expand the camera's test card

The camera component test card uses the camera API to add an image feed to the Viam app, enabling you to determine whether your camera is working. You should see a live video feed from the simulated camera. This is an overhead view of the conveyor/staging area.

{{< alert title="Checkpoint" color="success" >}}
Your camera is working. You can stream video and capture images from the simulated inspection station.
{{< /alert >}}

## 1.5 Add an ML Model Service

Now you'll add machine learning to run inference on your camera feed. You'll configure two services:

1. **ML model service**—Loads a trained model for the inference task
2. **Vision service**—Connects the camera to the model and returns detections

{{< expand "Components versus services" >}}

- **Components** are hardware: cameras, motors, arms
- **Services** are capabilities: vision (ML inference), motion (arm kinematics), custom control logic

Services often _use_ components. A **vision service** takes images from a camera, runs them through an ML model, and returns structured results—detections with bounding boxes and labels, or classifications with confidence scores.

The **ML model service** loads a trained model (TensorFlow, ONNX, or PyTorch) and exposes an `Infer()` method. The vision service handles the rest: converting camera images to tensors, calling the model, and interpreting outputs into usable detections.
{{< /expand >}}

### Create the ML model service

1. Click the **Configure** tab
2. Click **+** next to your machine part
3. Select **Component or service**
4. Select **ML model**
5. Select `TFLite CPU`
6. Click **Add module**
7. Name it `model-service`
8. Click **Create**

### Select a model from the registry

Configure the `model-service` ML model service you just included in your configuration.

1. In the `model-service` configuration panel, click **Select model**
2. Click the **Registry** tab
3. Search for `can-defect-detection` and select it from the list (a model that classifies cans as PASS or FAIL based on defect detection)
4. Click **Choose** to save the model selection
5. Click **Save** in the upper right corner to save your configuration

{{< alert title="Your own models" color="tip" >}}
For a different application, you'd train a model on your specific data and upload it to the registry. The registry handles versioning and deployment of ML models across your fleet.
{{< /alert >}}

## 1.6 Add a Vision Service

Now add a vision service that connects your camera to the ML model service.

### Create the vision service

1. Click **+** next to your machine part
2. Select **Component or service**
3. Search for `vision`
4. Select **vision / ML Model**
5. Name it `vision-service`
6. Click **Create**

### Link the camera and model in the vision service

1. Select the `vision-service` service in your machine's configuration
2. Find the **ML Model** dropdown and select `model-service` (the ML model service you just created)
3. Find the **Default Camera** dropdown and select `inspection-cam`
4. Find the **Attributes** section and set **Minimum confidence threshold** to 0.75
5. Click **Save** in the upper right corner

### Test the vision service

1. Find the **Test** section at the bottom of the `vision-service` configuration panel
2. Expand the **Test** card
3. If not already selected, select `inspection-cam` as the camera source
4. Set **Detections/Classifications** to `Live`
5. Check that detection and labeling are working

![Vision service test panel showing a can detected with a bounding box and FAIL label.](/tutorials/first-project/vision-service-test.png)

{{< alert title="What you've built" color="info" >}}
A complete ML inference pipeline. The vision service grabs an image from the camera, runs it through the TensorFlow Lite model, and returns structured detection results. This same pattern works for any ML task—object detection, classification, segmentation—you just swap the model.
{{< /alert >}}

{{< alert title="Checkpoint" color="success" >}}
You've configured a complete ML inference pipeline including a camera, model service, and vision service through the Viam app. The system can detect defective cans. Next, you'll set up continuous data capture so every detection is recorded and queryable.
{{< /alert >}}

{{< alert title="Explore the JSON configuration" color="tip" >}}
Everything you configured through the UI is stored as JSON. Click **JSON** in the upper left of the Configure tab to see the raw configuration. You'll see your camera, ML model service, and vision service defined with their attributes. As configurations grow more complex, the JSON view helps you understand how components and services connect.
{{< /alert >}}

**[Continue to Part 2: Data Capture →](../part-2/)**
