---
title: "How Linear Acceleration is Measured in Viam"
linkTitle: "Linear Acceleration"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the linear accelaration measurements reported by some models of movement sensor."
---

How Viam's platform reads and utilizes the orientation measurements reported as `Readings` by the following {{< glossary_tooltip term_id="models" text="models" >}} of movement sensor components:

- [accel-adxl345](/components/movement-sensor/accel-adxl345/)


An `Linear Acceleration` reading specifies the...

An example of a `Linear Acceleration` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

<!-- TODO: add terminal output or short code snippet -->

<!-- Use linear accelaration readings to specify *absolute* linear accelarations of components when using the [Motion Service](../../services/motion/) and [Frame System](../../services/frame-system/), as opposed to orientation vector readings, which you use to specify relative linear accelaration.

Because these absolute readings don't require spatial relationships to be defined, a *sensor* or *movement sensor* that reads `linear accelaration` requires less [robot configuration](/manage/configuration/) for you to utilize the [sensor API](/program/apis/#sensor) or [movement sensor API](/program/apis/#movement-sensor) than sensors or movement sensors that read `orientation.` -->
