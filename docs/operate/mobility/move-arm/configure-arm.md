---
title: "Configure an arm"
linkTitle: "Configure an arm"
weight: 10
type: "docs"
layout: "docs"
description: "Configure an arm component to use your robotic arm with Viam."
date: "2025-05-21"
---

Configure an [arm component](/operate/reference/components/arm/) to use your robotic arm with Viam.

## Prerequisites

{{< expand "A running machine connected to Viam." >}}

{{% snippet "setup.md" %}}

{{< /expand >}}

{{< expand "Set up your arm hardware." >}}

1. Mount your arm to a stable structure.

1. Ensure there is enough space for the arm to move without hitting obstacles, people, or pets.

1. Ensure the arm is connected to power, and to the computer running `viam-server`.

{{< /expand >}}

## Configure the arm

1. Navigate to your machine's page.

1. Select the **CONFIGURE** tab.

1. Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.

1. Select the `arm` type, then search for and select the model compatible with your arm hardware.
   For example, if you have a UFactory xArm 6, select the `xArm6` model.

   The following models implement the [arm component API](/dev/reference/apis/components/arm/):

   {{<resources api="rdk:component:arm" type="arm" no-intro="true">}}


1. Enter a name or use the suggested name for your arm and click **Create**.

1. Fill in the arm's configuration fields based on the model-specific documentation that appears in the right side of the configuration card.
   For example, an `xArm6` requires a `host` attribute:

   ```json
   {
     "host": "192.168.1.100"
   }
   ```

1. You will need a reference frame to use your arm with the motion planning service.
   Continue to [Configure your frame system](/operate/mobility/move-arm/frame-how-to/).
