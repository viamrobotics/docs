---
linkTitle: "Overview"
title: "Overview"
weight: 1
layout: "docs"
type: "docs"
no_list: true
description: "Build a complete quality inspection system with Viam — from camera setup to customer-facing product."
date: "2025-01-30"
aliases:
  - /try/first-project/
---

**Time:** ~45 minutes

## Scenario

This tutorial uses the simplest work cell (camera + compute) to teach patterns that apply to _all_ Viam applications.

You're building a **quality inspection station** for a canning line. Cans move past a camera on a conveyor belt. Your system must:

1. Detect when a can is present
2. Classify it as PASS or FAIL (identifying dented cans)
3. Log results for review and analysis
4. Provide a monitoring dashboard for operators

### Tutorial

In this tutorial you will work through a series of tasks that are common to many robotics applications. The techniques you learn here are applicable regardless of what hardware, software, data, or machine learning models you are working with.

| Part                                  | Time    | What you'll do                                         |
| ------------------------------------- | ------- | ------------------------------------------------------ |
| [Part 1: Vision pipeline](../part-1/) | ~10 min | Set up camera, ML model, and vision service            |
| [Part 2: Data capture](../part-2/)    | ~5 min  | Configure automatic image capture and cloud sync       |
| [Part 3: Control logic](../part-3/)   | ~10 min | Generate module, write inspection logic, test from CLI |
| [Part 4: Deploy a module](../part-4/) | ~10 min | Deploy module, configure detection data capture        |
| [Part 5: Productize](../part-5/)      | ~10 min | Build monitoring dashboard with Teleop                 |

{{< expand "Full section outline" >}}

**[Part 1: Vision pipeline](../part-1/)** (~10 min)

- [1.1 Verify your machine is online](../part-1/#11-verify-your-machine-is-online)
- [1.2 Locate your machine part](../part-1/#12-locate-your-machine-part)
- [1.3 Configure the camera](../part-1/#13-configure-the-camera)
- [1.4 Test the camera](../part-1/#14-test-the-camera)
- [1.5 Add a vision pipeline with a fragment](../part-1/#15-add-a-vision-pipeline-with-a-fragment)

**[Part 2: Data capture](../part-2/)** (~5 min)

- [2.1 Configure data capture](../part-2/#21-configure-data-capture)
- [2.2 View captured data](../part-2/#22-view-captured-data)
- [2.3 Summary](../part-2/#23-summary)

**[Part 3: Control logic](../part-3/)** (~10 min)

- [3.1 Generate the module scaffolding](../part-3/#31-generate-the-module-scaffolding)
- [3.2 Add remote machine connection](../part-3/#32-add-remote-machine-connection)
- [3.3 Add detection logic](../part-3/#33-add-detection-logic)
- [3.4 Summary](../part-3/#34-summary)

**[Part 4: Deploy a module](../part-4/)** (~10 min)

- [4.1 Review the generated module structure](../part-4/#41-review-the-generated-module-structure)
- [4.2 Build and upload your module](../part-4/#42-build-and-upload-your-module)
- [4.3 Add the module to your machine](../part-4/#43-add-the-module-to-your-machine)
- [4.4 Configure detection data capture](../part-4/#44-configure-detection-data-capture)
- [4.5 Summary](../part-4/#45-summary)

**[Part 5: Productize](../part-5/)** (~10 min)

- [5.1 Create a workspace](../part-5/#51-create-a-workspace)
- [5.2 Add a camera stream widget](../part-5/#52-add-a-camera-stream-widget)
- [5.3 Add a defects per minute widget](../part-5/#53-add-a-defects-per-minute-widget)
- [5.4 Add a confidence trend widget](../part-5/#54-add-a-confidence-trend-widget)
- [5.5 Arrange your dashboard](../part-5/#55-arrange-your-dashboard)
- [5.6 Summary](../part-5/#56-summary)

{{< /expand >}}

## Get started

Before starting, set up the Gazebo simulation environment by following the **[Gazebo Simulation Setup](../gazebo-setup/)** guide (~10 min).

**[Begin Gazebo Simulation Setup →](../gazebo-setup/)**
