---
title: "Orientation vector"
linkTitle: "Orientation vector"
weight: 190
type: "docs"
description: "A description of Viam's orientation vector object."
date: "2022-01-01"
no_list: true
aliases:
  - /internals/orientation-vector/
  - /appendix/orientation-vector
  - /operate/reference/orientation-vector/
# updated: ""  # When the content was last entirely checked
---

An _orientation vector_ specifies the orientation of an object in 3D space.
You use orientation vectors to specify relative orientations of components when using the [motion service](/operate/reference/services/motion/) and [frame system](/operate/reference/services/frame-system/).
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

## Gimbal lock at poles

{{< alert title=\"Caution\" color=\"caution\" >}}
When the OZ component of an orientation vector is very close to +1 or -1 (specifically, when `abs(OZ) >= 0.9999`), the orientation vector represents a gimbal-locked state, similar to pointing straight up or straight down.
In this condition, Theta values are computed using different mathematical methods than in the normal case, which can result in discontinuous behavior.
{{< /alert >}}

This edge case occurs because when an object is oriented nearly parallel to the Z-axis (pointing straight up or down), the axis of rotation (OX, OY, OZ) becomes aligned with the Z-axis.
In this configuration, there are infinite valid combinations of the orientation axis and Theta that represent the same physical orientation, similar to the gimbal lock problem in Euler angles.

To handle this mathematically:

- **Normal case** (`abs(OZ) < 0.9999`): Theta is calculated using the standard method based on plane normals
- **Pole case** (`abs(OZ) >= 0.9999`): Theta is calculated using a simplified trigonometric formula to avoid mathematical singularities:
  - For the north pole (OZ approaching +1): `Theta = -atan2(Y', -X')`
  - For the south pole (OZ approaching -1): `Theta = -atan2(Y', X')`

Where X' and Y' are components of the transformed X-axis basis vector.

See an example of how this is handled in Viam's spatial math library [here](https://github.com/viamrobotics/rdk/blob/142f052cb8e2c13d9cf9530dc6d71c7f812b92a8/spatialmath/quaternion.go#L143-L149).

If your application requires orientations near these poles, be aware that:

- Small changes in OZ near the threshold may cause discontinuous changes in how the orientation is represented
- The computed Theta value may change significantly when crossing the pole threshold
- The internal representation switches between two different calculation methods at this boundary

## Why Viam uses orientation vectors

- Easy to measure in the real world
- No protractor needed
- Rotation is pulled out as Theta which is often used independently and measured independently
