---
title: "Configure components attached to your arm"
linkTitle: "Configure additional components"
description: "Configure additional components such as grippers, cameras, and other sensors attached to your arm."
weight: 30
type: "docs"
layout: "docs"
aliases:
  - /operate/mobility/define-geometry/
  - /operate/mobility/define-obstacles/
  - /services/frame-system/nested-frame-config/
  - /mobility/frame-system/nested-frame-config/
  - /operate/reference/services/frame-system/nested-frame-config/
date: "2025-05-21"
---

If you have a gripper, camera, or other components attached to your arm, you can configure them to move with the arm.

You can also take into account passive objects attached to the arm such as a camera mount to avoid collisions.

## Configure a gripper's frame

If you have a gripper, you can configure it to move with the arm.
If you haven't already configured your gripper, see [Configure a gripper].

Configure the gripper's frame to describe its position and orientation relative to the arm:

1. In the **CONFIGURE** tab, find the gripper's configuration card.

1. Click **+ Add frame**.

1. Select the arm's frame as the parent frame.

1. Enter the gripper frame's position and orientation relative to the center of the end of the arm.
   It is up to you to decide what part of the gripper you want to use as the gripper frame.
   It is generally convenient to use a point near the center of the gripper jaws as the gripper frame.

   When you make a call to the motion service to move the gripper to a location, the point you specify in this step is the part of the gripper that will move to that location.

   {{<imgproc src="/operate/mobility/gripper-frame.png" resize="x1100" declaredimensions=true alt="A gripper mounted on an arm. The Z axis of the gripper points from the base of the gripper to the end of its jaws. The X axis points up through the gripper. The Y axis points in the direction along which the jaws open and close (following the right-hand rule). The diagram also shows the global coordinate system with Z pointing up, X down the length of the horizontal gripper, and Y pointing horizontally in the opposite direction of the gripper's Y." style="width:600px" class="imgzoom" >}}

   The gripper in the image above has a translation of 110 millimeters in the z-direction, and it is oriented along the same z-axis as the end of the arm but is rotated 90 degrees around the z-axis, so its frame configuration is:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": 90,
         "x": 0,
         "y": 0,
         "z": 1
       }
     },
     "parent": "my-arm",
     "translation": {
       "x": 0,
       "y": 0,
       "z": 110
     }
   }
   ```

1. Check whether your gripper has a kinematics file.

   Some grippers have [kinematics files](/operate/reference/kinematic-chain-config/) that describe the position and orientation of the jaws of the gripper as they move, relative to the gripper's base.
   This file typically also contains geometries that represent the gripper's volume to avoid collisions between the gripper and its environment.
   You can check whether your gripper has a kinematics file by looking in its module source code, or by using the [`GetKinematics` method](/dev/reference/apis/components/gripper/).

   If you have a kinematics file, you do not need to add any geometries to the gripper's frame, assuming the gripper appears as expected in the **VISUALIZE** tab.

   _If you do not have a kinematics file, see [Configure the geometry of the object](#configure-the-geometry-of-the-object) to configure a geometry for the gripper to avoid collisions between the gripper and its environment._

## Configure a camera

If you have a camera that can see the environment, configure the camera's frame to describe its position and orientation relative to the arm so that what the camera sees can be used to plan the arm's motion:

1. Configure the camera itself.
   For example, you can use an Intel Realsense camera by configuring the `realsense` model of the camera component according to its [documentation](https://app.viam.com/module/viam/realsense).

1. In the **CONFIGURE** tab, find the camera's configuration card.

1. Click **+ Add frame**.

1. Edit the frame depending on where the camera is mounted:

   {{< tabs >}}
   {{% tab name="Camera mounted on arm" %}}
   Set the arm's frame as the parent frame.

   Enter the camera lens' position and orientation relative to the center of the end of the arm.
   {{% /tab %}}

   {{% tab name="Camera mounted on a static object or wall" %}}
   Leave the world frame as the parent frame.

   Enter the camera lens' position and orientation relative to the world frame.
   {{% /tab %}}
   {{< /tabs >}}

## Configure a passive object

If you have a passive object attached to the arm such as a camera mount, you will want the motion service to be aware of it to avoid collisions.

- If you have an object that is sometimes attached to the arm and sometimes not, for example an object that your gripper picks up, you can pass it as a _transform_ object when you call the `Move` motion service API method.
  This is covered in the [move an arm guide](/operate/mobility/move-arm/arm-motion/#define-the-geometry-of-the-environment).
- If your object is always attached to the arm, you can configure it as a fake, generic component with a geometry by following the instructions in this section:

### Add the component and frame

1. In the **CONFIGURE** tab, click the **+** button > **Component or service** > **generic**.

1. Select **fake** component (do not select service; services do not have geometries).

1. Enter a name and click **Create**.

1. Click **+ Add frame**.

1. Set the parent frame to the name of the arm or gripper, depending on where the object is attached.

### Configure the geometry of the object

1. Copy the following geometry template into the frame configuration, depending on your object's shape:

   {{< tabs >}}
   {{% tab name="Box" %}}

   A rectangular prism with dimensions `x`, `y`, and `z` in millimeters.

   ```json {class="line-numbers linkable-line-numbers"}
     "geometry": {
       "type": "box",
       "x": 80,
       "y": 250,
       "z": 200
     }
   ```

   {{% /tab %}}
   {{% tab name="Capsule" %}}

   A cylinder with hemispherical end caps.
   `r` is the radius of the cylinder, and `l` is the overall length of the cylinder in millimeters.

   ```json {class="line-numbers linkable-line-numbers"}
     "geometry": {
       "type": "capsule",
       "r": 20,
       "l": 160
     }
   ```

   {{<imgproc src="/operate/mobility/capsule.png" resize="x1100" declaredimensions=true alt="A capsule with its length and radius labeled." style="max-width:250px" class="shadow imgzoom aligncenter" >}}

   {{% /tab %}}
   {{% tab name="Sphere" %}}

   A sphere with radius `r` in millimeters.

   ```json {class="line-numbers linkable-line-numbers"}
     "geometry": {
       "type": "sphere",
       "r": 90
     }
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Edit the dimensions to match your object's dimensions.

