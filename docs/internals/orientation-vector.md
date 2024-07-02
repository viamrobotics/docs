---
title: "Orientation Vector"
linkTitle: "Orientation Vector"
weight: 15
type: "docs"
description: "A description of Viam's orientation vector object."
aliases:
  - "/appendix/orientation-vector"
---

An _orientation vector_ specifies the orientation of an object in 3D space.
You use orientation vectors to specify relative orientations of components when using the [motion service](/services/motion/) and [frame system](/services/frame-system/).
The first three components of this vector form an axis pointing in the same direction as the object.
**Theta** specifies the angle of the object's rotation about that axis.

## Example: A camera in a room

Imagine you have a room with a camera.
The corner of the room is (0, 0, 0).

To configure the camera into the frame system, you need to know where in the room the camera is, and where it's pointing.

![A camera in a 3D space](/internals/vector/orientation-vector-camera.png)

**(OX, OY, OZ)** are defined by measurements starting from the corner of the room to the camera:

1. Determine the position of the camera (3,5,2)
2. Determine the position of a point that the camera can see, for example (3,1,1)
3. Subtract the camera point from the observed point to get the OV of the camera: (3,1,1) - (3,5,2) = (0,-4,-1)

{{< alert title="Info" color="info" >}}
When you provide an orientation vector to Viam, Viam normalizes it to the unit sphere.
Therefore if you enter (0, -4, -1), Viam stores it internally and displays it to you as (0,-0.97, -0.24).
{{< /alert >}}

**Theta** describes the angle of rotation of the camera around the calculated vector.
If you are familiar with the pitch-roll-yaw system, you can think of theta as _roll_.
If your camera is perpendicular to one of the axes of your Frame system,
you can determine Theta by looking at the picture and changing the value to 0, 90, 180, or 270 until the orientation of the picture is correct.

OX, OY, OZ, and Theta together form the orientation vector which defines which direction the camera is pointing with respect to the corner of the room, as well as to what degree the camera is rotated about an axis through the center of its lens.

## Why Viam uses orientation vectors

- Easy to measure in the real world
- No protractor needed
- Rotation is pulled out as Theta which is often used independently and measured independently
