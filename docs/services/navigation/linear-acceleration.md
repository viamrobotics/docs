---
title: "How Linear Acceleration is Measured in Viam"
linkTitle: "Linear Acceleration"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the linear acceleration measurements reported by some models of movement sensor."
---

How Viam's platform reads and utilizes the linear acceleration measurements reported as `Readings` by the following {{< glossary_tooltip term_id="model" text="models" >}} of movement sensor components:

- [accel-adxl345](/components/movement-sensor/adxl345/)

An example of a `Linear Acceleration` reading:

## Client side

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

## Server side

<!-- TODO: add terminal output or short code snippet -->

## Usage

Use linear velocity readings to determine the rate of change of the [linear velocity](/services/navigation/linear-velocity/) of your robot, or, the speed at which your robot is moving through space.
