---
title: "Phase 1: Platform mental model"
linkTitle: "1. Platform mental model"
type: "docs"
slug: "platform-mental-model"
weight: 10
description: "Understand how the Viam cloud, agent, and server fit together before you configure anything."
workshop: "pick-and-place"
phase: 1
phase_total: 5
time_estimate: "15 minutes"
next: "/tutorials/pick-and-place/configure-resources/"
languages: ["python"]
---

Before you configure a single resource, this phase gives you the mental map you need to understand what happens when you make an API call, why config changes appear instantly on the robot, and how Python code on your laptop talks to hardware on the other side of the room.

{{< workshop-phases >}}

## Three questions to answer first

<!-- TODO: pose and answer the three orienting questions from slides Phase 1 that frame why the Viam model is different from a traditional robotics SDK. -->

## The three layers

<!-- TODO: diagram and explanation of cloud platform, viam-agent, and viam-server from slides Phase 1. Cover how they communicate and which layer holds what. -->

## How your SDK connects

<!-- TODO: explain the WebRTC / gRPC signaling flow from slides Phase 1 showing the laptop SDK connecting through the cloud to viam-server on the robot. -->

## Configuration is the source of truth

<!-- TODO: explain the JSON config model from slides Phase 1: config lives in the cloud, viam-server pulls and applies it, and changes propagate without restarting the server. -->

## Resources: the universal abstraction

<!-- TODO: define what a resource is from slides Phase 1, including name, API (type + subtype), and model triple. -->

## Components and services

<!-- TODO: contrast components (hardware abstractions) with services (algorithms that consume components) using examples from slides Phase 1. -->

## The resource dependency graph

<!-- TODO: show how the dependency graph is derived from the config and why order of initialization matters, from slides Phase 1. -->

{{< workshop-nav >}}
