---
linkTitle: "Use Viam from an AI agent"
title: "Use Viam from an AI agent"
weight: 5
layout: "docs"
type: "docs"
description: "What an AI agent needs to know to discover, observe, and operate a Viam machine safely: the model, the ways in, and the rules that keep a robot safe when the agent is driving."
capabilities: ["sdks", "motion-planning"]
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

## What the machine will not tell you

Everything below is true of any Viam machine, and none of it is discoverable from the machine's own configuration or method listing. Read it before you plan a motion.

### Moving with the motion service

The motion service plans a path for a component and executes it on the arm. Give it the name of the component you want moved, the destination as a pose in a named frame, and any constraints:

```python
from viam.proto.common import Pose, PoseInFrame
from viam.proto.service.motion import Constraints, LinearConstraint
from viam.services.motion import MotionClient

motion = MotionClient.from_robot(machine, "builtin")

# Move the gripper's frame to a point 100 mm above the block, pointing straight down.
above_block = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=600, y=100, z=880, o_x=0, o_y=0, o_z=-1, theta=0),
)
await motion.move(component_name="pick-grip", destination=above_block)

# Descend on a straight line. Use a linear constraint for the last 100 mm of any
# approach, and for every move while holding something.
straight = Constraints(
    linear_constraint=[LinearConstraint(line_tolerance_mm=5, orientation_tolerance_degs=5)]
)
at_grasp = PoseInFrame(reference_frame="world", pose=Pose(x=600, y=100, z=784, o_z=-1))
await motion.move(component_name="pick-grip", destination=at_grasp, constraints=straight)
```

Plan the long part of the approach as a free move to the standoff pose, then one linear move straight down, and one linear move back up. Keep the linear constraint for that short final segment. A descent built from many small linear steps tends to fail: with a linear constraint the motion service solves for a direct straight line and will not fall back to a curved path, so a single segment with no direct solution returns `linear with cbirrt not allowed and no direct solutions found`. Read that as this exact straight line being infeasible, not the goal being unreachable, and either widen the tolerance or plan that segment as a free move.

`component_name` is the component's name as a string. Earlier versions of the SDKs took a `ResourceName` message here. If you pass one now, the call fails with `bad argument type for built-in operation`, which is the protobuf library rejecting the message where it expects a string. The same applies to `get_pose`.

`get_pose` reports where a component's frame is, in any other frame:

```python
gripper_in_world = await motion.get_pose(component_name="pick-grip", destination_frame="world")
```

### Units and frames

Poses are in millimeters and degrees. Point clouds are in meters. The orientation of a pose is an orientation vector: `o_x`, `o_y`, `o_z` give the direction the frame's z axis points, and `theta` is the roll about it. A gripper pointing straight down at the table has `o_z=-1`.

A vision service returns objects in the frame of the camera it read. To use them as motion targets, convert them with `transform_pose` on the machine client, which applies the frame system:

```python
from viam.proto.common import PoseInFrame

camera_frame_center = PoseInFrame(reference_frame="wrist-cam", pose=obj.geometries.geometries[0].center)
world_center = await machine.transform_pose(camera_frame_center, "world")
```

The frame system holds fixed things: the arm's base, the cameras, the table, a place pad. Read it with `get_frame_system_config`. Things that move are not in it. Read those from vision services, and pass them to `move` as obstacles in a `WorldState` when a path must avoid them.

### Waiting

Pass a timeout on every call. A camera or vision read that takes more than a few seconds is stuck, not slow, and a call without a deadline waits forever. If a call does not return, `get_operations` on the machine client lists it, and `cancel_operation` ends it.

Some drivers report `is_moving` as true while the arm is still. Judge motion by change in joint positions over a short window, not by that flag.

### Grasping

Grasp at or above the object's center height. A grasp near the surface it rests on stalls the jaw on that surface, not on the object.

`grab` returns whether the gripper holds something. `is_holding_something` is the check to make after any move while carrying. When a client's session ends, viam-server stops every actuator that session commanded. A gripper that holds an object keeps holding it. A gripper that closed on nothing stops where it is, with no force, until the next command.

### Looking

Read cameras from 300 mm or more above an object. Closer than that, the gripper's own fingertips enter the frame and color detectors find them. Check a vision result once against an independent depth read, then trust it; the check costs one call, rebuilding perception costs ten minutes. The first frame after a machine boots can be stale. If a reading is far from where the scene should be, read again.

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
