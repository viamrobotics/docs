---
title: "Resource APIs with Viam's SDKs"
linkTitle: "Resource APIs"
weight: 40
type: "docs"
description: "Using built-in resource API methods to control the components and services on your robot with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

INTRODUCTION Similar info to modular resources re. resource definitions and namespacing, "what is a resource," what is an API.
Talk about how these methods work --> providing wrapper for gRPC client request to these endpoints, which are how you access/interface with the components you have configured on your robot/`viam-server`.

## Resource Base API

Description, methods.

### ResourceName

### FromRobot

### GetOperation

### DoCommand (hmmm)

## Component APIs

INTRODUCTION: What do these do?

Table with methods? 
- [Arm](/components/arm/#api)
- [Base](/components/base/#api)
- [Camera](/components/camera/#api)
- [Gantry](/components/gantry/#api)
- [Gripper](/components/gripper/#api)
- [Input Controller](/components/input-controller/#api)
- [Motor](/components/motor/#api)
- [Movement Sensor](/components/movement-sensor/#api)
- [Sensor](/components/sensor/#api)
- [Servo](/components/servo/#api)

## Service APIs

INTRODUCTION: What do these do?

Table with methods?
- [Motion](/services/motion/#api)
- [SLAM](/services/slam)
- [MlModel](/services/ml)
- [Vision](/services/vision)

Might be long WIP fully building out here as SLAM, MlModel, Vision client methods are most extensively documented in SDKs, and Sensors service is a bit murky.
Could have tables linking to Go and Python SDK docs for now.

- [Frame System](/services/frame-system/#api)
^^ Tricky, might need explanation.

## Additional Interfaces

Need to think of better name here...

- Reference for GPIOPin etc api methods.
