---
title: "Move an arm without code"
linkTitle: "Move an arm with no code"
weight: 30
type: "docs"
layout: "docs"
description: "Move an arm without code using the web UI."
date: "2025-05-21"
---

{{<gif webm_src="/how-tos/joint_positions.webm" mp4_src="/how-tos/joint_positions.mp4" alt="The robot arm moving through joint position commands" max-width="150px" class="alignright">}}

You can move an arm without code using the web UI.
This is a good way to quickly test that your arm is working before writing code to move it.

This is also a good way to confirm the directions of the x, y, and z axes of your arm.

## Prerequisites

{{< expand "A running machine connected to Viam." >}}

{{% snippet "setup.md" %}}

{{< /expand >}}

{{< expand "Set up your arm hardware." >}}

1. Mount your arm to a stable structure.

1. Ensure there is enough space for the arm to move without hitting obstacles, people, or pets.

1. Ensure the arm is connected to power, and to the computer running `viam-server`.

{{< /expand >}}

{{< expand "Configure your arm." >}}

See [Configure an arm](/operate/mobility/move-arm/configure-arm/) for instructions.

{{< /expand >}}

## Move the arm

1. In the Viam app, navigate to your machine's page.

1. On your arm component's configuration card, select the **TEST** tab.

   {{% alert title="Caution" color="caution" %}}
   Be careful when moving your robot arm.
   Before moving the arm, ensure it has enough space and that there are no obstacles or people near the arm.

Keep in mind:

- Moving joints near the base of the arm even a few degrees can cause the end of the arm to move a significant distance.
- Moving the arm to a new pose can cause the arm to move in unexpected ways.

{{% /alert %}}

1. Enter joint positions or end effector poses, then click **Execute**.
   Or, use the **Quick move** interface to move each joint in 5 degree increments.

   {{<imgproc src="/components/arm/control.png" resize="x1100" declaredimensions=true alt="Arm control interface." style="max-width:600px" class="shadow imgzoom" >}}

   {{% alert title="Info" color="info" %}}

The Viam app control interface uses the [arm API](/dev/reference/apis/components/arm/) to move the arm.
You can also use the arm API to move the arm in code, though it is not recommended for complex movements because it does not take into account obstacles or allow for complex motion planning.

{{% /alert %}}

1. To refresh the numbers in the **MoveToJointPositions** or **MoveToPosition** tables, click **Current position**.

1. To confirm the directions of the x, y, and z axes of your arm, move the arm in each direction and note which way the arm moves in the real world.
   It can be useful to label the axes on your workspace, for example with tape or markers.
