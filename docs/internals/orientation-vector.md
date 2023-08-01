---
title: "How Orientation is Measured in Viam"
linkTitle: "Orientation"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the orientation measurements reported by some models of sensor."
aliases:
    - "/appendix/orientation-vector"
    - "/internals/orientation-vector"
---

A description of how Viam's platform reads and utilizes the orientation measurements reported by some models of sensor and movement sensor components.

<!-- TODO: CAN GATHER MODELS HERE -->

An _orientation vector_ specifies the orientation of an object in 3D space.
You use orientation vectors to specify relative orientations of components when using the [motion service](../../services/motion/) and [frame system](../../services/frame-system/).
The first three properties (coordinates) of this vector, `OX`, `OY`, and `OZ`, form an axis pointing in the same direction as the object.
**Theta** specifies the angle of the object's rotation about that axis.

An `Orientation` reading specifies the orientation of an object in 3D space as an "orientation vector", or, its position within the [cartesian coordinate system](https://en.wikipedia.org/wiki/Cartesian_coordinate_system) relative to some specific `origin` point that you, the user, need to choose and configure for your robot.

You compose "orientation vectors" following the same protocol to specify relative orientations of components when using the [Motion Service](../../services/motion/) and [Frame System](../../services/frame-system/).

An example of an `Orientation` reading or, an orientation vector:

``` golang
sensors.Readings{Name: movementsensor.Named("imu"), Readings: map[string]interface{}{"a": 1.2, "b": 2.3, "c": 3.4}}
```

<!-- TODO: add terminal output or short code snippet -->

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
