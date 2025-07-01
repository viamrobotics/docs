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

Viam's [frame system](/operate/reference/services/frame-system/) allows you to describe the spatial relationship between the components in your robot.
You configure your machine's frames once, and Viam keeps track of the frames as they move.
This means you can send motion service commands using a consistent coordinate system, regardless of where the components are at a given time.

You must configure frames before you can use the motion service.
For example, if you want to command an arm to move to coordinates of `(300, 0, 0)` millimeters, you first need to decide on the origin `(0, 0, 0)` and the directions of the x, y, and z axes of the {{< glossary_tooltip term_id="world-frame" text="world" >}} coordinate system to give your coordinates meaning.

You then define the arm's `frame` to describe its position and orientation relative to the world frame.
If you also have a gripper component, you define the gripper's `frame` to describe its position and orientation relative to the arm, so that when the arm moves, the motion service knows where the gripper is as well.

### Visualize components and frames

{{< readfile "/static/include/snippet/visualize.md" >}}
