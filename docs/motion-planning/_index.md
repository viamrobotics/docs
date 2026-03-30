---
linkTitle: "Motion planning"
title: "Motion Planning"
weight: 160
layout: "docs"
type: "docs"
no_list: true
noedit: true
open_on_desktop: true
overview: true
description: "Plan and execute collision-free movements for robot arms and gantries."
notoc: true
# Aliases stripped — /operate/mobility/ and /operate/mobility/motion-concepts/
# still exist on new-docs-site. Add back when those pages are deleted.
---

Your robot arm needs to move from one position to another without colliding with
the table, the walls, or itself. Motion planning computes collision-free paths
through 3D space, taking into account the arm's kinematic model, the workspace
geometry, and any constraints on how the arm should move.

Viam's motion planning system handles this automatically. You define the spatial
layout of your workspace (the frame system), describe what obstacles exist, and
tell the arm where to go. The motion planner finds a safe path and executes it.

## How It Works

Motion planning in Viam connects several pieces:

1. **Frame system**: a coordinate tree that tracks where every component is in
   space. The frame system lets you specify target positions in any frame and
   translates between them automatically.

2. **Kinematic model**: a description of the arm's joints and links that tells
   the planner what configurations are physically possible.

3. **Obstacles**: geometry (boxes, spheres, capsules) that define regions the
   arm must avoid.

4. **Constraints**: rules about how the arm should move between poses, such as
   keeping the end effector on a straight line or maintaining its orientation.

5. **Motion service**: the service that takes all of the above and computes a
   collision-free path from the current pose to the target pose.

## Get Started

Set up the spatial model for your workspace, then use the how-to guides to move
your hardware.

### Understand your workspace

{{< cards >}}
{{% card link="/motion-planning/frame-system/" noimage="true" %}}
{{% card link="/motion-planning/obstacles/" noimage="true" %}}
{{% card link="/motion-planning/camera-calibration/" noimage="true" %}}
{{< /cards >}}

### Configure your frame system

{{< cards >}}
{{% card link="/motion-planning/frame-system-how-to/arm-gripper-camera/" noimage="true" %}}
{{% card link="/motion-planning/frame-system-how-to/arm-fixed-camera/" noimage="true" %}}
{{% card link="/motion-planning/frame-system-how-to/mobile-base-sensors/" noimage="true" %}}
{{% card link="/motion-planning/frame-system-how-to/mobile-base-arm/" noimage="true" %}}
{{< /cards >}}

### Plan and execute motion

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/move-arm-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/move-arm-with-constraints/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/avoid-obstacles/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/move-gantry/" noimage="true" %}}
{{< /cards >}}

### Manipulation

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/pick-an-object/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/place-an-object/" noimage="true" %}}
{{< /cards >}}

### Understand the internals

{{< cards >}}
{{% card link="/motion-planning/constraints/" noimage="true" %}}
{{% card link="/motion-planning/reference/algorithms/" noimage="true" %}}
{{% card link="/motion-planning/reference/" noimage="true" %}}
{{< /cards >}}
