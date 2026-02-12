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

**Time:** ~10 min

## Prerequisites

Before starting this tutorial, you need the can inspection simulation running.
Follow the **[Gazebo Simulation Setup Guide](../gazebo-setup/)** to:

1. Build the Docker image with Gazebo Harmonic
2. Create a machine in Viam and get credentials
3. Start the container with your Viam credentials

Once you see "Can Inspection Simulation Running!" in the container logs and your machine shows **Live** in the Viam app, return here to continue.

{{< alert title="What you're working with" color="info" >}}
The simulation runs Gazebo Harmonic inside a Docker container.
It simulates a conveyor belt with cans (some dented) passing under an inspection camera.
viam-server runs on the Linux virtual machine inside the container and connects to Viam's cloud, just like it would on a physical machine.
Everything you configure in the Viam app applies to the simulated hardware.
{{< /alert >}}

## 1.1 Find Your Machine Part

In the Viam app, make sure the **Configure** tab for your machine is selected.

{{<imgproc src="/tutorials/first-project/machine-live-status.png" resize="x1100" declaredimensions=true alt="Machine page showing the green Live status indicator next to the machine name." class="imgzoom shadow">}}

Your machine is online but empty.
To configure it, you'll add components and services to your **machine part**.
A machine part is the compute hardware for your robot.
In this tutorial, your machine part is a virtual machine running Linux in the Docker container.

Find `inspection-station-1-main` in the **Configure** tab.

## 1.2 Configure the Camera

You'll now add the camera as a _component_.

{{< expand "What's a component?" >}}
In Viam, a **component** is any piece of hardware: cameras, motors, arms, sensors, grippers.
You configure components by declaring what they are, and Viam handles the drivers and communication.

**The power of Viam's component model:** All cameras expose the same API—USB webcams, Raspberry Pi camera modules, IP cameras, simulated cameras.
Your application code uses the same `GetImages()` method regardless of the underlying hardware.
Swap hardware by changing configuration, not code.
{{< /expand >}}

### Add a camera component

To add the camera component to your machine part:

1. Click the **+** button and select **Configuration block**
2. Search for `gz-camera`
3. Select `gz-camera:rgb-camera`
4. Click **Add component**
5. Enter `inspection-cam` for the name
6. Click **Add component**

{{<imgproc src="/tutorials/first-project/camera-config-panel.png" resize="x1100" declaredimensions=true alt="Camera configuration panel showing the inspection-cam component with JSON configuration section and documentation." class="imgzoom shadow">}}

### Configure the camera

To configure your camera component to work with the camera in the simulation, you need to specify the correct camera ID.
Most components require a few configuration parameters.

1. In the **JSON Configuration** section, add:

   ```json
   {
     "id": "/inspection_camera"
   }
   ```

2. Click **Save** in the top right

{{<imgproc src="/tutorials/first-project/camera-config-json.png" resize="x1100" declaredimensions=true alt="Camera configuration panel with the JSON configuration set to inspection_camera." class="imgzoom shadow">}}

{{< alert title="What happened behind the scenes" color="info" >}}
You declared "this machine has an attached camera called `inspection-cam`" by editing the configuration in the Viam app.
When you clicked **Save**, `viam-server` loaded the camera module which implements the camera API for the specific model of camera we are using.
It also added a camera component, and made the camera available through Viam's standard camera API.
Software you write, other services, and user interface components will use the API to get the images they need.
Using the API as an abstraction means that everything still works if you swap cameras.
{{< /alert >}}

## 1.3 Test the Camera

Verify the camera is working.
Every component in Viam has a built-in test card right in the configuration view.

### Open the test panel

1. You should still be on the **Configure** tab with your `inspection-cam` selected
2. Look for the **Test** section at the bottom of the camera's configuration panel
3. Click **Test** to expand the camera's test card

The camera component test card uses the camera API to add an image feed to the Viam app, enabling you to determine whether your camera is working.
You should see a live video feed from the simulated camera.
This is an overhead view of the conveyor/staging area.

