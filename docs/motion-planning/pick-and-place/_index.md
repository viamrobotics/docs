---
linkTitle: "Pick and place"
title: "Pick and place"
weight: 60
layout: "docs"
type: "docs"
description: "End-to-end manipulation: detect, grasp, move, and release an object."
---

Pick-and-place is the point where motion planning, vision, and gripper
control meet. Each service works on its own, but the failure modes that
matter most (the gripper closing on air, a depth estimate that crashes
the arm into the table) only appear when all three run together.

The workflow splits into two stages so each can be developed and
debugged independently:

- **Pick** covers detection, approach, and grasp. The arm moves to a
  pre-grasp pose above the object, descends, closes the gripper on the
  object, and lifts.
- **Place** covers transport and release. The arm moves the grasped
  object to a target location, descends, opens the gripper, and
  retreats.

Both stages reuse the obstacle definitions and geometry-attachment
patterns from [Define obstacles](/motion-planning/obstacles/) and the
arm-motion patterns from [Move an arm](/motion-planning/move-an-arm/).

## How-tos

{{< cards >}}
{{% card link="/motion-planning/pick-and-place/pick-an-object/" noimage="true" %}}
{{% card link="/motion-planning/pick-and-place/place-an-object/" noimage="true" %}}
{{< /cards >}}
