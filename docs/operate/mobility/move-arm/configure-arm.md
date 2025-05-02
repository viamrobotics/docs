---
title: "Configure an arm"
linkTitle: "Configure an arm"
weight: 10
type: "docs"
layout: "docs"
description: "Configure an arm including its reference frame."
---

## Prerequisites

{{< expand "A running machine connected to the Viam app." >}}

{{% snippet "setup.md" %}}

{{< /expand >}}

{{< expand "Set up your arm hardware." >}}

1. Mount your arm to a stable structure.

1. Ensure there is enough space for the arm to move without hitting obstacles, people, or pets.

1. Ensure the arm is connected to power, and to the computer running `viam-server`.

{{< /expand >}}

## Configure the arm

1. In the [Viam app](https://app.viam.com), navigate to your machine's page.

1. Select the **CONFIGURE** tab.

1. Click the **+** icon next to your machine part in the left-hand menu and select **Component**.

1. Select the `arm` type, then search for and select the model compatible with your arm hardware.
   For example, if you have a UFactory xArm 6, select the `xArm6` model.

1. Enter a name or use the suggested name for your arm and click **Create**.

1. Fill in the arm's configuration fields based on the model-specific documentation that appears in the right side of the configuration card.
   For example, an `xArm6` requires a `host` attribute:

   ```json
   {
     "host": "192.168.1.100"
   }
   ```

1. You will need a reference frame to use your arm with the motion planning service.
   Click **+ Add Frame**.

   For a project with a single arm, you can define the arm's frame as being the same as the world frame, so leave the default values.

1. Save your configuration.
