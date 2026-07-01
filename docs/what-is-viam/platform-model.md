---
linkTitle: "How Viam fits together"
title: "How Viam fits together"
weight: 20
layout: "docs"
type: "docs"
description: "A tour of Viam's core vocabulary, machine, part, component, service, module, and modular resource, for developers new to robotics."
aliases:
  - "/concepts/platform-model/"
  - "/concepts/"
---

Picture a small delivery robot: two motors, a camera up front, a GPS unit, and a single-board computer that ties them together.
In Viam terms, that whole robot is a **machine**.
The software brain running on its computer is a program called `viam-server`, built on Viam's Robot Development Kit (RDK).
`viam-server` is what your code talks to, and it is the piece that turns a pile of hardware and algorithms into something you can drive from a uniform API.

Everything else in the Viam vocabulary describes how that machine is organized and how you extend it.
Once these words click, the rest of the documentation reads much more smoothly.

## Machines and parts

A **machine** is the logical unit you configure and control: our delivery robot, a conveyor cell, or a camera-only sensor station.

A **part** is one running instance of `viam-server` that belongs to a machine.
Most machines have exactly one part, so in practice "machine" and "part" often point at the same physical computer.
The distinction matters when a single machine spans more than one computer, for example, a robot arm on one board and a vision workstation on another, coordinated as one machine.
Each computer runs its own part, and the parts connect so that your code sees one machine with one address.
When you read about a machine "having a main part" or "sub-parts," this is the idea at work.

## Components and services

Inside a part, capabilities are grouped into two families.

A **component** represents a piece of hardware you drive: a motor, a camera, a GPS movement sensor, an arm.
Each kind of component has a standard API, so every camera responds to the same image-capture method regardless of the vendor, and every motor responds to the same set-power and stop methods.
This uniformity is the point, you write against the camera API, and swapping a USB webcam for an industrial camera does not change your code.

A **service** provides higher-level software capability that usually builds on top of components.
The vision service runs object detection on frames from a camera; the motion service plans a path and commands an arm to follow it; the navigation service drives a base toward a destination.
Services also present standard APIs, so a detector-based vision service and a segmentation-based one answer the same detection methods.

The clean way to keep them straight: a component is a thing the machine controls, and a service is a capability the machine performs.
Both are **resources**, the general word for any configured, API-addressable element of a machine, and both are reached through `viam-server` in exactly the same style.

## Models and APIs

An **API** defines _what_ methods a resource answers, the camera API, the motor API, the vision service API.
A **model** is a specific _implementation_ of one of those APIs.

The camera API is a single contract, but a Logitech webcam, a RealSense depth camera, and a simulated fake camera are three different models that all satisfy it.
When you configure a component or service, you choose a model, and behind that model sits real code that fulfills the API.
Models are named with a triplet, `namespace:family:name`. The built-in webcam is `rdk:builtin:webcam`; a community model might be `myorg:realsense:d435`. The middle slot is the model's _family_, not the API it implements, and the namespace keeps a community-contributed model distinct from Viam's own.

## Modules and modular resources

Viam ships with many built-in models, but the platform is designed to be extended, and this is where modules come in.

A **module** is a packaged program that adds one or more new models to `viam-server`.
The individual capability a module contributes, the configured camera or the custom vision routine you get out of it, is a **modular resource**.
A modular resource implements a standard component or service API, so once it is running it looks and behaves like any built-in resource: the same methods, the same tooling, the same client code.

Modules are shared through the **registry**, Viam's catalog of models.
When you add a model from the registry to a machine, `viam-server` downloads the module, launches it, and manages its lifecycle.
Your configuration names a model; the module supplies the implementation; the API guarantees that the rest of your system does not need to know which module is behind it.
This is what lets a hobbyist's sensor driver and a vendor's official one slot into the same machine interchangeably.

## Two ways you write code

As a developer, you meet Viam from one of two directions, and telling them apart clears up a lot of early confusion.

When you write a **client script**, _you_ are the caller.
Your program connects to a machine, gets a handle to a resource, and calls its API methods, read this sensor, move that arm, run detections on this camera.
Control flows outward from your code into the machine, and this is how most applications, dashboards, and automations are built.
See [Control a machine](/hardware/) for this path.

When you **author a module**, the relationship inverts: _the platform_ is the caller.
You implement the methods of a component or service API, and `viam-server` invokes your code whenever a client asks that resource to do something.
Instead of calling `get-image`, you are the one who answers `get-image` when a request arrives.
Your module registers its model, and from then on it serves requests rather than sending them.
See [Build modules](/build-modules/) for this path.

The same API sits between both roles, which is the elegant part: a client script written against the camera API works identically whether the camera is a built-in model or a modular resource you wrote yourself.
Learn one API contract and you understand both sides of it.

## Putting it together

Back to the delivery robot.
The machine is the robot; its one part is `viam-server` on the onboard computer.
The motors, camera, and GPS are components; a vision service and a navigation service supply the higher-level behavior.
If the stock GPS driver does not fit the specific hardware, someone publishes a module to the registry whose modular resource implements the movement sensor API, and the machine uses it exactly like a built-in one.
An operator's phone app is a client script that calls these APIs to send the robot on its way.

With this vocabulary in place, the rest of the documentation, configuration, module development, fleet management, describes variations on these same relationships.

## Next steps

- [Configure and control a machine](/hardware/), put components and services on a real part and drive them.
- [Build a module](/build-modules/overview/), author your own modular resource against a standard API.
- [Machine architecture reference](/reference/machine-to-machine-comms/), a closer look at how parts, resources, and `viam-server` connect.
