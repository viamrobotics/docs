---
title: "Configure a GPS"
linkTitle: "GPS"
weight: 2
type: "docs"
description: "Supported GPS models."
# SMEs: Rand
---

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide date for the `Position`, `CompassHeading` and `LinearVelocity` methods.
Fix and Correction data are available by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](../../sensor/).
