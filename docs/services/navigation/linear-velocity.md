---
title: "How Linear Velocity is Measured in Viam"
linkTitle: "Linear Velocity"
weight: 10
type: "docs"
description: "How to use the linear velocity measurements reported by some models of movement sensor."
---

Linear velocity measurements are read by the following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/):

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

An example of a `Linear Velocity` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

## Usage

If you want to read linear velocity, [configure a capable movement sensor](/components/movement-sensor/#configuration) on your robot.
Use linear velocity readings to determine the speed at which your robot is moving through space.
Use [linear acceleration](/services/navigation/linear-acceleration/) readings from another movement sensor to determine the rate of change of this speed.
