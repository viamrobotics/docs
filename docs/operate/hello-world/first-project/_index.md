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
**Components:** Camera + Compute
**Physics required:** None (rendered images only)

## Before You Begin

### What is Viam?

Viam lets you build robotics applications the way you build other software. Viam abstracts away hardware concerns and services for common tasks to enable you to focus on your core robotics application. Declare your hardware in a config, write control logic against well-defined APIs for everything, push updates through a CLI. Viam is the development workflow you're used to, applied to physical machines.

Viam works with any hardware:

| Category | Examples                                    |
| -------- | ------------------------------------------- |
| Cameras  | Webcams, depth cameras, thermal, CSI        |
| Arms     | 6-DOF robot arms, collaborative arms        |
| Bases    | Wheeled, tracked, holonomic, drones         |
| Motors   | DC, stepper, servo, brushless               |
| Sensors  | IMU, GPS, ultrasonic, temperature, humidity |
| Grippers | Parallel jaw, vacuum, custom end effectors  |
| Boards   | Raspberry Pi, Jetson, Orange Pi, ESP32      |
| LiDAR    | 2D and 3D scanning                          |
| Encoders | Rotary, absolute, incremental               |
| Gantries | Linear actuators, multi-axis systems        |

If your hardware isn't on the list, you can add support with a custom module by implementing the appropriate API.

This tutorial uses the simplest work cell (camera + compute) to teach patterns that apply to _all_ Viam applications.

### What You'll Learn

By the end of this tutorial, you'll understand how to:

| Skill                | What It Means                               | Applies To                          |
| -------------------- | ------------------------------------------- | ----------------------------------- |
| Configure components | Add hardware to a Viam machine              | Any sensor, actuator, or peripheral |
| Add services         | Attach capabilities like ML inference       | Vision, navigation, motion planning |
| Write control logic  | Code that reads sensors and makes decisions | Any automation task                 |
| Configure automation | Set up data capture, triggers, and alerts   | Production monitoring               |
| Scale with fragments | Reuse configurations across machines        | Any fleet, any size                 |
| Manage fleets        | Monitor, update, and debug remotely         | Production operations               |
| Build customer apps  | Create products on top of Viam              | Shipping to your customers          |

**These patterns are the same whether you're working with a camera, a robot arm, or a warehouse full of mobile robots.**

## Scenario

You're building a **quality inspection station** for a canning line. Cans move past a camera on a conveyor belt. Your system must:

1. Detect when a can is present
2. Classify it as PASS or FAIL (identifying dented cans)
3. Log results and trigger alerts on failures
4. Scale to multiple inspection stations
5. Ship as a product your customers can use

## What You'll Build

A working inspection system with:

- A camera streaming live images
- An ML model classifying cans as PASS/FAIL (detecting dents)
- Business logic that triggers alerts on failures
- A second station added to your fleet
- A dashboard showing inspection results across stations
- A customer-facing web app with your branding

## Tutorial Parts

| Part                                   | Time    | What You'll Do                                         |
| -------------------------------------- | ------- | ------------------------------------------------------ |
| [Part 1: Vision Pipeline](part-1/)     | ~15 min | Set up camera, ML model, and vision service            |
| [Part 2: Data Capture](part-2/)        | ~15 min | Configure automatic data sync and alerts               |
| [Part 3: Build the Inspector](part-3/) | ~15 min | Generate module, write inspection logic, test from CLI |
| [Part 4: Deploy as a Module](part-4/)  | ~10 min | Add DoCommand, package and deploy                      |
| [Part 5: Scale](part-5/)               | ~10 min | Create fragment, add second machine                    |
| [Part 6: Productize](part-6/)          | ~10 min | Build dashboard, white-label auth                      |

{{< expand "Full Section Outline" >}}

**[Part 1: Vision Pipeline](part-1/)** (~15 min)

- [1.1 Understand viam-server](part-1/#11-understand-viam-server)
- [1.2 Verify Your Machine is Online](part-1/#12-verify-your-machine-is-online)
- [1.3 Configure the Camera](part-1/#13-configure-the-camera)
- [1.4 Test the Camera](part-1/#14-test-the-camera)
- [1.5 Add a Vision Service](part-1/#15-add-a-vision-service)

**[Part 2: Data Capture](part-2/)** (~15 min)

- [2.1 Configure Data Capture](part-2/#21-configure-data-capture)
- [2.2 Add Machine Health Alert](part-2/#22-add-machine-health-alert)
- [2.3 View and Query Data](part-2/#23-view-and-query-data)
- [2.4 Summary](part-2/#24-summary)

**[Part 3: Build the Inspector](part-3/)** (~15 min)

- [3.1 Generate the Module Scaffold](part-3/#31-generate-the-module-scaffold)
- [3.2 Add Remote Machine Connection](part-3/#32-add-remote-machine-connection)
- [3.3 Add Detection Logic](part-3/#33-add-detection-logic)
- [3.4 Configure the Rejector](part-3/#34-configure-the-rejector)
- [3.5 Add Rejection Logic](part-3/#35-add-rejection-logic)
- [3.6 Summary](part-3/#36-summary)

**[Part 4: Deploy as a Module](part-4/)** (~10 min)

- [4.1 Add the DoCommand Interface](part-4/#41-add-the-docommand-interface)
- [4.2 Review the Generated Module Structure](part-4/#42-review-the-generated-module-structure)
- [4.3 Build and Deploy](part-4/#43-build-and-deploy)
- [4.4 Summary](part-4/#44-summary)

**[Part 5: Scale](part-5/)** (~10 min)

- [5.1 Create a Fragment](part-5/#51-create-a-fragment)
- [5.2 Parameterize Machine-Specific Values](part-5/#52-parameterize-machine-specific-values)
- [5.3 Add a Second Machine](part-5/#53-add-a-second-machine)
- [5.4 Fleet Management Capabilities](part-5/#54-fleet-management-capabilities)

**[Part 6: Productize](part-6/)** (~15 min)

- [6.1 Create a Dashboard](part-6/#61-create-a-dashboard)
- [6.2 Set Up White-Label Auth](part-6/#62-set-up-white-label-auth)
- [6.3 (Optional) Configure Billing](part-6/#63-optional-configure-billing)

{{< /expand >}}

## Get Started

**[Begin Part 1: Vision Pipeline →](part-1/)**

## Simulation Requirements

### Work Cell Elements

| Element       | Description                                         |
| ------------- | --------------------------------------------------- |
| Conveyor belt | Moving belt where cans travel                       |
| Camera        | Overhead RGB camera (640x480)                       |
| Sample cans   | Mix of good cans and dented cans (~10% defect rate) |
| Lighting      | Consistent industrial lighting                      |

### Viam Components

| Component        | Type             | Notes                                                     |
| ---------------- | ---------------- | --------------------------------------------------------- |
| `inspection-cam` | camera           | Gazebo RGB camera                                         |
| `can-classifier` | mlmodel          | TFLite model for PASS/FAIL classification (detects dents) |
| `can-detector`   | vision           | ML model service connected to camera                      |
| `rejector`       | motor            | Pneumatic pusher for rejecting defective cans             |
| `inspector`      | generic (module) | Control logic service                                     |
| `offline-alert`  | trigger          | Email notification when machine goes offline              |

### Simulated Events

| Event       | Trigger                     | Purpose            |
| ----------- | --------------------------- | ------------------ |
| Can appears | Automatic (every 4 seconds) | New can to inspect |
