---
title: "Move an arm without code"
linkTitle: "Move an arm with no code"
weight: 20
type: "docs"
layout: "docs"
description: "Move an arm without code from the Viam app interface."
---

You can move an arm without code from the Viam app interface.

## Prerequisites

{{< expand "A running machine connected to the Viam app." >}}

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

1. Enter joint positions or end effector poses, then click **Execute**.
   Or, use the **Quick move** interface to move each joint in 5 degree increments.

{{% alert title="Caution" color="caution" %}}
Be careful when moving your robot arm.
Before moving the arm, ensure it has enough space and that there are no obstacles or people near the arm.

Keep in mind:

- Moving joints near the base of the arm even a few degrees can cause the end of the arm to move a significant distance.
- Moving the arm to a new pose can cause the arm to move in unexpected ways.

{{% /alert %}}
