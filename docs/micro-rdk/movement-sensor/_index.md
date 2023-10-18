---
title: "Micro-RDK Movement Sensor Models"
linkTitle: "Movement Sensor"
weight: 30
type: "docs"
description: "Movement Sensor support in the micro-rdk."
images: ["/icons/components/imu.svg"]
tags: ["movement sensor", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

The micro-RDK currently supports the following models of Movement Sensor:

| Model | Description |
| ----- | ----------- |
| [`single`](single/) | |
| [`incremental`](incremental/) | |

The [Movement Sensor API](/components/Movement Sensor/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/components/Movement Sensor/#stop)
- [`SetPower()`](/components/Movement Sensor/#setpower)