---
linkTitle: "Pick and place"
title: "Pick and place"
weight: 40
layout: "docs"
type: "docs"
description: "End-to-end manipulation: detect, grasp, move, and release an object."
---

Manipulation combines motion planning, vision, and gripper control.
Pick and place break the workflow into two stages so each stage can be
developed and debugged independently.

- **Pick** covers detection, approach, and grasp. The arm moves to a
  pre-grasp pose above the object, descends, closes the gripper on the
  object, and lifts.
- **Place** covers transport and release. The arm moves the grasped
  object to a target location, descends, opens the gripper, and
  retreats.

Both stages depend on the obstacle and geometry-attachment patterns
covered under [Obstacles](/motion-planning/obstacles/), plus the
typical arm-motion and gripper-contact constraints under
[Move an arm](/motion-planning/move-an-arm/).

## How-tos

{{< cards >}}
{{% card link="/motion-planning/pick-and-place/pick-an-object/" noimage="true" %}}
{{% card link="/motion-planning/pick-and-place/place-an-object/" noimage="true" %}}
{{< /cards >}}
