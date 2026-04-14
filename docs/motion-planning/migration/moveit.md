---
linkTitle: "From MoveIt"
title: "Motion planning for MoveIt users"
weight: 10
layout: "docs"
type: "docs"
description: "Concept mappings from MoveIt (ROS) to Viam's motion service for users evaluating a migration or building on top of Viam."
---

If you have shipped arm applications with MoveIt, the mental model
transfers reasonably cleanly: Viam's motion service is a planner-plus-
executor that takes a target pose and produces a collision-free arm
motion, much as `move_group` does. The shape of the API and the set of
configuration files are different.

## Concept mapping

| MoveIt concept                     | Viam equivalent                                                                                                                   |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `move_group`                       | [Motion service](/motion-planning/reference/motion-service/), specifically its `Move` method                                      |
| Planning Group                     | Implicit. Planning targets a single component at a time; no explicit group definition.                                            |
| Planning Scene                     | [`WorldState`](/motion-planning/obstacles/#worldstate), passed per-call. No persistent scene.                                     |
| Planner (OMPL-based family)        | cBiRRT, a constrained bidirectional RRT. Single algorithm. See [How motion planning works](/motion-planning/how-planning-works/). |
| IK solver (KDL, Trac-IK, Pick IK)  | NLopt, internal. No user-exposed solver selection.                                                                                |
| SRDF                               | Not needed. Arm modules declare their own kinematics and planning groups internally.                                              |
| Setup Assistant                    | JSON config in the Viam app. No generated launch files.                                                                           |
| URDF                               | Supported. Also a Viam-native SVA JSON format. See [Arm kinematics](/motion-planning/reference/kinematics/).                      |
| xacro                              | Not supported. Expand to URDF before loading.                                                                                     |
| Self-filter / body padding         | [`CollisionSpecification`](/motion-planning/motion-how-to/allow-frame-collisions/) with `AllowedFrameCollisions`.                 |
| `trajectory_msgs::JointTrajectory` | The motion service returns a plan internally; your code calls `Move` or the arm's `MoveToJointPositions`.                         |
| `attach_object` / `detach_object`  | [`WorldState.transforms`](/motion-planning/motion-how-to/attach-detach-geometries/), per-call.                                    |
| PILZ Industrial Motion Planner     | Not directly comparable. For industrial-grade straight-line moves, use `LinearConstraint`.                                        |
| Task Constructor                   | Application-level orchestration. Viam does not ship a task-composition framework.                                                 |

## Writing the same motion

In MoveIt (C++):

```cpp
move_group::MoveGroupInterface group("manipulator");
geometry_msgs::Pose target;
target.position.x = 0.3;
target.position.y = 0.2;
target.position.z = 0.4;
target.orientation.w = 1.0;
group.setPoseTarget(target);
group.move();
```

In Viam (Python, same task):

```python
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

target = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=300, y=200, z=400, o_x=0, o_y=0, o_z=-1, theta=0),
)

await motion_service.move(component_name="my-arm", destination=target)
```

Both invocations plan around obstacles known to the planner, handle
kinematics internally, and block until motion completes or fails.
Viam's units are millimeters and degrees; MoveIt uses meters and
quaternions.

## What transfers

- **URDF descriptions** work as-is. Point your arm module at the URDF,
  or use Viam's SVA JSON format.
- **Collision geometry** maps directly. Boxes, spheres, and capsules
  are the common primitives in both systems; Viam also supports
  meshes.
- **Constraint types** have analogs. MoveIt's path constraints
  correspond to Viam's `LinearConstraint` and `OrientationConstraint`;
  MoveIt's allowed collision matrix is the `CollisionSpecification`.
- **Obstacle avoidance** is integrated into `Move`, as it is in
  `move_group.move()`.

## What is different

- **No persistent Planning Scene.** Each `Move` sees the world you
  pass in through `WorldState`. There is no long-lived scene
  monitored by external processes. Stale obstacles decay
  automatically; nothing to clear. See
  [How Viam's world model differs](/motion-planning/obstacles/#how-viams-world-model-differs-from-ros).
- **Plan does not replan during execution.** MoveIt's executors can
  halt and replan on planning-scene updates; Viam's `Move` runs the
  committed path to completion. See
  [Replanning behavior](/motion-planning/replanning-behavior/).
- **One planner, one IK solver.** You do not pick between OMPL planners
  or between KDL/Trac-IK/Pick IK. cBiRRT and NLopt are what you get.
- **No Setup Assistant or SRDF.** Your arm module declares its own
  kinematics and self-collision relationships. You configure
  component frames and geometries through the Viam app.

## What you lose

- **Planner selection and per-planner tuning.** If your application
  relies on PILZ for industrial straight-line moves, RRTconnect for
  speed, or PRMstar for optimization, Viam does not give you that
  choice. Use constraints to express the path behavior you want.
- **Visualization through rviz.** Viam has
  [the 3D scene tab](/motion-planning/3d-scene/) in the web UI, which
  covers frame visualization and obstacle geometry but does not
  mirror rviz's full plugin ecosystem.
- **Task Constructor and MoveIt-native task composition.** Build
  task sequences in application code.
- **Direct access to planning internals** (OMPL state spaces, custom
  samplers, custom validity checkers). These are not exposed.

## What you gain

- **One API across heterogeneous arms.** The same `Move` call drives
  a Universal Robots UR5e, a UFactory xArm 6, a KUKA arm, an eva, and
  others through their respective Viam modules. See
  [Using industrial arms with Viam](/motion-planning/migration/industrial-arms/).
- **Less configuration to author.** No launch files. No SRDF. No
  `move_group.launch`. Arm config is JSON attributes in the Viam app.
- **Built-in cloud connectivity.** The motion service is reachable
  through the Viam app, through any SDK, and through the CLI without
  standing up a ROS network.

## What's next

- [How motion planning works](/motion-planning/how-planning-works/):
  the cBiRRT algorithm and its limits.
- [Allow specific frames to collide](/motion-planning/motion-how-to/allow-frame-collisions/):
  Viam's self-filter / body padding equivalent.
- [Move an arm to a pose](/motion-planning/motion-how-to/move-arm-to-pose/):
  the equivalent of `move_group.move()`.
- [Frame system for TF users](/motion-planning/migration/tf/):
  if you also want to understand Viam's coordinate frames.
- [Using industrial arms with Viam](/motion-planning/migration/industrial-arms/):
  the vendor-abstraction story in more detail.
