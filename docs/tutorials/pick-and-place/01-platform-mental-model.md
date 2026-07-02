---
title: "Phase 1: Platform mental model"
linkTitle: "1. Platform mental model"
type: "docs"
slug: "platform-mental-model"
weight: 10
description: "Understand how the Viam cloud, agent, and server fit together before you configure anything."
workshop: "pick-and-place"
toc_hide: true
phase: 1
phase_total: 6
time_estimate: "15 minutes"
next: "/tutorials/pick-and-place/configure-resources/"
languages: ["python"]
---

Before you configure a single resource, this phase gives you the mental map you need to understand what happens when you make an API call, why config changes appear instantly on the robot, and how Python code on your laptop talks to hardware on the other side of the room.

{{< workshop-phases >}}

## Three questions to answer first

By the end of this phase you should be able to answer three questions. Keep them in mind as you read, and check yourself against them again at the end.

1. What are the three layers of a Viam machine, and which one does your Python code actually talk to?
2. What is the difference between a component and a service?
3. Why does adding the arm in Phase 2 trigger a download?

You will not write any code or change any configuration in this phase. Instead, you will open your own machine in the Viam app and look at what is already there, so that the concepts below have something real to point at.

## The three layers

<!-- ASSET P0 diagram-three-layers (DIAGRAM): cloud app (source of truth) -> viam-server pulls config; viam-agent supervises; SDK arrow to viam-server. See plans/2026-07-02-pick-and-place-shot-list.md -->

A Viam machine is made of three layers that each do one job:

- **The Viam cloud app** is the source of truth for configuration. When you add a component, change an attribute, or wire up a service, you are editing a JSON document stored in the cloud. The app never runs your robot directly; it describes what should run.
- **viam-agent** runs on the machine itself. It manages the install: it installs, updates, and keeps `viam-server` running, restarts it if it crashes, and provides the initial bootstrap credentials viam-server needs to reach the cloud. Think of viam-agent as the process supervisor, not as the source of your resource config, and not as something you interact with directly during this workshop.
- **viam-server** is the process that does the actual work. It pulls its resource config from the cloud app, starts every component and service that config describes, and exposes them over an API. This is the layer that drives the arm, reads the camera, and runs the vision pipeline.

Open your machine's overview page in the Viam app now and find the status indicator that shows the machine is live. That indicator reflects viam-agent keeping viam-server running and connected to the cloud app, the handoff between all three layers happening continuously in the background.

## How your SDK connects

In Phase 4 you write a Python script that imports the Viam SDK and connects to your machine. That connection goes to `viam-server`, not to the cloud app. The cloud app helps your script locate the machine and authenticate, but once the connection is established, every control API call goes directly to `viam-server` on the robot: moving the arm, reading the camera, calling the vision service.

This matters because it explains why your script keeps working even if your laptop briefly loses its connection to the internet at large but keeps a path to the robot: the cloud app is not in the request path for control, only for discovery and configuration delivery.

Open the **CONNECT** tab on your machine's page in the Viam app and look at the code sample it generates. The address and API key shown there are exactly what your Phase 4 script will use to reach `viam-server`.

## Configuration is the source of truth

Whatever you set in the app's **CONFIGURE** tab is what the machine runs. There is no separate step to "deploy" a change: when you save an edit, the cloud app updates the config document, and `viam-server` picks up the new config and applies it, typically within seconds, without a restart for most changes.

This is why the workshop asks you to make changes in the app rather than by editing a file on the robot directly. The app's CONFIGURE tab is the only place you need to look to know what a machine will do.

Open the **CONFIGURE** tab now and find the JSON view toggle near the top of the panel. Switching to JSON shows you the exact document that `viam-server` receives, the same resources you see as cards in the builder view, expressed as the config it consumes.

## Resources: the universal abstraction

<!-- ASSET P1 configure-arm1-triplet (UI+): arm-1 in CONFIGURE with its viam:ufactory:xArm6 namespace:family:model highlighted -->

