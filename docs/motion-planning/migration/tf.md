---
linkTitle: "From TF"
title: "Frame system for ROS TF users"
weight: 30
layout: "docs"
type: "docs"
description: "Concept mappings from ROS tf/tf2 to Viam's frame system, including REP-105 conventions and pose query equivalents."
---

ROS TF is the canonical way to reason about coordinate frames in the
ROS world: a publisher-subscriber tree of named frames with
time-stamped transforms. Viam's frame system is the conceptual
equivalent but is structured differently in a few ways that matter for
users porting designs over.

## Concept mapping

| ROS TF / tf2 concept                              | Viam equivalent                                                                                   |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| TF tree                                           | [Frame system](/motion-planning/frame-system/) — a tree of named frames rooted at `world`.        |
| TF2                                               | Same frame system. Viam has one TF implementation, not two.                                       |
| REP-105 (`map` → `odom` → `base_link`)            | `world` → components. No separate map/odom distinction in the tree.                               |
| Static broadcaster (`static_transform_publisher`) | Frame config on a component with fixed `translation` and `orientation`.                           |
| Dynamic broadcaster                               | Components with `framesystem.InputEnabled` (arm, gantry) update their own frames as they move.    |
| `tf2_echo`                                        | [`viam machines part motion print-status`](/motion-planning/reference/cli-commands/#print-status) |
| `tf_monitor`, `tf2_tools` view_frames             | [3D scene tab](/motion-planning/3d-scene/) in the Viam app.                                       |
| `lookup_transform` / `transform_frames`           | [Robot service `GetPose` and `TransformPose`](/motion-planning/reference/frame-system-api/)       |
| TF message time stamps / interpolation            | Viam looks up frames at the current time. No time travel.                                         |
| `tf_prefix` / frame namespacing                   | Frame system is per-machine. Cross-machine frame sharing is not supported.                        |
| `robot_state_publisher` from URDF                 | The arm module reads URDF (or SVA) and contributes its joints to the frame system automatically.  |

## Writing the same pose lookup

In ROS 2 (Python, with tf2):

```python
from tf2_ros import Buffer, TransformListener
from rclpy.node import Node

node = Node("lookup")
buffer = Buffer()
listener = TransformListener(buffer, node)

# Later, after spinning the node for a bit:
tr = buffer.lookup_transform(
    target_frame="world",
    source_frame="gripper",
    time=rclpy.time.Time(),
)
```

In Viam (Python):

```python
gripper_in_world = await machine.get_pose(
    component_name="my-gripper",
    destination_frame="world",
)
```

No buffer, no node to spin, no separate listener. The robot client
already has access to the frame system; `get_pose` returns the
current pose synchronously.

## What transfers

- **URDF support.** Point the arm module at a URDF file. Viam's
  planner consumes the same format ROS does, plus a Viam-native SVA
  JSON format with equivalent expressive power. See
  [Arm kinematics](/motion-planning/reference/kinematics/).
- **Tree-based frame model.** Parent/child relationships, translation,
  rotation, and propagation all work the way you expect.
- **Pose lookup semantics.** `GetPose` answers the same question as
  `lookup_transform`.
- **Supplemental transforms.** TF's dynamic broadcaster pattern maps
  to Viam's `WorldState.transforms`, applied per motion-service call.
  See [Attach and detach geometries](/motion-planning/motion-how-to/attach-detach-geometries/).

## What is different

- **REP-105 is not the tree.** ROS puts `map` at the root, with `odom`
  between `map` and `base_link` so that drift correction happens on
  the `map → odom` edge. Viam's tree is rooted at `world`. If you need
  the drift-correction pattern, implement it in application code: the
  frame system itself is not structured for a separate localization-
  estimate frame between the world and your base.
- **No timestamps, no time travel.** ROS TF interpolates between
  timestamped transforms so you can ask "where was the gripper 500ms
  ago?". Viam's frame system answers "where is the gripper now"
  and has no time dimension. For historical queries, capture poses in
  application code.
- **No prefix-based namespacing.** Each machine has a single frame
  system. You cannot ask one machine for another machine's gripper
  pose through the frame system; cross-machine coordination lives in
  application logic.
- **xacro is not expanded.** If your URDF is authored as xacro, run
  xacro once to produce a URDF and load that.

## What you lose

- **Time-stamped history.** You will not be able to look up a past
  pose through the API.
- **Cross-machine frame sharing.** In a fleet, each machine's frame
  system is isolated.
- **Arbitrary custom broadcasters.** You cannot register a process
  that publishes new frames into the tree at will; frames are
  configuration-defined or produced by a component with
  `framesystem.InputEnabled`.

## What you gain

- **No tf daemon to run.** The frame system is always available
  through the machine client. No `tf_buffer.spin_until_future_complete`.
- **Configuration-driven.** Frames are part of the component's JSON
  config. They deploy with the machine, survive restarts, and travel
  through fragments in a fleet.
- **CLI inspection.**
  [`viam machines part motion print-config`](/motion-planning/reference/cli-commands/#print-config)
  and `print-status` give you immediate "what does the robot think the
  world looks like" answers without writing code or spinning nodes.
- **Integration with the motion service.** The planner already sees
  the frame system; you do not have to wire it in.

## What's next

- [Frame system](/motion-planning/frame-system/): the concept page.
- [Frame system API](/motion-planning/reference/frame-system-api/):
  the RPCs (which live on the robot service, not a dedicated frame
  system service).
- [Motion CLI commands](/motion-planning/reference/cli-commands/):
  the `tf2_echo` equivalents.
- [Debug motion with the CLI](/motion-planning/motion-how-to/debug-motion-with-cli/):
  symptom-driven debugging flows.
