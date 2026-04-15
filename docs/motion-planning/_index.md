---
linkTitle: "Motion planning"
title: "Motion planning"
weight: 160
layout: "docs"
type: "docs"
no_list: true
noedit: true
open_on_desktop: true
overview: true
description: "Plan and execute collision-free movements for robot arms and gantries."
notoc: true
aliases:
  - /operate/mobility/
  - /operate/mobility/motion-concepts/
---

Your robot arm needs to move from one position to another without colliding with
the table, the walls, or itself. Motion planning computes collision-free paths
through 3D space, taking into account the arm's kinematic model, the workspace
geometry, and any constraints on how the arm should move.

Viam's motion planning system handles this automatically. You define the spatial
layout of your workspace (the frame system), describe what obstacles exist, and
tell the arm where to go. The motion planner finds a safe path and executes it.

This section covers motion planning for arms, gantries, and other kinematic
chains. For GPS-based autonomous navigation with mobile bases, see
[Navigation](/navigation/).

## Start here

New to Viam's motion service? Work through a short quickstart that uses
fake components so you can run it on any machine:

{{< cards >}}
{{% card link="/motion-planning/quickstarts/first-arm/" noimage="true" %}}
{{% card link="/motion-planning/quickstarts/frame-system/" noimage="true" %}}
{{< /cards >}}

## How it works

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

## Get started

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

### Visualize and debug your workspace

{{< cards >}}
{{% card link="/motion-planning/3d-scene/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/debug-motion-plan/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/calibrate-frame-offsets/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/verify-point-cloud-alignment/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/set-up-obstacle-avoidance/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/edit-frames/" noimage="true" %}}
{{< /cards >}}

### Plan and execute motion

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/move-arm-to-pose/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/move-arm-with-constraints/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/avoid-obstacles/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/drive-a-base/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/move-gantry/" noimage="true" %}}
{{< /cards >}}

### Manipulation

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/pick-an-object/" noimage="true" %}}
{{% card link="/motion-planning/motion-how-to/place-an-object/" noimage="true" %}}
{{< /cards >}}

### Understand the internals

{{< cards >}}
{{% card link="/motion-planning/how-planning-works/" noimage="true" %}}
{{% card link="/motion-planning/replanning-behavior/" noimage="true" %}}
{{% card link="/motion-planning/constraints/" noimage="true" %}}
{{% card link="/motion-planning/reference/" noimage="true" %}}
{{< /cards >}}

### Migrating from ROS or a vendor SDK

{{< cards >}}
{{% card link="/motion-planning/migration/moveit/" noimage="true" %}}
{{% card link="/motion-planning/migration/nav2/" noimage="true" %}}
{{% card link="/motion-planning/migration/tf/" noimage="true" %}}
{{% card link="/motion-planning/migration/industrial-arms/" noimage="true" %}}
{{< /cards >}}
