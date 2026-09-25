---
title: "Services reference"
linkTitle: "Services"
weight: 30
type: "docs"
layout: "docs"
no_list: true
description: "Configuration reference for Viam built-in services: per-service models, attributes, and JSON templates."
capabilities: ["section-index"]
diataxis: overview
date: "2026-04-14"
aliases:
  - /operate/reference/services/
---

Built-in services are software capabilities that ship with [`viam-server`](/reference/viam-server/).
Unlike hardware drivers, which talk to a specific piece of equipment, services provide advanced capabilities that often work across many components, such as motion planning coordinating clear paths for an arm around obstacles.

Because they are built in, you can add built-in services to any machine's configuration without installing a separate module.
If a built-in service doesn't fit your use case, you can also find community and Viam-maintained service models in the [Viam registry](https://app.viam.com/registry) or [build your own](/build-modules/overview/).

Each page below covers available models, configuration attributes, and JSON templates.
For API method reference, see [Service APIs](/reference/apis/services/).

| Service                                             | Description                                                                                                |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [Base remote control](/reference/services/base-rc/) | Drive a mobile base with an input controller like a gamepad or joystick                                    |
| [Discovery](/reference/services/discovery/)         | Detect available hardware on a machine and suggest component configurations                                |
| [Frame system](/reference/services/frame-system/)   | Store spatial relationships between components so other services can reason about position and orientation |
| [Generic](/reference/services/generic/)             | A catch-all API for services that don't fit other service types                                            |
| [Motion](/reference/services/motion/)               | Plan and execute movement for components relative to themselves, other machines, and the world             |
| [Vision](/reference/services/vision/)               | Add computer vision capabilities like detection, classification, and segmentation to cameras               |
