---
title: "Configure components attached to your arm"
linkTitle: "Configure additional components"
description: "Configure additional components such as grippers, cameras, and other sensors attached to your arm."
weight: 20
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

## Configure a gripper

If you have a gripper, you can configure it to move with the arm.
See [Configure a gripper](/operate/reference/components/gripper/) for instructions on configuring the gripper itself.
Then, configure the gripper's frame to describe its position and orientation relative to the arm:

1. In the **CONFIGURE** tab, find the gripper's configuration card.

1. Click **+ Add Frame**.

1. Select the arm's frame as the parent frame.

1. Enter the gripper origin's position and orientation relative to the center of the end of the arm.
   It is up to you to decide what part of the gripper you want to use as the origin of the frame.
   It is common to use a central point near the base of the gripper jaws as the origin.

   {{<imgproc src="/tutorials/constrain-motion/gripper-diagram.png" resize="x1100" declaredimensions=true alt="A gripper mounted on an arm. The Z axis of the gripper points from the base of the gripper to the end of its jaws. The X axis points up through the gripper. The Y axis points in the direction along which the jaws open and close (following the right-hand rule). The diagram also shows the global coordinate system with Z pointing up, X down the length of the horizontal gripper, and Y pointing horizontally in the opposite direction of the gripper's Y." style="max-width:500px" class="imgzoom" >}}

   For example, the gripper in the image above has a translation of 110 millimeters in the z-direction, and it is oriented along the same z-axis as the end of the arm but is rotated 90 degrees around the z-axis, so its frame configuration is:

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

## Configure a camera

If you have a camera that can see the environment, first configure the camera itself.
For example, you can use an Intel Realsense camera by configuring the `realsense` component according to its [documentation](https://app.viam.com/module/viam/realsense).
Then, configure the camera's frame to describe its position and orientation relative to the arm:

1. In the **CONFIGURE** tab, find the camera's configuration card.

1. Click **+ Add Frame**.

   - If the camera is mounted on the arm:

     1. Select the arm's frame as the parent frame.

     1. Enter the camera lens' position and orientation relative to the center of the end of the arm.

   - If the camera is mounted separately from the arm:

     1. Leave the world frame as the parent frame.

     1. Enter the camera lens' position and orientation relative to the world frame.

## Configure a passive object

If you have a passive object attached to the arm such as a camera mount, you will want the motion service to be aware of it to avoid collisions.

You do not need to configure the object as a component, because you won't be interacting with it through a Viam API.
Instead, you will pass it as a _transform_ object when you call the `Move` motion service API method.
