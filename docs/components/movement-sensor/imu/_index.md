---
title: "Configure an IMU"
linkTitle: "IMU"
weight: 3
type: "docs"
description: "Supported IMU models."
# SMEs: Rand
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the `AngularVelocity`, `Orientation`, `CompassHeading`, and `LinearAcceleration` methods.
Acceleration and magnetometer data are available by using the [sensor](../../sensor/) `GetReadings` method, which IMUs wrap.
Viam has built-in support for IMUs from two manufacturers:
