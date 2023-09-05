---
title: "Position Measurement"
linkTitle: "Position"
weight: 10
type: "docs"
description: "Use the position measurements reported by some models of movement sensor."
---

The following {{< glossary_tooltip term_id="model" text="models" >}} of the [movement sensor](/components/movement-sensor/) component report Position measurements:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

An `Position` reading specifies the GPS coordinates of an object in 3D space, or, its position in the geographic coordinate system [(GCS)](https://en.wikipedia.org/wiki/Geographic_coordinate_system).

An example of a `Position` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

## Usage

If you want to get a position, first [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.

Position readings allow you to get the *absolute* position of components when using the [motion service](/services/motion/) and [navigation service](/services/navigation/).
This is in contrast to orientation vector readings, which you use to specify relative position.

Absolute readings don't require spatial relationships to be defined.
Unlike a sensor that reads [orientation](/services/navigation/orientation/), a sensor that reads position does not require[configuration](/manage/configuration/) of the [frame system service](/services/frame-system/).
