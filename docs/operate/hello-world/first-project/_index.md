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

**Time:** ~75 minutes

## Before You Begin

### What is Viam?

Viam lets you build robotics applications the way you build other software. Viam abstracts away hardware concerns and services for common tasks to enable you to focus on your core robotics application. Declare your hardware in a config, write control logic against well-defined APIs for everything, push updates through a CLI. Viam is the development workflow you're used to, applied to physical machines.

Viam supports most robotics hardware. If your hardware isn't on the list, you can add support with a custom module by implementing the appropriate API.

This tutorial uses the simplest work cell (camera + compute) to teach patterns that apply to _all_ Viam applications.

## Scenario

You're building a **quality inspection station** for a canning line. Cans move past a camera on a conveyor belt. Your system must:

1. Detect when a can is present
2. Classify it as PASS or FAIL (identifying dented cans)
3. Log results and trigger alerts on failures
4. Scale to multiple inspection stations
5. Ship as a product your customers can use

### Tutorial Overview

In this tutorial you will work through a series of tasks that are common to many robotics applications. The techniques you learn here are applicable regardless of what hardware, software, data, or machine learning models you are working with.

| Part                               | Time    | What You'll Do                                          |
| ---------------------------------- | ------- | ------------------------------------------------------- |
| [Part 1: Vision Pipeline](part-1/) | ~15 min | Set up camera, ML model, and vision service             |
| [Part 2: Data Capture](part-2/)    | ~15 min | Configure automatic data sync and alerts                |
| [Part 3: Control Logic](part-3/)   | ~15 min | Generate module, write inspection logic, test from CLI  |
| [Part 4: Deploy a Module](part-4/) | ~10 min | Add DoCommand, deploy, configure detection data capture |
| [Part 5: Scale](part-5/)           | ~10 min | Create fragment, add second machine                     |
| [Part 6: Productize](part-6/)      | ~10 min | Build dashboard, white-label auth                       |

{{< expand "Full Section Outline" >}}

**[Part 1: Vision Pipeline](part-1/)** (~15 min)

- [1.1 Verify Your Machine is Online](part-1/#11-verify-your-machine-is-online)
- [1.2 Locate Your Machine Part](part-1/#12-locate-your-machine-part)
- [1.3 Configure the Camera](part-1/#13-configure-the-camera)
- [1.4 Test the Camera](part-1/#14-test-the-camera)
- [1.5 Add an ML Model Service](part-1/#15-add-an-ml-model-service)
- [1.6 Add a Vision Service](part-1/#16-add-a-vision-service)

**[Part 2: Data Capture](part-2/)** (~15 min)

- [2.1 Configure Data Capture](part-2/#21-configure-data-capture)
- [2.2 View Captured Data](part-2/#22-view-captured-data)
- [2.3 Summary](part-2/#23-summary)

**[Part 3: Control Logic](part-3/)** (~15 min)

- [3.1 Generate the Module Scaffold](part-3/#31-generate-the-module-scaffold)
- [3.2 Add Remote Machine Connection](part-3/#32-add-remote-machine-connection)
- [3.3 Add Detection Logic](part-3/#33-add-detection-logic)
- [3.4 Configure the Rejector](part-3/#34-configure-the-rejector)
- [3.5 Add Rejection Logic](part-3/#35-add-rejection-logic)
- [3.6 Summary](part-3/#36-summary)

**[Part 4: Deploy a Module](part-4/)** (~10 min)

- [4.1 Add the DoCommand Interface](part-4/#41-add-the-docommand-interface)
- [4.2 Review the Generated Module Structure](part-4/#42-review-the-generated-module-structure)
- [4.3 Build and Deploy](part-4/#43-build-and-deploy)
- [4.4 Configure Detection Data Capture](part-4/#44-configure-detection-data-capture)
- [4.5 Summary](part-4/#45-summary)

**[Part 5: Scale](part-5/)** (~10 min)

- [5.1 Create a Fragment](part-5/#51-create-a-fragment)
- [5.2 Parameterize the Camera ID](part-5/#52-parameterize-the-camera-id)
- [5.5 Create the Second Machine](part-5/#55-create-the-second-machine)
- [5.9 Fleet Management Capabilities](part-5/#59-fleet-management-capabilities)

**[Part 6: Productize](part-6/)** (~15 min)

- [6.1 Create a Dashboard](part-6/#61-create-a-dashboard)
- [6.2 Set Up White-Label Auth](part-6/#62-set-up-white-label-auth)
- [6.3 (Optional) Configure Billing](part-6/#63-optional-configure-billing)

{{< /expand >}}

## Get Started

**[Begin Part 1: Vision Pipeline →](part-1/)**
