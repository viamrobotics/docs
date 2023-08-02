---
title: "How Position is Measured in Viam"
linkTitle: "Position"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the position measurements reported by some models of movement sensor."
---

How Viam's platform reads and utilizes the position measurements reported as `Readings` by the following {{< glossary_tooltip term_id="models" text="models" >}} of movement sensor components:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-rtk](/components/movement-sensor/gps/gps-rtk/)

An `Position` reading specifies the GPS coordinates of an object in 3D space, or, its position in the geographic coordinate system [(GCS)](https://en.wikipedia.org/wiki/Geographic_coordinate_system).

An example of a `Position` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

<!-- TODO: add terminal output or short code snippet -->

Use position readings to specify the *absolute* position of components when using the [Motion Service](../../services/motion/) and [Frame System](../../services/frame-system/), as opposed to orientation vector readings, which you use to specify relative position.

Because these absolute readings don't require spatial relationships to be defined, a *sensor* or *movement sensor* that reads `position` requires less [robot configuration](/manage/configuration/) for you to utilize the [sensor API](/program/apis/#sensor) or [movement sensor API](/program/apis/#movement-sensor) than sensors or movement sensors that read `orientation.`

If you don't aren't creating a custom model of sensor, you don't need to follow instructions to configure your sensor to utilize it with the movement sensor API reporting position `Readings`, as long as you are using one of Viam's built-in models of movement sensor that support GPS position readings ([gps-nmea](/components/movement-sensor/gps/gps-nmea/) or [gps-rtk](/components/movement-sensor/gps/gps-rtk/)).
