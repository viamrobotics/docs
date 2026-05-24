---
linkTitle: "Check the registry first"
title: "Add software capabilities from the registry"
weight: 3
layout: "docs"
type: "docs"
description: "Before writing a module, check whether one already exists. The registry has more than hardware drivers."
date: "2026-04-17"
aliases:
  - /registry/
---

Before you write a module, check whether one already exists. The Viam registry contains more than hardware drivers. Many software capabilities you might want to build are already published as modules you can configure and use directly.

This page exists in the build-modules section as a reminder: look first, build second. If an existing module solves your problem, you save the implementation work and inherit a maintained codebase.

## What's in the registry beyond hardware drivers

### Vision and ML

- Pre-trained detectors and classifiers: YOLOv8 ([viam-labs:vision:yolov8](https://app.viam.com/module/viam-labs/yolov8)), Roboflow Universe models, motion detection, person re-identification, face identification.
- LLM-based vision: GPT-4o for image classification ([mcvella:vision:chatgpt](https://app.viam.com/module/mcvella/openai)).
- ML model runtimes: TFLite, TensorFlow, ONNX, PyTorch, NVIDIA Triton, Coral Edge TPU.

### Conversational and audio

- LLM chat: local LLMs ([viam-labs:chat:llm](https://app.viam.com/module/viam-labs/local-llm)) and ChatGPT ([mcvella:chat:chatgpt](https://app.viam.com/module/mcvella/chatgpt)).
- Speech-to-text and text-to-speech: cloud-backed and local options ([viam-labs:speech:speechio](https://app.viam.com/module/viam-labs/speech), Vosk, Piper).
- System audio: microphones, speakers, wake-word filtering.

### Discovery for hardware already on your network

- RTSP cameras: UniFi Protect, ONVIF, UPnP.
- Depth cameras: Intel RealSense, Orbbec.
- System microphones and webcams.

### Custom logic and external integrations

- Generic services for one-off automations: for example, [automated plant watering](https://app.viam.com/module/devrel/watering-controller).
- External-service bridges: Google Calendar, Elgato Stream Deck.
- Data utilities: mirror captured data to other machines ([viam-soleng:data:mirror](https://app.viam.com/module/viam-soleng/mirror)).

### SLAM and motion

- Google Cartographer ([viam:slam:cartographer](https://app.viam.com/module/viam/slam)).
- Viam-hosted Cloud SLAM.
- Outdoor vehicle motion services.

## How to find a module

Two paths:

1. **Search the registry directly** at [app.viam.com/registry](https://app.viam.com/registry). Filter by type (Module, ML Model, or Training Script), by API (such as `rdk:service:vision` or `rdk:service:discovery`), or by keyword.
2. **Search from your machine's CONFIGURE tab.** Click **+** then **Configuration block**. The model search shows registry modules alongside built-in models.

When you find a candidate, open its registry page and check:

- **Source.** Modules whose first triplet element is `viam` are officially supported. Others are community-published.
- **Version maturity.** Stable semver releases (`1.0.0` or higher) signal the author considers the module production-ready.
- **Platform support.** Confirm the module builds for your machine's OS and architecture.
- **README.** Look for configuration examples, hardware tested against, and known limitations.

## When to build your own module

Write your own module when:

- No existing module covers your hardware or use case after a thorough search.
- An existing module is close but missing a feature you need. Consider opening an issue or contributing the change before forking.
- You have licensing, security, or compliance requirements that require source control.

If you do build, the rest of this section walks through the workflow:

- [Anatomy of a module](/build-modules/module-anatomy/) for the structural overview.
- [Write a driver module](/build-modules/write-a-driver-module/) for new hardware.
- [Write a logic module](/build-modules/write-a-logic-module/) for control logic and orchestration.
- [Write an inline module](/build-modules/write-an-inline-module/) to prototype in the browser.

## Related pages

- [How components work](/hardware/configure-hardware/) for adding a registry module's resource to a machine.
- [Deploy software](/fleet/deploy-software/) for rolling out a module to many machines.
