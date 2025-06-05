---
title: "Configure an arm"
linkTitle: "Configure an arm"
weight: 10
type: "docs"
layout: "docs"
description: "Configure an arm including its reference frame."
date: "2025-05-21"
---

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

   For a project with a single arm, you can define the arm's frame as being the same as the world frame, so leave the default values:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": 0,
         "x": 0,
         "y": 0,
         "z": 1
       }
     },
     "parent": "world",
     "translation": {
       "x": 0,
       "y": 0,
       "z": 0
     }
   }
   ```

1. Save your configuration.

## Configure a different reference frame

For a project with multiple arms, you can define a different [reference frame](/operate/reference/services/frame-system/) for each arm.
To use a reference frame for your arm that is different from the default world frame:

1. Configure the arm as above, adding a frame with the **+ Add Frame** button.

1. Edit your arm's frame according to your needs.
   The frame parameters are:

   - `parent`: The parent frame.
     You can use the `world` frame, or another frame you have defined.

     For example, if you have an arm mounted on a gantry, you can use the gantry's frame as the parent frame of the arm by setting `"parent": "name-of-your-gantry"`.
     This will cause the arm's frame to be updated as the gantry moves.

   - `orientation`: The orientation of the frame relative to the parent frame, represented as a vector.
     If you use the default values, the frame is aligned with the parent frame.
   - `translation`: The distance between the frame and the parent frame in each direction, in millimeters.

1. Confirm the x, y, and z axes of the arm by moving it in each direction using the **TEST** tab.

### Example: Two arms mounted on a table

Imagine you have two arms mounted on a table, some distance apart.

{{<imgproc src="operate/two-arm-setup-3d.svg" resize="x1100" declaredimensions=true alt="Two arms mounted on a table with frames shown, z pointed up for both." style="max-width:600px" class="imgzoom" >}}

1. You define the frame of one arm to be at the same origin as the world frame.
1. You move the arm in each direction using the web UI and see that positive x is to the right, positive y is forward, and positive z is up.
   You label the world frame axes on the table with tape for your reference.
1. You measure the distance between the two arms.
   The second arm is 200mm to the left of the first arm, so `"y": 200`.
1. The second arm is facing towards the first arm.
   By the right-hand rule, this means that the second arm is rotated negative 90 degrees around its z axis: `"th": -90`.
   You edit the second arm's frame to reflect this:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": -90,
         "x": 0,
         "y": 0,
         "z": 1
       }
     },
     "parent": "world",
     "translation": {
       "x": 0,
       "y": 200,
       "z": 0
     }
   }
   ```

   Because you aligned the first arm's origin frame with the world frame, the second arm's parent could be world or the first arm's origin frame (for example, `arm_1_origin`) with no difference in function.

1. You check that the second arm's frame is configured correctly by moving it in each direction using web UI and confirming that it moves as expected.
   When you move it in the positive x direction, it should move towards the first arm.
