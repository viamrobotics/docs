---
linkTitle: "Part 1: Vision Pipeline"
title: "Part 1: Vision Pipeline"
weight: 10
layout: "docs"
type: "docs"
description: "Set up a camera, ML model, and vision service to detect defects."
date: "2025-01-30"
aliases:
  - /operate/hello-world/first-project/part-1/
  - /try/first-project/part-1/
---

**Goal:** Get a computer vision pipeline working.

**Skills:** Connect a machine to Viam, configure components with the Viam CLI, use fragments to add preconfigured services.

**Time:** ~10 min

## Prerequisites

Before starting this tutorial, you need the can inspection simulation running. Follow the **[Gazebo Simulation Setup Guide](../gazebo-setup/)** to:

1. Build the Docker image with Gazebo Harmonic
2. Create a machine in Viam and get credentials
3. Start the container with your Viam credentials

Once you see "Can Inspection Simulation Running!" in the container logs and your machine shows **Live** in the Viam app, return here to continue.

You also need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.

{{< alert title="What you're working with" color="info" >}}
The simulation runs Gazebo Harmonic inside a Docker container. It simulates a conveyor belt with cans (some dented) passing under an inspection camera. viam-server runs on the Linux virtual machine inside the container and connects to Viam's cloud, just like it would on a physical machine. Everything you configure applies to the simulated hardware.
{{< /alert >}}

## 1.1 Verify Your Machine is Online

If you followed the [setup guide](../gazebo-setup/), your machine should already be online.

Run:

```sh {class="command-line" data-prompt="$"}
viam machines status --machine=<machine-id>
```

Look for `status: live` in the output. If your machine isn't live yet, check that the Docker container is running and that the logs show "Can Inspection Simulation Running!".

Ordinarily, after creating a machine in Viam, you would download and install `viam-server` together with the cloud credentials for your machine. For this tutorial, we've already installed `viam-server` and launched it in the simulation Docker container.

## 1.2 Get Your Part ID

Your machine is online but empty. To configure your machine, you will add components and services to your machine part. Your machine part is the compute hardware — in this tutorial, a virtual machine running Linux in the Docker container.

Get the part ID for `inspection-station-1-main`:

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine=<machine-id>
```

Copy the part ID from the output. You'll use it in every command that follows.

## 1.3 Configure the Camera

You'll now add the camera as a _component_.

{{< expand "What's a component?" >}}
In Viam, a **component** is any piece of hardware: cameras, motors, arms, sensors, grippers. You configure components by declaring what they are, and Viam handles the drivers and communication.

**The power of Viam's component model:** All cameras expose the same API—USB webcams, Raspberry Pi camera modules, IP cameras, simulated cameras. Your application code uses the same `GetImages()` method regardless of the underlying hardware. Swap hardware by changing configuration, not code.
{{< /expand >}}

### Add a camera component

Add the `gz-camera` module's `rgb-camera` model and name it `inspection-cam`:

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource \
  --part=<part-id> \
  --name=inspection-cam \
  --model-name=gz-camera:gz-camera:rgb-camera
```

{{< expand "Why does the model triplet have three parts?" >}}
The model triplet format is `namespace:module-name:model-name`. Here, `gz-camera` is both the namespace and module name, and `rgb-camera` is the specific model within that module. The module (`gz-camera`) is what implements the Viam camera API for this simulated hardware. When you add a component that comes from a registry module, `viam-server` downloads and runs the module automatically.
{{< /expand >}}

### Configure the camera

Set the camera ID so the module knows which Gazebo camera to connect to:

```sh {class="command-line" data-prompt="$"}
viam resource update \
  --part=<part-id> \
  --resource-name=inspection-cam \
  --config '{"id": "/inspection_camera"}'
```

{{< alert title="What happened behind the scenes" color="info" >}}
You declared "this machine has a camera called `inspection-cam`" by running two CLI commands. `viam-server` picks up configuration changes immediately — no restart needed. It loaded the camera module, added the camera component, and made it available through Viam's standard camera API. Software you write, other services, and UI components all use the same API. Using the API as an abstraction means everything still works if you swap cameras.
{{< /alert >}}

## 1.4 Test the Camera

The easiest way to verify the camera is working is to use the Viam app's built-in test panel, which shows a live video feed.

