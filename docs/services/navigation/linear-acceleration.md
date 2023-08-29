---
title: "How Linear Acceleration is Measured in Viam"
linkTitle: "Linear Acceleration"
weight: 10
type: "docs"
description: "How to use the linear acceleration measurements reported by some models of movement sensor."
---

Linear acceleration measurements are read by the following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/):

- [accel-adxl345](/components/movement-sensor/adxl345/)

An example of a `Linear Acceleration` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

## Usage

If you want to read linear acceleration, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
Use linear acceleration readings to determine the rate of change of the [linear velocity](/services/navigation/linear-velocity/) of your robot, or, the speed at which your robot is moving through space.
