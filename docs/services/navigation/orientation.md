---
title: "How Orientation is Measured in Viam"
linkTitle: "Orientation"
weight: 10
type: "docs"
description: "Use the orientation measurements reported by some models of movement sensor."
aliases:
    - "/appendix/orientation-vector"
    - "/internals/orientation-vector"
---

Orientation measurements are read by the following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/):

- [imu-wit](/components/movement-sensor/imu/imu-wit/)
- [imu-vectornav](/components/movement-sensor/imu/imu-vectornav/)

An `Orientation` reading specifies the orientation of an object in 3D space as an "orientation vector", or, its position within the [cartesian coordinate system](https://en.wikipedia.org/wiki/Cartesian_coordinate_system) relative to some specific `origin` point that you, the user, need to choose and configure for your robot.

## Client side

You compose "orientation vectors" following the same protocol to specify relative orientations of components when using the [motion service](/services/motion/) and [frame system](/services/frame-system/).

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

## Server side

When you input an orientation vector, Viam normalizes it to the unit sphere.
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
```

If you want to read orientation, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
Additionally, follow [these instructions](/services/frame-system/#configuration) to configure the geometries of each component of your robot within the [frame system](/services/frame-system/).
