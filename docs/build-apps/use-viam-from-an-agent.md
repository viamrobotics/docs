---
linkTitle: "Use Viam from an AI agent"
title: "Use Viam from an AI agent"
weight: 5
layout: "docs"
type: "docs"
description: "What an AI agent needs to know to discover, observe, and operate a Viam machine safely: the model, the ways in, and the rules that keep a robot safe when the agent is driving."
date: "2026-09-03"
---

An AI agent with a shell or an SDK can operate a Viam machine the same way a person or a program can.
This page is written for the agent, or for the person setting one up.
It covers what a machine is made of, how to reach it, what to do before moving anything, and what the platform does for you when things go wrong.

If you already have a key and a terminal, the shortest path is [Drive a machine from the CLI](/cli/drive-a-machine/).

## The model in one screen

- A **machine** is a robot or device running `viam-server`.
  It has one or more **parts**; the main part is the one you talk to.
- A part serves **resources**: **components** (hardware such as an arm, a camera, a gripper, a motor) and **services** (software such as motion planning, vision, or data management).
  Every resource has an **API** (its type, for example `rdk:component:arm`), a **model** (the implementation, often from a module), and a **name**.
- Every API is defined in protobuf and served over gRPC.
  The machine can list its resources and describe its methods at runtime, so you can learn a machine without documentation for its hardware.
- The **frame system** is the machine's kinematic tree: where each component is relative to its parent and to the `world` frame.
  The motion service plans against it.
- A **key** authenticates you.
  Keys are scoped to a machine, a location, or an organization.
  Today every key minted from the CLI has full write access to its scope, and a machine checks only that a key is valid, not what it may do.

## Ways in

| Path | Use it when                                                                                                                                      | Guide                                                                                                                      |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| CLI  | You have a shell. One command calls any API method with JSON in and JSON out; no code to write.                                                  | [Drive a machine from the CLI](/cli/drive-a-machine/)                                                                      |
| SDK  | You need to hold state across steps (a grasp, then a lift, then a place), stream frames, or run a loop. One long-lived client keeps one session. | [Connect to a machine](/build-apps/tasks/connect-to-machine/), [Control components](/build-apps/tasks/control-components/) |

The two paths call the same API.
Anything you can do with one you can do with the other; the difference is whether you want a process that stays connected.

## Look before you move

The order that works, and the reason for each step:

1. **List the resources** (`ResourceNames`) and **their state** (`GetMachineStatus`).
   A resource that is still configuring or unhealthy will fail every call; the status says why.
2. **Read the frame system** (`FrameSystemConfig`) and each component's **kinematics and geometry**.
   That tells you which frames exist, what is attached to what, and what the planner already knows about.
3. **Observe** before acting: an image, a point cloud, a sensor reading.
   A vision service can return an image, detections, and object point clouds in one call (`CaptureAllFromCamera`).
4. **Plan motion through the motion service** rather than commanding joints or poses directly.
   `Move` takes a goal pose in any frame, plus obstacles and constraints you declare, and returns collision-checked motion against the frame system's geometry.
   The arm's own `MoveToPosition` is unplanned.
5. **Verify by observation, not by return value.**
   A gripper's `Grab` reporting success does not prove it lifted anything; look, or call `IsHoldingSomething` after the lift.

Two known limits of perception worth planning around: a 3D segmenter's bounding-box center can include background points behind an object's edges, so it reads farther from the camera axis than the object is; and depth is least reliable at the near edge of a camera's range.
Observing from directly above an object, from a moderate height, avoids both.

## What the platform does for you

- **Stops actuators when your session ends.**
  Each client connection carries a heartbeat.
  If it lapses because your process exits or crashes, the machine stops the actuators that session commanded, within about two seconds.
  Consequences: from the CLI each command is its own session, so a motion started by one command stops when that command exits; and on some gripper models the stop releases the drive, dropping what it holds.
  Sequences that must hold an object belong in one process with one client.
- **Names every operation and lets you cancel it.**
  `GetOperations` lists what is running; `CancelOperation` stops one; `StopAll` stops everything in one call.
- **Refuses motion it cannot plan.**
  A goal inside the table, or inside an obstacle you declared, fails with an error that names the constraint.
- **Converges configuration.**
  When you add a component or service, the machine applies it within about ten seconds; `GetMachineStatus` reports the revision it reached and each resource's state.

Two things the heartbeat does not cover today: motion-service moves continue after the client that started them disappears, and there is no per-resource permission or approval step.
A key that can read a camera can also move an arm.
Use `StopAll` when a move must end, and give an agent a machine-scoped key rather than a location or organization key when it only needs one machine.

## Remembering across sessions

Machines, parts, locations, and organizations each carry a metadata document you can read and write through the app API: a place for notes such as calibration offsets or what worked last time.
It is a single JSON object replaced whole on every write, with no revision check, so two writers can overwrite each other; keep notes small and read before you write.

## Growing the machine

A procedure that works can become a permanent capability of the machine.
`viam module generate` scaffolds a module, `viam module reload` hot-loads it onto the running part, and the new resource then appears in `ResourceNames` like any built-in.
See [Build and deploy modules](/cli/build-and-deploy-modules/).

## Reading errors

| Error                                                                            | Meaning                                                                                             |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `resource rdk:component:arm/my-arm not found`                                    | Wrong name or not configured; check `ResourceNames`.                                                |
| `Unimplemented`                                                                  | This model does not implement that method. No further detail is given.                              |
| `all IK solutions failed constraints. Failures: { obstacle constraint: 62.00% }` | The planner could not reach the goal; the percentages say which constraint blocked most candidates. |
| `arm stalled at waypoint 2/2 (stuck joints: j3: at 110.0 want 118.8)`            | The arm hit something during execution.                                                             |
| `modular resource config validation error: context deadline exceeded`            | The module did not answer in time, usually because it is still starting.                            |

## Next

- [Drive a machine from the CLI](/cli/drive-a-machine/): every command above, with the exact method names and request shapes.
- [Connect to a machine](/build-apps/tasks/connect-to-machine/) and [Control components](/build-apps/tasks/control-components/) for the SDK path.
- [Motion service](/motion-planning/) for planning, obstacles, and constraints in depth.
