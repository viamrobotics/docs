---
linkTitle: "Overview"
title: "App tutorials"
weight: 1
layout: "docs"
type: "docs"
description: "Guided end-to-end projects that build a working Viam app you can run. Pick by UI shape, machine scope, and language."
date: "2026-04-20"
---

Each tutorial in this section builds one small but complete Viam app end-to-end, from empty project directory to a program you can run against your own machine. The tutorials assume your project is already scaffolded, see [App scaffolding](/build-apps/setup/overview/) for the prerequisite setup.

## Pick a tutorial

| Tutorial                                                                            | Language                        | Shape             | Scope              | What it builds                                                                                                                                                                               |
| ----------------------------------------------------------------------------------- | ------------------------------- | ----------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Single-machine dashboard](/build-apps/app-tutorials/tutorial-dashboard/)           | TypeScript (browser)            | Web UI            | One machine        | Camera feed, live sensor reading, motor start/stop button, connection status. Introduces the core client pattern: connect, fetch resources by name, call component APIs.                     |
| [Multi-machine fleet dashboard](/build-apps/app-tutorials/tutorial-fleet/)          | TypeScript (browser)            | Web UI            | Organization fleet | Lists every machine in your org and shows aggregated sensor readings from each. Introduces cloud-scoped API keys and MQL aggregation over captured data.                                     |
| [Flutter app with widgets](/build-apps/app-tutorials/tutorial-flutter-app/)         | Flutter (iOS, Android, desktop) | Mobile/desktop UI | One machine        | Camera, sensor, and motor control using the prebuilt Flutter widgets (`ViamCameraStreamView`, `ViamSensorWidget`, `ViamMotorWidget`). Introduces the widget-based approach for Flutter apps. |
| [Python monitoring service](/build-apps/app-tutorials/tutorial-monitoring-service/) | Python                          | Headless service  | One machine        | Non-UI process that polls a sensor on a schedule and drives a motor based on the reading. Introduces the headless-service pattern and clean shutdown.                                        |

## Before you start

Every tutorial assumes you have a scaffolded project for the target language and a reachable machine. If you haven't set up a project yet, work through [App scaffolding](/build-apps/setup/overview/) first, it covers project creation, SDK installation, credentials, and a connection verification step that every tutorial builds on.
