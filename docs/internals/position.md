---
title: "How Position is Measured in Viam"
linkTitle: "Position"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the position measurements reported by some models of sensor."
---

<!-- A description of how Viam's platform reads and utilizes the position measurements reported by some models of sensor and movement sensor components. -->
<!-- Alternative title ideas: "Position Vectors: Position measurements in Viam" "Position Vectors: How Position is measured in Viam" -->

An `Position` reading specifies the GPS coordinates of an object in 3D space, or, its position in the geographic coordinate system [(GCS)](https://en.wikipedia.org/wiki/Geographic_coordinate_system).

An example of a `Position` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

<!-- TODO: add terminal output or short code snippet -->

Use position readings to specify *absolute* positions of components when using the [Motion Service](../../services/motion/) and [Frame System](../../services/frame-system/), as opposed to orientation vector readings, which you use to specify relative position.

Because these absolute readings don't require spatial relationships to be defined, a *sensor* or *movement sensor* that reads `position` requires less [robot configuration](/manage/configuration/) for you to utilize the [sensor API](/program/apis/#sensor) or [movement sensor API](/program/apis/#movement-sensor) than sensors or movement sensors that read `orientation.`
