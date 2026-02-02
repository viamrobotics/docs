---
linkTitle: "Your First Project"
title: "Your First Project"
weight: 17
layout: "docs"
type: "docs"
no_list: true
description: "Build a complete quality inspection system with Viam—from camera setup to customer-facing product."
date: "2025-01-30"
---

**Time:** ~60 minutes

## Before You Begin

### What is Viam?

Viam lets you build robotics applications the way you build other software. Viam abstracts away hardware concerns and services for common tasks to enable you to focus on your core robotics application. Declare your hardware in a config, write control logic against well-defined APIs for everything, push updates through a CLI. Viam is the development workflow you're used to, applied to physical machines.

Viam supports most robotics hardware. If your hardware isn't on the list, you can add support with a custom module by implementing the appropriate API.

This tutorial uses the simplest work cell (camera + compute) to teach patterns that apply to _all_ Viam applications.

## Scenario

You're building a **quality inspection station** for a canning line. Cans move past a camera on a conveyor belt. Your system must:

1. Detect when a can is present
2. Classify it as PASS or FAIL (identifying dented cans)
3. Log results for review and analysis
4. Provide a monitoring dashboard for operators

### Tutorial Overview

In this tutorial you will work through a series of tasks that are common to many robotics applications. The techniques you learn here are applicable regardless of what hardware, software, data, or machine learning models you are working with.

| Part                               | Time    | What You'll Do                                         |
| ---------------------------------- | ------- | ------------------------------------------------------ |
| [Part 1: Vision Pipeline](part-1/) | ~15 min | Set up camera, ML model, and vision service            |
| [Part 2: Data Capture](part-2/)    | ~10 min | Configure automatic image capture and cloud sync       |
| [Part 3: Control Logic](part-3/)   | ~15 min | Generate module, write inspection logic, test from CLI |
| [Part 4: Deploy a Module](part-4/) | ~10 min | Deploy module, configure detection data capture        |
| [Part 5: Productize](part-5/)      | ~10 min | Build monitoring dashboard with Teleop                 |

{{< expand "Full Section Outline" >}}

**[Part 1: Vision Pipeline](part-1/)** (~15 min)

- [1.1 Verify Your Machine is Online](part-1/#11-verify-your-machine-is-online)
- [1.2 Locate Your Machine Part](part-1/#12-locate-your-machine-part)
- [1.3 Configure the Camera](part-1/#13-configure-the-camera)
- [1.4 Test the Camera](part-1/#14-test-the-camera)
- [1.5 Add an ML Model Service](part-1/#15-add-an-ml-model-service)
- [1.6 Add a Vision Service](part-1/#16-add-a-vision-service)

**[Part 2: Data Capture](part-2/)** (~10 min)

- [2.1 Configure Data Capture](part-2/#21-configure-data-capture)
- [2.2 View Captured Data](part-2/#22-view-captured-data)
- [2.3 Summary](part-2/#23-summary)

**[Part 3: Control Logic](part-3/)** (~15 min)

- [3.1 Generate the Module Scaffolding](part-3/#31-generate-the-module-scaffolding)
- [3.2 Add Remote Machine Connection](part-3/#32-add-remote-machine-connection)
- [3.3 Add Detection Logic](part-3/#33-add-detection-logic)
- [3.4 Summary](part-3/#34-summary)

**[Part 4: Deploy a Module](part-4/)** (~10 min)

- [4.1 Review the Generated Module Structure](part-4/#41-review-the-generated-module-structure)
- [4.2 Build and Upload Your Module](part-4/#42-build-and-upload-your-module)
- [4.3 Add the Module to Your Machine](part-4/#43-add-the-module-to-your-machine)
- [4.4 Configure Detection Data Capture](part-4/#44-configure-detection-data-capture)
- [4.5 Summary](part-4/#45-summary)

**[Part 5: Productize](part-5/)** (~10 min)

- [5.1 Create a Workspace](part-5/#51-create-a-workspace)
- [5.2 Add a Camera Stream Widget](part-5/#52-add-a-camera-stream-widget)
- [5.3 Add a Defects Per Minute Widget](part-5/#53-add-a-defects-per-minute-widget)
- [5.4 Add a Confidence Trend Widget](part-5/#54-add-a-confidence-trend-widget)
- [5.5 Arrange Your Dashboard](part-5/#55-arrange-your-dashboard)
- [5.6 Summary](part-5/#56-summary)

{{< /expand >}}

## Get Started

**[Begin Part 1: Vision Pipeline →](part-1/)**