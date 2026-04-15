---
linkTitle: "Move an arm"
title: "Move an arm"
weight: 20
layout: "docs"
type: "docs"
description: "Command an arm to a target pose, along a constrained path, or directly in joint space."
---

Viam exposes three ways to command an arm, each suited to a different
situation:

- **[Move to a Cartesian pose](/motion-planning/move-an-arm/move-to-pose/)**
  uses the motion service. The planner finds a collision-free path from
  the arm's current pose to the target. This is the right default when
  you know where the end effector needs to go and you want the planner
  to figure out how to get there.

- **[Move with constraints](/motion-planning/move-an-arm/move-with-constraints/)**
  is the same Cartesian-target path plus rules about how the arm moves
  (stay on a straight line, keep the end effector level). Use this
  when the shape of the motion matters, not just the destination.

- **[Move by setting joint positions](/motion-planning/move-an-arm/move-by-joint-positions/)**
  bypasses the planner and drives each joint directly to a commanded
  angle. Use this when you know the joint angles you want, you need
  predictable motion between two known configurations, or you want to
  avoid the planner picking an unexpected IK solution.

See [Constraints](/motion-planning/move-an-arm/constraints/) for the
full reference on the four constraint types.

## How-tos

{{< cards >}}
{{% card link="/motion-planning/move-an-arm/move-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/move-with-constraints/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/move-by-joint-positions/" noimage="true" %}}
{{% card link="/motion-planning/move-an-arm/constraints/" noimage="true" %}}
{{< /cards >}}