{{<imgproc src="/tutorials/first-project/camera-test-panel.png" resize="x1100" declaredimensions=true alt="Camera test panel showing a live video feed from the simulated inspection camera." class="imgzoom shadow">}}

{{< alert title="Checkpoint" color="success" >}}
Your camera is working.
You can stream video and capture images from the simulated inspection station.
{{< /alert >}}

## 1.4 Add an ML Model Service

Now you'll add machine learning to run inference on your camera feed.
You'll configure two services:

- **ML model service**—Loads a trained model for the inference task
- **Vision service**—Connects the camera to the ML model and returns detections

### Create the ML model service

1. Click **+** next to your machine part
2. Select **Configuration block**
3. Search for `tflite`
4. Select `tflight_cpu/tflight_cpu`
5. Click **Add component**
6. Name it `model-service`
7. Click **Add component**

{{<imgproc src="/tutorials/first-project/model-service-config.png" resize="x1100" declaredimensions=true alt="ML model service configuration panel showing the model-service with Select model button and TFLite CPU module." class="imgzoom shadow">}}

### Select a model from the registry

Configure the `model-service` ML model service you just included in your configuration.

1. In the `model-service` configuration panel, click **Select model**
2. Search for `can-defect-detection` and select it from the list (a model that classifies cans as PASS or FAIL based on defect detection)

   {{<imgproc src="/tutorials/first-project/select-model-dialog.png" resize="x1100" declaredimensions=true alt="Select a model dialog showing the can-defect-detection model by Viam." class="imgzoom shadow">}}

3. Click **Choose** to save the model selection
4. Click **Save** in the upper right corner to save your configuration

{{< alert title="Your own models" color="tip" >}}
For a different application, you'd train a model on your specific data and upload it to the registry.
The registry handles versioning and deployment of ML models across your fleet.
{{< /alert >}}

## 1.5 Add a Vision Service

Now add a vision service that connects your camera to the ML model service.

### Create the vision service

1. Click **+** next to your machine part
2. Select **Configuration block**
3. Search for `vision`
4. Select **mlmodel**
5. Click **Add component**
6. Name it `vision-service`
7. Click **Add component**

{{<imgproc src="/tutorials/first-project/vision-service-created.png" resize="x1100" declaredimensions=true alt="Vision service configuration panel showing the newly created vision-service with empty ML Model and Default Camera dropdowns." class="imgzoom shadow">}}

### Link the camera and model in the vision service

1. Select the `vision-service` service in your machine's configuration
2. Find the **ML Model** dropdown and select `model-service` (the ML model service you just created)
3. Find the **Default Camera** dropdown and select `inspection-cam`
4. Find the **Attributes** section and set **Minimum confidence threshold** to 0.75
5. Click **Save** in the upper right corner

{{<imgproc src="/tutorials/first-project/vision-service-config.png" resize="x1100" declaredimensions=true alt="Vision service configuration panel showing ML Model set to model-service, Default Camera set to inspection-cam, and confidence threshold at 0.75." class="imgzoom shadow">}}

### Test the vision service

1. Find the **Test** section at the bottom of the `vision-service` configuration panel
2. Expand the **Test** card
3. If not already selected, select `inspection-cam` as the camera source
4. Set **Detections/Classifications** to `Live`
5. Check that detection and labeling are working

{{<imgproc src="/tutorials/first-project/vision-service-test.png" resize="x1100" declaredimensions=true alt="Vision service test panel showing a can detected with a bounding box and FAIL label." class="imgzoom shadow">}}

{{< alert title="Checkpoint" color="success" >}}
You've configured a complete ML inference pipeline that can detect defective cans.

The ML model service loads a trained model and exposes an `Infer()` method, while the vision service handles the rest—grabbing images from the camera, running them through the model, and returning structured detections with bounding boxes, labels, and confidence scores.

This pattern works for any ML task.
Swap the model for object detection, classification, or segmentation without changing the pipeline.
You can also swap one camera for another with one configuration change.

Next, you'll set up continuous data capture so every detection is recorded and queryable.
{{< /alert >}}

**[Continue to Part 2: Data Capture →](../part-2/)**
