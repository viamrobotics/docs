---
title: "How Orientation is Measured in Viam"
linkTitle: "Orientation"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the orientation measurements reported by some models of movement sensor."
aliases:
    - "/appendix/orientation-vector"
    - "/internals/orientation-vector"
---

How Viam's platform reads and utilizes the orientation measurements reported as `Readings` by the following {{< glossary_tooltip term_id="models" text="models" >}} of movement sensor components:

- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [imu-vectornav](/components/movement-sensor/imu/imu-vectornav/)

An _orientation vector_ specifies the orientation of an object in 3D space.
You use orientation vectors to specify relative orientations of components when using the [motion service](../../services/motion/) and [frame system](../../services/frame-system/).
The first three properties (coordinates) of this vector, `OX`, `OY`, and `OZ`, form an axis pointing in the same direction as the object.
**Theta** specifies the angle of the object's rotation about that axis.

An `Orientation` reading specifies the orientation of an object in 3D space as an "orientation vector", or, its position within the [cartesian coordinate system](https://en.wikipedia.org/wiki/Cartesian_coordinate_system) relative to some specific `origin` point that you, the user, need to choose and configure for your robot.

You compose "orientation vectors" following the same protocol to specify relative orientations of components when using the [Motion Service](../../services/motion/) and [Frame System](../../services/frame-system/).

An example of an `Orientation` reading or, an orientation vector:

``` shell
imu get_readings return value: {'angular_velocity': x: -47.9736328125
y: 142.63916015625
z: -90.14892578125
, 'linear_acceleration': x: -6.3973068359375
y: 1.3455413330078123
z: 12.320561743164061
, 'orientation': o_x: -0.5830770214771182
o_y: -0.3688865202247088
o_z: 0.7238397075471042
theta: 60.92769307372125
}
```

When you provide an orientation vector to Viam, Viam **normalizes** `(0X, OY, OZ))` to the unit sphere.
Therefore, if you ran the following line of code simulating an orientation `Reading` from a sensor of `(0, -4, -1)`, it will be normalized to `(0, -0.97, -0.24)` as interpreted by `viam-server`:

``` golang
sensors.Readings{Name: movementsensor.Named("imu"), Readings: map[string]interface{}{"b": 0, "b": -4, "c": -1}}
```

``` sh
imu get_readings return value: {'angular_velocity': x: -47.9736328125
y: 142.63916015625
z: -90.14892578125
, 'linear_acceleration': x: -6.3973068359375
y: 1.3455413330078123
z: 12.320561743164061
, 'orientation': o_x: 0.0
o_y: -4.0
o_z: -1.0
theta: 60.92769307372125
}
```

<!-- TODO: uhh the sample just doesn't include theta right? should I add it to the sample code? -->

## Configuration

### Example: A camera in a room

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

- **Theta**: describes the angle of **rotation** of the component (camera in example) around the calculated vector.
If you are familiar with the pitch-roll-yaw system, you can think of theta as _roll_.
If your camera is perpendicular to one of the axes of your Frame system,
you can determine Theta by looking at the picture and changing the value to 0, 90, 180, or 270 until the orientation of the picture is correct.

OX, OY, OZ, and Theta together form the orientation vector which defines which direction the camera is pointing with respect to the corner of the room, as well as to what degree the camera is rotated about an axis through the center of its lens.

<!-- ## Why Viam uses orientation vectors

- Easy to measure in the real world
- No protractor needed
- Rotation is pulled out as Theta which is often used independently and measured independently -->
