---
linkTitle: "Migration"
title: "Migration from ROS and vendor SDKs"
weight: 180
layout: "docs"
type: "docs"
description: "Concept-by-concept mappings for readers coming from MoveIt, Nav2, ROS TF, or vendor-specific industrial arm SDKs."
---

Most roboticists evaluating Viam arrive with a working mental model
from somewhere else: MoveIt for arm planning, Nav2 for mobile
navigation, ROS TF for coordinate frames, or a vendor-specific SDK
like UR's URScript or KUKA's KRL. These pages translate those models
into Viam's motion service, navigation service, and frame system.

The pages are honest about both sides:

- **What transfers**: concepts that map directly (most of them).
- **What is different**: places where Viam's abstraction chose a
  different set of tradeoffs.
- **What you lose**: features and flexibility you had elsewhere that
  Viam does not expose.
- **What you gain**: what Viam does that the other option does not.

## Pick your starting point

{{< cards >}}
{{% card link="/motion-planning/migration/moveit/" noimage="true" %}}
{{% card link="/motion-planning/migration/nav2/" noimage="true" %}}
{{% card link="/motion-planning/migration/tf/" noimage="true" %}}
{{% card link="/motion-planning/migration/industrial-arms/" noimage="true" %}}
{{< /cards >}}

For the ROS vocabulary terms these pages use, see
[vocabulary.md](https://github.com/viamrobotics/docs-dev/blob/main/code-map/vocabulary.md)
in the docs-dev repository.
