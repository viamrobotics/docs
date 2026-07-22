---
linkTitle: "WorldState"
title: "WorldState"
weight: 10
layout: "docs"
type: "docs"
description: "What a WorldState is: the per-request set of obstacles and frame transforms you pass to a single Move call for the planner to plan around."
---

A `WorldState` is the argument you pass to a single `Move` call. It carries the obstacles
and frame transforms that the motion planner should account for on that one request. When
the call returns, the `WorldState` is gone.

## What a WorldState carries

A `WorldState` holds two kinds of item:

- **Obstacles**: geometries the planner treats as things to avoid, each expressed in a
  reference frame. Use them for objects that are not part of the machine's configured frame
  system, such as a pallet detected at runtime.
- **Transforms**: frames added to the frame system for this request only. A transform can
  reposition where the arm moves (for example, a frame at a grasped object's tip) or carry a
  geometry that travels with a component.

## A WorldState applies to one request

A `WorldState` is per-request. The motion service uses it to plan the single motion you
attach it to, then discards it. To carry the same obstacles into a later `Move` call, pass
a `WorldState` again. To build obstacles and transforms and attach them to a
`Move` call, see [Define obstacles](/motion-planning/obstacles/) and
[Arm and end effector frames](/motion-planning/frame-system/end-effector-frames/).

## WorldState versus the world state store service

The names are similar, but the two are different things, and only one affects a plan:

- **`WorldState`** is planner input. The obstacles and transforms in it shape the motion the
  planner computes for one `Move` call.
- The [world state store service](/reference/apis/services/world-state-store/) is
  visualization output. It holds transforms that the 3D scene draws, and the planner never
  reads it.

The same geometry can take both paths, but they are separate: put it in a `WorldState` for
the planner to avoid, and publish it to the world state store service for the scene to draw.
