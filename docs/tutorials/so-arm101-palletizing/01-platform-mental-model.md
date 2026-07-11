---
title: "Phase 1: The platform and the miniature cell"
linkTitle: "1. Platform mental model"
type: "docs"
slug: "platform-mental-model"
weight: 10
description: "How your laptop, the arm's host, and Viam fit together, and the three ideas this workshop is built on."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 1
phase_total: 6
time_estimate: "15 minutes"
next: "/tutorials/so-arm101-palletizing/configure-the-arm/"
languages: ["python"]
draft: true
---

Before you configure anything, this phase gives you a mental model of the cell you are about to build and the platform it runs on. You will not touch config or code yet, but every phase after this one leans on the ideas introduced here.

## What you'll build

You are building a miniature palletizing cell. An SO-ARM101 arm picks cubes, one at a time, from a staging spot and stacks them on a small pallet: two layers of four, eight cubes total. The arm and its gripper are the hardware; a set of hand-taught poses and, later, your own Python code, are what turn that hardware into a working pack sequence.

<!-- ASSET diagram-cell-layout (DIAGRAM): arm base, staging spot, 2x2 pallet grid, two layers -->

## How your laptop, the arm's host, and Viam fit together

A Viam machine has three parts working together, and it helps to know which one does what before you start configuring.

The Viam cloud app, at [app.viam.com](https://app.viam.com), holds your machine's configuration: the arm and gripper you add, the poses you save, and any services you configure. It is the source of truth for what the machine should run, not something that talks to the arm directly.

On the host, either a Raspberry Pi or a laptop, two programs do the work. `viam-agent` supervises `viam-server`: it installs it, keeps it running, and restarts it if it crashes. `viam-server` reads the configuration from the cloud app, starts the resources it describes, and exposes them over an API. The SO-ARM101 itself connects to this host over a USB serial cable; `viam-server` talks to the arm's motors through that connection.

Your Python code runs from your own laptop, separate from the host. When your script connects to the machine, it reaches `viam-server` over the network, using the address and credentials from the machine's **CONNECT** tab. The cloud app helps your script find and authenticate to the machine, but the actual move commands travel straight to `viam-server` on the host.

## Components and services

Everything a Viam machine does is modeled as a resource, and resources split into two kinds.

The arm and the gripper are **components**: each one wraps a piece of physical hardware and exposes an API for it. An arm component moves to a pose; a gripper component opens and closes.

The frame system and the motion service are **services**: software that reasons about the components rather than being hardware itself. The frame system tracks where every object in the cell sits relative to the arm's base. The motion service uses that information to plan a path from where the arm is to where it needs to be, without colliding with anything along the way.

## The three ideas this workshop is built on

Three concepts carry the whole workshop. This section only previews them; you will work with each one directly in a later phase.

The **frame system** answers "where is everything, relative to the arm?" Every pose you teach, and every obstacle you configure, is expressed as a position relative to the arm's base frame. Once something has a place in the frame system, the arm and the motion service can reason about it.

**Motion planning** answers "how does the arm get there?" Given a target pose, the motion service works out a path of joint movements that reaches it. You will not write this logic yourself; you call the motion service and it does the planning.

**WorldState** answers "what must the planner avoid?" It is the set of obstacles, expressed in the frame system, that the motion service treats as solid. In this workshop, WorldState grows as you pack: once a cube is sitting on the pallet, it becomes an obstacle the planner must route around when placing the next one.

## Why a real arm changes the job

The simulated Viam 101 course hands you the coordinates of every object in the cell: the pick station, the pallet, and each box already have a frame. On real hardware, nothing comes pre-measured. You have to map the physical world, the staging spot and the pallet grid in front of you, into the arm's frame yourself. You will do exactly that by hand in Phase 3, jogging the arm to each anchor point and recording where it is.

The SO-ARM101 is a five degree-of-freedom (5-DOF) arm, one fewer than the six-axis arms used in many industrial cells. On a top-down grasp, that missing degree of freedom couples the wrist's yaw to the rest of the approach: you cannot set an arbitrary wrist rotation independently of the arm's position the way a 6-DOF arm can. In this workshop that coupling does not matter, because the cubes are rotationally symmetric: however the gripper's fingers land on a cube's sides, the grasp works.

{{< checkpoint >}}
Open your machine in the Viam app and confirm the green **Live** indicator. You should be able to name the two components you will configure (arm and gripper) and the two services that will move the arm (frame system and motion). If your machine is not Live, start `viam-server` on the host before continuing.
{{< /checkpoint >}}

{{< workshop-nav >}}
