---
linkTitle: "Problems Viam Solves"
title: "Problems Viam Solves"
weight: 15
layout: "docs"
type: "docs"
description: "A guide to the challenges you'll face at each stage of robotics development and how Viam helps."
date: "2025-01-30"
---

Building a robotics application is hard. This document maps the problems you'll face at each stage and shows where Viam helps.

## Stage 1: Prototype

_You're building something that works on your bench._

### The Problems

**Hardware integration is painful.** Every sensor and actuator has its own SDK, its own quirks, and its own incompatibilities. You spend more time debugging drivers than building features.

**Communication protocols are arcane.** I2C, SPI, UART, and CAN each have their own timing, addressing, and failure modes. Working with different protocols slows the pace of development.

**Development is tied to the device.** You're SSH'ing in, editing files, and restarting processes. The iteration loop is slow and frustrating.

**There's no consistency.** Code for one camera doesn't work with another. Switching motors means rewriting control logic. Everything is bespoke.

**Building intelligence is even harder.** Object detection requires ML pipelines. Motion planning requires complex algorithms. Building these from scratch distracts from your actual application.

### How Viam Helps

**Viam's Registry** provides pre-built, tested modules for 200+ components. You configure your hardware in a simple JSON file rather than writing driver code.

**Communication protocols are entirely abstracted**. You never have to think about I2C versus SPI. Viam abstracts away the different protocols, giving you a consistent API across cameras, sensors, motors, etc.

**Develop code anywhere.** Write code on your laptop in your IDE. Run it against your robot over the network.

**SDKs and APIs work across all hardware.** To swap one camera for another in Viam, you change a few lines of a configuration file. Your code stays the same.

**Built-in services for vision and motion.** Object detection, classification, and segmentation work out of the box. Motion planning handles path optimization and collision avoidance. Focus on what your robot should do, not how to make it see and move.

## Stage 2: First Deployment

_Your robot leaves the bench and enters the real world._

### The Problems

**The environment is hostile.** Lighting changes, dust accumulates, and temperatures vary. Solutions that worked on your bench fail in the field.

**Calibration is tedious.** Camera-arm setups need precise spatial relationships for motion planning. This type of calibration is difficult and time-consuming.

**Network access is complicated.** Your robot is behind a firewall. NAT makes inbound connections impossible. You can't just SSH in.

**You can't see what's happening.** When something goes wrong, you're blind. Logs are on the device. Sensor feeds are inaccessible. Debugging remotely is not possible.

**Available models don't fit your use case.** Pre-trained models rarely recognize your specific objects or scenarios. Training custom models requires infrastructure that is a project in itself.

### How Viam Helps

**Diagnose environmental issues remotely.** When lighting, temperature, or dust cause unexpected behavior, view live camera feeds and sensor data to identify problems. Adjust configuration from the cloud.

**Remote access works through firewalls.** WebRTC handles NAT traversal automatically. You do not need to set up a VPN or port forwarding.

**Pre-computed transforms** are available for common hardware combinations. Reusable configuration blocks (fragments) include the spatial relationships your motion planner needs. No manual calibration is required for supported camera-arm setups.

**You can see everything remotely.** Live sensor feeds, component status, and logs are all accessible from the Viam app or your code, which can run from anywhere.

**Configuration pushes from the cloud.** When you need to adjust settings in the field, you don't need to touch the device.

**Train custom models on captured data.** Capture images from your deployed robots, annotate them, and train models within Viam's data management infrastructure.

## Stage 3: Multiple Units

_You've proven the concept. Now you're deploying 5, 10, 50 robots._

### The Problems

**Setup doesn't scale.** Manually configuring each device takes hours. Mistakes creep in. Units drift out of sync.

**Hardware is never identical.** Different sensor batches and revisions create subtle variations.

**Updates are error-prone.** You either need to write your own fleet deployment infrastructure or deploy updates to each machine, one at a time.

### How Viam Helps

**Provisioning is streamlined.** New devices connect to the cloud and pull their configuration automatically.

**Fragments are reusable configurations.** Define a camera-arm combination, a vision pipeline, or an entire work cell once. Apply it to any number of machines. Override per-machine differences (different camera model, site-specific settings) without forking the base fragment.

**Staged rollouts** let you push updates to one device, then ten, then all, with rollback if something goes wrong.

## Stage 4: Fleet at Scale

_You're operating hundreds or thousands of robots—and delivering to customers._

### The Problems

**Visibility is overwhelming.** Monitoring every device individually is not feasible. You need systems that surface which devices require attention.

**Updates are high-stakes.** A bad update can disrupt production across your fleet. You need mechanisms to stage and validate changes.

**Customers expect dashboards.** They want to see their robots. You need to provide access without building auth systems, billing infrastructure, and dashboards from scratch.

### How Viam Helps

**Fleet monitoring** shows health across all devices at a glance. Anomalies surface automatically.

Viam enables **OTA updates at scale** with staged rollouts, canary deployments, and rollback.

**Customer delivery infrastructure built in.** White-label authentication with your branding. TypeScript SDK for web dashboards, Flutter SDK for mobile apps. Built-in billing with per-machine or per-data pricing tiers.

## Stage 5: Ongoing Maintenance

_The fleet is running. Now you maintain it forever._

### The Problems

**Remote debugging is essential.** Without physical access to devices, you need visibility into logs, sensor state, and system health.

**Logs are scattered.** Retrieving logs from devices with intermittent connectivity requires dedicated infrastructure.

**Maintenance tasks pile up.** Periodic calibrations, health checks, and sensor readings require scheduling infrastructure such as cron jobs or custom schedulers.

**Models drift.** The ML model that worked at launch degrades over time. You need to retrain and redeploy.

### How Viam Helps

**Remote log access** includes offline buffering. Logs synchronize automatically when connectivity is restored.

**Scheduled tasks without custom schedulers.** Viam runs periodic sensor readings, daily calibrations, and health checks at specified intervals without requiring cron jobs or external scheduling infrastructure.

**Data pipelines** capture real-world performance continuously. Use this data to identify issues and retrain models.

**One-click model deployment** allows you to update ML models across the fleet.

## Summary

| Stage     | Pain                                              | Viam Solution                                                                     |
| --------- | ------------------------------------------------- | --------------------------------------------------------------------------------- |
| Prototype | Hardware integration, slow iteration              | Viam Registry, develop from anywhere, consistent APIs, built-in vision and motion |
| Deploy    | Calibration, remote access, visibility, model fit | Pre-computed transforms, WebRTC, remote diagnostics, model training               |
| Scale     | Configuration management                          | Reusable configuration blocks (fragments), staged rollouts                        |
| Fleet     | Visibility, updates, customer delivery            | Monitoring, OTA, white-label auth, billing                                        |
| Maintain  | Remote debugging, scheduled tasks, model drift    | Log access, scheduled jobs, model deployment                                      |

## Next steps

{{< cards >}}
{{% card link="/operate/hello-world/what-is-viam/" %}}
{{% card link="/operate/hello-world/tutorial-desk-safari/" %}}
{{< /cards >}}