1. Open [app.viam.com](https://app.viam.com) and navigate to your machine
2. Click the **CONFIGURE** tab and select `inspection-cam`
3. Expand the **TEST** section at the bottom of the camera's configuration panel

You should see a live overhead view of the conveyor/staging area.

{{< alert title="Checkpoint" color="success" >}}
Your camera is working. You can stream video and capture images from the simulated inspection station.
{{< /alert >}}

## 1.5 Add a vision pipeline with a fragment

Now you'll add machine learning to run inference on your camera feed. You need two services:

1. **ML model service** that loads a trained model for the inference task
2. **Vision service** that connects the camera to the model and returns detections

{{< expand "Components versus services" >}}

- **Components** are hardware: cameras, motors, arms
- **Services** are capabilities: vision (ML inference), motion (arm kinematics), custom control logic

Services often _use_ components. A **vision service** takes images from a camera, runs them through an ML model, and returns structured results, detections with bounding boxes and labels, or classifications with confidence scores.

The **ML model service** loads a trained model (TensorFlow, ONNX, or PyTorch) and exposes an `Infer()` method. The vision service handles the rest: converting camera images to tensors, calling the model, and interpreting outputs into usable detections.
{{< /expand >}}

Instead of adding each service manually, you'll use a **fragment**. A fragment is a reusable block of configuration that can include components, services, modules, and ML models. Fragments let you share tested configurations across machines and teams.

The `try-vision-pipeline` fragment includes an ML model service loaded with a can defect detection model and a vision service wired to that model. The fragment accepts a `camera_name` variable so it works with any camera.

### Add the fragment

Apply the `try-vision-pipeline` fragment to your machine part:

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add \
  --part=<part-id> \
  --fragment=<try-vision-pipeline-fragment-id>
```

{{< expand "How do I find the fragment ID?" >}}
You can find the fragment ID in the [Viam registry](https://app.viam.com/registry) by searching for `try-vision-pipeline` and copying the ID from the fragment's detail page.
{{< /expand >}}

### Set the camera variable

The fragment uses a `camera_name` variable to wire the vision service to your specific camera. Set it in the machine's JSON configuration:

```sh {class="command-line" data-prompt="$"}
viam machines part run \
  --part=<part-id> \
  --data='{"name": "inspection-station-1-main"}' \
  viam.app.v1.RobotService.GetRobotPart
```

Then update the fragment's variable override. Open the machine's JSON config and add the `fragment_mods` entry:

```json
{
  "fragment_mods": [
    {
      "fragment_id": "<try-vision-pipeline-fragment-id>",
      "mods": [
        {
          "$ set": {
            "camera_name": "inspection-cam"
          }
        }
      ]
    }
  ]
}
```

Save this as `fragment-vars.json` and apply it with the app API, or set the variable in the [Viam app](https://app.viam.com) if you prefer.

{{< alert title="What the fragment added" color="info" >}}
The fragment added two services and their dependencies to your machine:

- **model-service**: An ML model service running TensorFlow Lite with the `can-defect-detection` model from the Viam registry. This model classifies cans as PASS or FAIL.
- **vision-service**: A vision service that takes images from your camera, runs them through the ML model, and returns structured detection results.

The fragment also added the TFLite CPU module and the ML model package. Everything is wired together and ready to use.
{{< /alert >}}

{{< alert title="Fragments and reuse" color="tip" >}}
This fragment works with any camera. If you were using a USB webcam instead of the simulation camera, you'd set `camera_name` to whatever you named your webcam component. The ML pipeline stays the same. This is how fragments enable reuse across different hardware setups.
{{< /alert >}}

### Test the vision service

1. Open [app.viam.com](https://app.viam.com) and navigate to your machine
2. Click the **CONFIGURE** tab and find `vision-service`
3. Expand the **TEST** section, select `inspection-cam` as the camera source, and set **Detections/Classifications** to `Live`

{{< alert title="What you've built" color="info" >}}
A complete ML inference pipeline. The vision service grabs an image from the camera, runs it through the TensorFlow Lite model, and returns structured detection results. This same pattern works for any ML task: object detection, classification, segmentation. Swap the model and camera, and the pipeline still works.
{{< /alert >}}

{{< alert title="Checkpoint" color="success" >}}
You added a camera component and used a fragment to add a complete ML vision pipeline — entirely from the command line. The system can detect defective cans. Next, you'll set up continuous data capture so every detection is recorded and queryable.
{{< /alert >}}

{{< alert title="Explore the JSON configuration" color="tip" >}}
Everything you configured is stored as JSON in Viam's cloud. You can inspect the full configuration at any time:

```sh {class="command-line" data-prompt="$"}
viam metadata read --part-id=<part-id>
```

You'll see your camera component, the fragment reference, and how the fragment's services connect to your camera. As configurations grow more complex, the JSON view helps you understand how components and services connect.
{{< /alert >}}

**[Continue to Part 2: Data Capture →](../part-2/)**
