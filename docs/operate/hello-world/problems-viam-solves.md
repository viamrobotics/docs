---
linkTitle: "Problems Viam Solves"
title: "Problems Viam Solves"
weight: 15
layout: "docs"
type: "docs"
description: "A guide to the challenges you'll face at each stage of robotics development and how Viam helps."
date: "2025-01-30"
---

Building a robotics application is hard.
Not just the "making a robot move" part—that's the beginning.
The real challenges emerge as you move from prototype to production.

This document maps the problems you'll face at each stage and shows where Viam helps.

## Stage 1: Prototype

_You're building something that works on your bench._

### The Problems

**Hardware integration is painful.** Every sensor and actuator has its own SDK, its own quirks, its own incompatibilities. You spend more time debugging drivers than building features.

**Communication protocols are arcane.** I2C, SPI, UART, CAN—each with its own timing, addressing, and failure modes. You didn't sign up to become a protocol expert.

**Development is tied to the device.** You're SSH'ing in, editing files, restarting processes. The iteration loop is slow and frustrating.

**There's no consistency.** Code for one camera doesn't work with another. Switching motors means rewriting control logic. Everything is bespoke.

**Building intelligence is even harder.** Object detection requires ML pipelines. Motion planning requires complex algorithms. You're supposed to be building an application, not reinventing computer vision.

### How Viam Helps

**Viam's Registry** provides pre-built, tested modules for 200+ components. You configure your hardware—you don't write driver code.

**Communication protocols are entirely abstracted**. You never think about I2C versus SPI. You configure "this is a motor" and it works.

**Develop code anywhere.** Write code on your laptop in your IDE. Run it against your robot over the network. No SSH, no file copying, no deploy step. Just run and see results. When latency matters, move the code to the device—same APIs, same code.

**SDKs and APIs work across all hardware.** Switch cameras? Change one config line. Your code stays the same.

**Built-in services for vision and motion.** Object detection, classification, and segmentation work out of the box. Motion planning handles path optimization and collision avoidance. Focus on what your robot should do, not how to make it see and move.

## Stage 2: First Deployment

_Your robot leaves the bench and enters the real world._

### The Problems

**The environment is hostile.** Lighting changes. Temperatures vary. Dust accumulates. Things that worked perfectly on your bench fail mysteriously in the field.

**Calibration is tedious.** Camera-arm setups need precise spatial relationships. You're measuring offsets, calculating transforms, getting it wrong, measuring again.

**Network access is complicated.** Your robot is behind a firewall. NAT makes inbound connections impossible. You can't just SSH in.

**You can't see what's happening.** When something goes wrong, you're blind. Logs are on the device. Sensor feeds are inaccessible. Debugging requires physical presence.

**Available models don't fit your use case.** Pre-trained object detection doesn't recognize your specific parts. You need custom models, but setting up training infrastructure is a project in itself.

### How Viam Helps

**Diagnose environmental issues remotely.** When lighting, temperature, or dust cause unexpected behavior, view live camera feeds and sensor data to identify problems without dispatching a technician. Adjust configuration from the cloud.

**Remote access works through firewalls.** WebRTC handles NAT traversal automatically. No VPN, no port forwarding, no IT department negotiations.

**Pre-computed transforms** for common hardware combinations. Reusable configuration blocks (fragments) include the spatial relationships your motion planner needs—no manual measurement required for supported camera-arm setups.

**You can see everything remotely.** Live sensor feeds, component status, and logs—all accessible from the Viam app or your code.

**Configuration pushes from the cloud.** When you need to adjust settings in the field, you don't need to touch the device.

**Train custom models on captured data.** Capture images from your deployed robots, annotate them, and train models—all within Viam. No GPU provisioning, no ML pipeline setup. Deploy trained models back to your fleet with versioning.

## Stage 3: Multiple Units

_You've proven the concept. Now you're deploying 5, 10, 50 robots._

### The Problems

**Setup doesn't scale.** Manually configuring each device takes hours. Mistakes creep in. Units drift out of sync.

**Hardware is never identical.** Different sensor batches. Different revisions. Subtle variations that break assumptions.

**Updates are terrifying.** Pushing changes to many devices at once? What if something goes wrong? What if you brick the fleet?

### How Viam Helps

**Provisioning is streamlined.** New devices connect to the cloud and pull their configuration automatically.

**Fragments are reusable configurations.** Define a camera-arm combination, a vision pipeline, or an entire work cell once. Apply it to any number of machines. Override per-machine differences (different camera model, site-specific settings) without forking the base fragment.

**Staged rollouts** let you push updates to one device, then ten, then all. Rollback if something goes wrong.

## Stage 4: Fleet at Scale

_You're operating hundreds or thousands of robots—and delivering to customers._

### The Problems

**Visibility is overwhelming.** You can't watch every device. You need to know which ones need attention.

**Updates are high-stakes.** A bad push can take down production. You need confidence before rolling out changes.

**Customers expect dashboards.** They want to see their robots. You need to provide access without building auth systems, billing infrastructure, and dashboards from scratch.

### How Viam Helps

**Fleet monitoring** shows health across all devices at a glance. Anomalies surface automatically.

**OTA updates at scale** with staged rollouts, canary deployments, and rollback.

**Customer delivery infrastructure built in.** White-label authentication with your branding. TypeScript SDK for web dashboards, Flutter SDK for mobile apps. Built-in billing with per-machine or per-data pricing tiers.

## Stage 5: Ongoing Maintenance

_The fleet is running. Now you maintain it forever._

### The Problems

**Remote debugging is essential.** You can't dispatch a technician for every issue. You need to diagnose from afar.

**Logs are scattered.** Getting logs off devices with intermittent connectivity is its own infrastructure project.

**Maintenance tasks pile up.** Periodic calibrations, health checks, sensor readings—you're writing cron jobs and custom schedulers.

**Models drift.** The ML model that worked at launch degrades over time. You need to retrain and redeploy.

### How Viam Helps

**Remote log access** with offline buffering. Logs sync when connectivity returns.

**Scheduled tasks without schedulers.** Run periodic sensor readings, daily calibrations, health checks at specified intervals—no cron jobs required.

**Data pipelines** capture real-world performance continuously. Use this data to identify issues and retrain models.

**One-click model deployment** updates ML models across the fleet without touching application code.

## Summary

| Stage     | Pain                                              | Viam Solution                                                                     |
| --------- | ------------------------------------------------- | --------------------------------------------------------------------------------- |
| Prototype | Hardware integration, slow iteration              | Viam Registry, develop from anywhere, consistent APIs, built-in vision and motion |
| Deploy    | Calibration, remote access, visibility, model fit | Pre-computed transforms, WebRTC, remote diagnostics, model training               |
| Scale     | Configuration management                          | Reusable configuration blocks (fragments), staged rollouts                        |
| Fleet     | Visibility, updates, customer delivery            | Monitoring, OTA, white-label auth, billing                                        |
| Maintain  | Remote debugging, scheduled tasks                 | Logs, scheduled jobs, model deployment                                            |

## Next steps

{{< cards >}}
{{% card link="/operate/hello-world/what-is-viam/" %}}
{{% card link="/operate/hello-world/tutorial-desk-safari/" %}}
{{< /cards >}}
