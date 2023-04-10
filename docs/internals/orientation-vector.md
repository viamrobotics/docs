---
title: "Poses and Orientation Vectors"
linkTitle: "Pose"
weight: 10
type: "docs"
description: "A description of Viam's orientation vector method."
---

A _Pose_ specifies where an object is with respect to another reference point and where it is pointing.
To specify where an object is you use an orientation vector (**RX, RY, RZ**) that describes the difference between the center of the object and another reference frame.
To specify where an object is pointing, you use **theta** which describes the angular position of the object around that vector.

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
3. Subtract the starting point from the position of the camera: (5,4,2) - (0, 0, 0) = (5, 4, 2).

**Theta** describes the angle of the camera.
If your camera is perpendicular to one of the axes of your Frame system, you can test the correct value by using 0, 90, 180, or 270 for Theta and checking if the orientation of the picture is correct.

 RX, RY, RZ, and Theta together form the _Pose_ which defines the camera's position and where it is pointing.