Everything a Viam machine does, hardware and software alike, is modeled as a **resource**. Each resource has a name you choose (like `arm-1`), an API that describes what kind of thing it is (an arm, a camera, a vision service), and a model that identifies the specific implementation.

Open the **CONFIGURE** tab and find `arm-1`. Next to its name you will see a triplet in the form `namespace:family:model`, for example `viam:ufactory:xArm6`. That triplet tells `viam-server` exactly which code to run for this resource: who published it (`namespace`), what family of hardware it belongs to (`family`), and the specific model (`model`).

The same idea applies to `gripper-1` and `cam-1`: each is a resource with a name, an API, and a model, even though one drives a gripper and the other reads a depth camera.

## Components and services

Resources split into two kinds:

- **Components** represent physical hardware. `arm-1`, `gripper-1`, and `cam-1` are all components: each one wraps a piece of hardware and exposes a standard API for it (an arm API with move commands, a camera API that returns images, and so on).
- **Services** represent software capabilities that consume other resources rather than hardware directly. A motion service plans collision-free paths for an arm. Later, in Phase 5, you configure a `shape-detector` vision service that reads frames from `cam-1` and finds blocks by shape, and a `vision-segment` service (model `detections-to-segments`) that takes those detections and turns them into point cloud segments the motion planner can grasp. Neither service is a physical thing; each one composes other resources into a new capability.

Open the **CONTROL** tab and look at the cards laid out for your machine. Each card corresponds to one resource. The arm, gripper, and camera cards let you jog hardware directly; any service card lets you exercise a capability that is built on top of that hardware.

{{< alert title="Foreshadowing" color="note" >}}
You will not configure `shape-detector` or `vision-segment` until Phase 5. For now, just notice the pattern: a service is defined by what other resources it depends on, not by hardware it owns.
{{< /alert >}}

## Builtin resources and modules

Some resources are **builtin**: `viam-server` (also called the RDK, the robot development kit) ships with support for common APIs and a handful of default models out of the box. Most of the interesting functionality on a real machine, though, comes from **modules**: packages that `viam-server` downloads and runs to add support for a specific model.

The `viam:ufactory:xArm6` arm you saw in the CONFIGURE tab is module-provided. In Phase 2, the moment you add that arm to your config, `viam-server` recognizes it does not have `viam:ufactory:xArm6` built in, downloads the module that provides it from the Viam registry, and starts it. You will be able to watch that download and start happen live in the LOGS tab.

Open the **CONFIGURE** tab again and compare `arm-1`'s namespace to the namespace on any resource marked `rdk` (if you see one). A namespace of `rdk` means the model ships inside `viam-server` itself; any other namespace, like `viam` or `erh`, means the model arrives as a module.

## The resource dependency graph

<!-- ASSET P0 diagram-dependency-graph (DIAGRAM): cam-1 -> shape-detector -> vision-segment; arm-1 -> gripper-1 + five pose switches; motion service -->

Resources can depend on each other. A gripper attaches to an arm, so `gripper-1`'s config points at `arm-1`. A vision service reads from a camera, so it depends on `cam-1`. `viam-server` reads these dependencies out of your config and builds a graph, then starts resources in an order that respects it: a resource cannot start until everything it depends on has started.

This is the same pattern you will see again in Phase 5: `vision-segment` depends on `shape-detector`, which depends on `cam-1`. Neither can produce meaningful output until the resource beneath it is running.

Open the **LOGS** tab and look at the startup sequence the next time the machine restarts (you do not need to trigger one now). The order resources come online in the log follows the dependency graph, not the order they appear in the config file.

{{< alert title="Check yourself" color="note" >}}
Before moving to Phase 2, make sure you can answer the three questions from the top of this page: name the three layers and which one your code talks to, what separates a component from a service, and why adding the arm triggers a module download. If any answer feels shaky, re-skim the relevant section above.
{{< /alert >}}

{{< workshop-nav >}}
