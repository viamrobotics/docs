---
title: "Quality Inspection with Gazebo Simulation"
linkTitle: "Quality Inspection"
type: "docs"
weight: 60
description: "Build a complete quality inspection system with Viam — from camera setup to customer-facing product — using a Gazebo simulation, no hardware required."
authors: []
level: "Beginner"
languages: ["go"]
viamresources: ["camera", "vision", "mlmodel", "data_manager", "generic"]
platformarea: ["ml", "data", "core"]
tags: ["tutorial", "workshop", "vision", "data", "module"]
workshop: "quality-inspection"
workshop_overview: true
time_estimate: "55 minutes"
no_list: true
aliases:
  - /try/overview/
  - /try/first-project/
---

This tutorial uses the simplest work cell (camera + compute) to teach patterns that apply to _all_ Viam applications—and it runs entirely in a Gazebo simulation, so you don't need any physical hardware to follow along.

## What you'll build

You're building a quality inspection station for a canning line. Cans move past a camera on a conveyor belt. Your system must:

1. Detect when a can is present
2. Classify it as PASS or FAIL (identifying dented cans)
3. Log results for review and analysis
4. Provide a monitoring dashboard for operators

The techniques you learn here are applicable regardless of what hardware, software, data, or machine learning models you are working with.

## Phases

1. **[Gazebo simulation setup](/tutorials/quality-inspection/gazebo-setup/)** (~10 min)
2. **[Vision pipeline](/tutorials/quality-inspection/vision-pipeline/)** (~10 min)
3. **[Data capture](/tutorials/quality-inspection/data-capture/)** (~5 min)
4. **[Control logic](/tutorials/quality-inspection/control-logic/)** (~10 min)
5. **[Deploy a module](/tutorials/quality-inspection/deploy-module/)** (~10 min)
6. **[Productize](/tutorials/quality-inspection/productize/)** (~10 min)

{{< expand "Full section outline" >}}

**[Gazebo simulation setup](/tutorials/quality-inspection/gazebo-setup/)** (~10 min)

- [Prerequisites](/tutorials/quality-inspection/gazebo-setup/#prerequisites)
- [Step 1: Build the Docker Image](/tutorials/quality-inspection/gazebo-setup/#step-1-build-the-docker-image)
- [Step 2: Create a Machine in Viam](/tutorials/quality-inspection/gazebo-setup/#step-2-create-a-machine-in-viam)
- [Step 3: Create a credentials file](/tutorials/quality-inspection/gazebo-setup/#step-3-create-a-credentials-file)
- [Step 4: Start the Container](/tutorials/quality-inspection/gazebo-setup/#step-4-start-the-container)
- [Step 5: Verify the Setup](/tutorials/quality-inspection/gazebo-setup/#step-5-verify-the-setup)

**[Vision pipeline](/tutorials/quality-inspection/vision-pipeline/)** (~10 min)

- [1.1 Verify your machine is online](/tutorials/quality-inspection/vision-pipeline/#11-verify-your-machine-is-online)
- [1.2 Locate your machine part](/tutorials/quality-inspection/vision-pipeline/#12-locate-your-machine-part)
- [1.3 Configure the camera](/tutorials/quality-inspection/vision-pipeline/#13-configure-the-camera)
- [1.4 Test the camera](/tutorials/quality-inspection/vision-pipeline/#14-test-the-camera)
- [1.5 Add a vision pipeline with a fragment](/tutorials/quality-inspection/vision-pipeline/#15-add-a-vision-pipeline-with-a-fragment)

**[Data capture](/tutorials/quality-inspection/data-capture/)** (~5 min)

- [2.1 Configure data capture](/tutorials/quality-inspection/data-capture/#21-configure-data-capture)
- [2.2 View captured data](/tutorials/quality-inspection/data-capture/#22-view-captured-data)
- [2.3 Summary](/tutorials/quality-inspection/data-capture/#23-summary)

**[Control logic](/tutorials/quality-inspection/control-logic/)** (~10 min)

- [3.1 Generate the module scaffolding](/tutorials/quality-inspection/control-logic/#31-generate-the-module-scaffolding)
- [3.2 Add remote machine connection](/tutorials/quality-inspection/control-logic/#32-add-remote-machine-connection)
- [3.3 Add detection logic](/tutorials/quality-inspection/control-logic/#33-add-detection-logic)
- [3.4 Summary](/tutorials/quality-inspection/control-logic/#34-summary)

**[Deploy a module](/tutorials/quality-inspection/deploy-module/)** (~10 min)

- [4.1 Review the generated module structure](/tutorials/quality-inspection/deploy-module/#41-review-the-generated-module-structure)
- [4.2 Build and upload your module](/tutorials/quality-inspection/deploy-module/#42-build-and-upload-your-module)
- [4.3 Add the module to your machine](/tutorials/quality-inspection/deploy-module/#43-add-the-module-to-your-machine)
- [4.4 Configure detection data capture](/tutorials/quality-inspection/deploy-module/#44-configure-detection-data-capture)
- [4.5 Summary](/tutorials/quality-inspection/deploy-module/#45-summary)

**[Productize](/tutorials/quality-inspection/productize/)** (~10 min)

- [5.1 Create a workspace](/tutorials/quality-inspection/productize/#51-create-a-workspace)
- [5.2 Add a camera stream widget](/tutorials/quality-inspection/productize/#52-add-a-camera-stream-widget)
- [5.3 Add a defects per minute widget](/tutorials/quality-inspection/productize/#53-add-a-defects-per-minute-widget)
- [5.4 Add a confidence trend widget](/tutorials/quality-inspection/productize/#54-add-a-confidence-trend-widget)
- [5.5 Arrange your dashboard](/tutorials/quality-inspection/productize/#55-arrange-your-dashboard)
- [5.6 Summary](/tutorials/quality-inspection/productize/#56-summary)

{{< /expand >}}

## Get started

Before starting, set up the Gazebo simulation environment by following the **[Gazebo simulation setup](/tutorials/quality-inspection/gazebo-setup/)** guide (~10 min).

**[Begin Gazebo simulation setup →](/tutorials/quality-inspection/gazebo-setup/)**
