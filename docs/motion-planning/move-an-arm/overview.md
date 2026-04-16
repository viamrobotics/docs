---
linkTitle: "Overview"
title: "Move an arm"
weight: 1
layout: "docs"
type: "docs"
description: "Command an arm to a target pose, along a constrained path, or directly in joint space. Build pick-and-place flows from those primitives."
aliases:
  - /motion-planning/pick-and-place/
---

Viam exposes three ways to command an arm. Three questions sort them:

1. **What do you know about the destination?** A Cartesian target (a pose
   in space) calls for the motion service. A specific joint configuration
   calls for direct joint commands.
2. **Does the shape of the motion matter, or only the endpoint?** If you
   need a straight line, a fixed orientation, or any other rule about
   the path itself, you need constraints.
3. **Do you want obstacle avoidance and IK picked for you, or fine
   manual control?** The motion service handles both; direct joint
   commands skip both.

| Pattern                                                                          | Input                    | Obstacle avoidance | Path-shape control | When to pick                                                                                                                                     |
| -------------------------------------------------------------------------------- | ------------------------ | ------------------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Move to a pose](/motion-planning/move-an-arm/move-to-pose/)                     | Cartesian target         | Yes                | No                 | You know where the end effector needs to go and want the planner to figure out how.                                                              |
| [Move with constraints](/motion-planning/move-an-arm/move-with-constraints/)     | Cartesian target + rules | Yes                | Yes                | The shape of the motion matters (straight-line tool path, level end effector).                                                                   |
| [Move by joint positions](/motion-planning/move-an-arm/move-by-joint-positions/) | Joint angles             | No                 | Direct             | You know the joint angles, need predictable motion between known configurations, or want to avoid the planner picking an unexpected IK solution. |

For the four constraint types the planner enforces, see
[Configure motion constraints](/motion-planning/move-an-arm/constraints/).

## Pick and place

Pick-and-place is the point where motion planning, vision, and gripper
control meet. Each service works on its own, but the failure modes that
matter most (the gripper closing on air, a depth estimate that crashes
the arm into the table) only appear when all three run together.

The workflow splits into two stages so each can be developed and debugged
independently:

- **Pick** covers detection, approach, and grasp. The arm moves to a
  pre-grasp pose above the object, descends, closes the gripper on the
  object, and lifts.
- **Place** covers transport and release. The arm moves the grasped
  object to a target location, descends, opens the gripper, and retreats.

Both stages reuse the obstacle definitions and geometry-attachment patterns
from [Obstacles](/motion-planning/obstacles/) and the arm-motion patterns
from the table above.

## How-tos

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/move-with-constraints/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/move-by-joint-positions/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/constraints/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/pick-an-object/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/place-an-object/" noimage="true" %}}
{{< /cards >}}
