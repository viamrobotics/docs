---
title: "How Compass Heading is Measured in Viam"
linkTitle: "Compass Heading"
weight: 10
type: "docs"
description: "Use compass heading measurements reported by some models of movement sensor."
---

Compass heading measurements are read by the following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/):

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

An example of a `Compass Heading` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

## Usage

Use compass heading readings to determine the *bearing* of your robot, or, the [cardinal direction](https://en.wikipedia.org/wiki/Cardinal_direction) that your robot is facing.
