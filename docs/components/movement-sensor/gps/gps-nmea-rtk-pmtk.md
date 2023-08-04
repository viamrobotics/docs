---
title: "Configure an NTRIP-based RTK GPS with an I2C Connection"
linkTitle: "gps-nmea-rtk-pmtk"
weight: 10
type: "docs"
description: "Configure an NTRIP-based RTK GPS."
images: ["/icons/components/imu.svg"]
# SMEs: Susmita
---

{{% alert title="Stability Notice" color="note" %}}

The `gps-nmea-rtk-pmtk` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the `Position`, `CompassHeading` and `LinearVelocity` methods.
You can obtain fix and correction data by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](../../../sensor/).

The `gps-ntrip` <!-- this isn't a model. What should this say? --> movement sensor model supports [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [real time kinematic positioning (RTK)](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS units ([such as these](https://www.sparkfun.com/rtk)).

The chip requires a correction source to get to the required positional accuracy.
The `gps-nmea-rtk-pmtk` model uses an over-the-internet correction source and sends the data over I<sup>2</sup>C.
