---
title: "How Compass Heading is Measured in Viam"
linkTitle: "Compass Heading"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the compass heading measurements reported by some models of movement sensor."
---

How Viam's platform reads and utilizes the compass heading measurements reported as `Readings` by the following {{< glossary_tooltip term_id="model" text="models" >}} of [movement sensor](/components/movement-sensor/) components:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)
- [gps-nmea-rtk-pmtk](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [gps-nmea-rtk-serial](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

An example of a `Compass Heading` reading:

## Client side

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

## Server side

<!-- TODO: add terminal output or short code snippet -->

## Usage

Use compass heading readings to determine the *bearing* of your robot, or, the [cardinal direction](https://en.wikipedia.org/wiki/Cardinal_direction) that your robot is facing.
