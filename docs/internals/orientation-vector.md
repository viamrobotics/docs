---
title: "Orientation Vector"
linkTitle: "Orientation Vector"
weight: 10
type: "docs"
description: "A description of Viam's orientation vector method."
---

A _pose_ specifies where an object is with respect to another reference point and which direction it is pointing.
Pose includes a 3D vector specifying the position of the center of the object, as well as an *orientation vector* specifying the angle of the object in 3D space.
To specify which direction an object is pointing, you use an orientation vector (**OX, OY, OZ, theta**).
The first three components of this vector form an axis pointing in the same direction as the object.
**Theta** specifies the angle of the object's rotation about that axis.

## Example: A camera in a room

Imagine you have a room with a camera.
The corner of the room is (0, 0, 0).

To configure the camera into the frame system, you need to know where in the room the camera is, and where it's pointing.

![A camera in a 3D space](../img/vector/orientation-vector-camera.png)

**(RX, RY, RZ)** are defined by measurements starting from the corner of the room to the camera:

1. Determine the starting point.
   In this case it is (0, 0, 0).
2. Determine the position of the camera.
   In this case it is (5, 4, 2).
3. Subtract the starting point from the position of the camera: (5, 4, 2) - (0, 0, 0) = (5, 4, 2).

**Theta** describes the angle of the camera.
If your camera is perpendicular to one of the axes of your Frame system, you can test the correct value by using 0, 90, 180, or 270 for Theta and checking if the orientation of the picture is correct.

 RX, RY, RZ, and Theta together form the _Pose_ which defines the camera's position and where it is pointing.
