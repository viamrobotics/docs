---
title: "Motion planning basics"
linkTitle: "Motion basics"
weight: 8
type: "docs"
layout: "docs"
description: "Learn what you can do with Viam's motion planning tools."
date: "2025-05-21"
# updated: ""
---

Viam's motion planning tools allow you to automate the intelligent movement of your machines.
You can:

- Plan coordinated motion of multiple components
- Avoid obstacles
- Constrain the orientation of an arm's end effector
- Give GPS waypoints to a mobile robot

For example, instead of sending individual commands to each motor of a robotic arm, you can use one motion planning command to move the arm smoothly to a specific position while avoiding obstacles and keeping a gripper upright.

## Supported components

You can move the following components with the [motion service](/operate/reference/services/motion/):

{{< cards >}}
{{% relatedcard link="/operate/reference/components/arm/" %}}
{{% relatedcard link="/operate/reference/components/base/" %}}
{{% relatedcard link="/operate/reference/components/gantry/" %}}
{{% relatedcard link="/operate/reference/components/gripper/" %}}
{{< /cards >}}

You can use the following components to augment motion planning and navigation:

- [Camera](/operate/reference/components/camera/)
  - For example, you could use a [RealSense depth camera](https://app.viam.com/module/viam/realsense) to identify and avoid obstacles.
- [Movement sensor](/operate/reference/components/movement-sensor/)
  - For example, use a [GPS](https://app.viam.com/module/viam/gps) to locate a mobile robot.

## The frame system

Viam's [frame system](/operate/reference/services/frame-system/) is a way to describe the spatial relationship between the components in your robot.
The motion service uses the frame system to plan the motion of components.

For example, if you want to command an arm to move to coordinates of `(300, 0, 0)` millimeters, you first need to define the origin `(0, 0, 0)` of the coordinate system and the directions of the x, y, and z axes to give those coordinates meaning.

To give the necessary context, you define the arm's `frame` to describe its position and orientation relative to the world.
If you also have a gripper component, you define the gripper's `frame` to describe its position and orientation relative to the arm, so that when the arm moves, the motion service knows where the gripper is as well.

<!-- Not live yet
## Visualize components and frames

You can visualize your machine's components and frames in the Viam app.

1. In the Viam app, navigate to your machine's page.
1. Select the **VISUALIZE** tab.

   {{<imgproc src="/services/frame-system/viz-tab.png" resize="x1100" declaredimensions=true alt="Visualization of a number of objects seemingly floating in space above a grid." style="max-width:600px" class="shadow" >}}
-->