1. The origin of the geometry is at its center.

   Set the translation of the object's origin relative to its parent frame.
   For example, if you have a capsule of length `160` and you want it to begin at the origin of the parent frame, set the translation to `"z"=80`.

1. Click **Save**.

1. Check that the object appears as expected in the **VISUALIZE** tab.

1. If you need to change the object's orientation, you can make changes to the orientation, save the config, and return to the **VISUALIZE** tab to see the changes.
   It can be helpful to understand the following:

   {{< tabs >}}
   {{% tab name="Box" %}}

   The z-axis of a box is along its z-dimension and so forth with the x and y axes.
   If your box is at a right angle to how you want it to be oriented, try changing the dimensions to match the correct directions.

   If you need to rotate the box about its z-axis, edit theta (`th`) to the desired angle and check the **VISUALIZE** tab to see the changes.

   To point the box's z-axis in a different direction, for example at a 30 degree angle from the parent frame's x-axis in the x-y plane, you can change its orientation to:

   ```json {class="line-numbers linkable-line-numbers"}
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": 0,
         "x": 0.866,
         "y": 0.5,
         "z": 0
       }
     }
   ```

   Go to the **VISUALIZE** tab to see the changes.

   {{% /tab %}}
   {{% tab name="Capsule" %}}

   The z-axis of a capsule is along its length.

   If, for example, you need the length of the capsule to be along the x-axis, you can change its orientation to:

   ```json {class="line-numbers linkable-line-numbers"}
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": 0,
         "x": 1,
         "y": 0,
         "z": 0
       }
     }
   ```

   Go to the **VISUALIZE** tab to see that the z-axis of the capsule is now aligned with the parent frame's x-axis, 90 degrees from its original orientation.

   If you need the capsule to be aligned at a 45 degree angle between y and z, you can change its orientation to:

   ```json {class="line-numbers linkable-line-numbers"}
     "orientation": {
       "type": "ov_degrees",
       "value": {
         "th": 0,
         "x": 0,
         "y": 1,
         "z": 1
       }
     }
   ```

   You should not need to modify theta (`th`) for capsules since that would spin the round capsule around its axis, causing no meaningful change.

   {{% /tab %}}
   {{% tab name="Sphere" %}}

   A sphere's orientation generally does not need to be changed.

   {{% /tab %}}
   {{< /tabs >}}
