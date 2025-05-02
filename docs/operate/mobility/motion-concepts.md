---
title: "Motion planning concepts"
linkTitle: "Motion concepts"
weight: 8
type: "docs"
layout: "docs"
description: "Learn what you can do with Viam's motion planning tools."
---

Viam's motion planning tools allow you to automate the intelligent movement of your machines.
You can:

- Move individual components
- Move multiple components in a coordinated way
- Avoid configured static obstacles
- Avoid dynamic obstacles using a depth camera
- Constrain the orientation of a component
- Navigate a mobile robot with GPS

For example, instead of sending individual commands to each motor of a robotic arm, you can use motion planning to move the arm smoothly to a specific position while avoiding obstacles and keeping a gripper upright.

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
  - For example, a [RealSense depth camera](https://app.viam.com/module/viam/realsense)
- [Movement sensor](/operate/reference/components/movementsensor/)
  - For example, a [GPS](https://app.viam.com/module/viam/gps)

## The frame system

Viam's [frame system](/operate/reference/services/frame-system/) is a way to describe the spatial relationship between the components in your robot.
The motion service uses the frame system to plan the motion of components.

For example, if you command an arm to move to coordinates of `(300, 0, 0)` millimeters, this has no meaning unless you have defined where the origin `(0, 0, 0)` of the coordinate system is, as well as which directions correspond to the x, y, and z axes.

To give the necessary context, you define the arm's `frame` to describe its position and orientation relative to the world.
If you also have a gripper component, you define the gripper's `frame` to describe its position and orientation relative to the arm, so that when the arm moves, the motion service knows where the gripper is as well.

## Visualizing components and frames

You can visualize your machine's components and frames in the Viam app.

1. In the Viam app, navigate to your machine's page.
1. Select the **VISUALIZE** tab.

   {{<imgproc src="/services/frame-system/viz-tab.png" resize="x1100" declaredimensions=true alt="Visualization of a number of objects seemingly floating in space above a grid." style="max-width:600px" class="shadow" >}}
