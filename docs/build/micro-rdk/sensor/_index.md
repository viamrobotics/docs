---
title: "Micro-RDK Sensor Models"
linkTitle: "Sensor"
weight: 30
type: "docs"
description: "Support in the micro-RDK for sensors, devices that measur information about the outside world."
images: ["/icons/components/sensor.svg"]
tags: ["sensor", "components", "micro-rdk"]
no_list: true
# SMEs: Andrew Morrow
---

A sensor is a device that can measure information about the outside world.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Sensor Component](/components/sensor/).

## Supported models

For configuration information, click a supported sensor model name:

<!-- prettier-ignore -->
| Model |Description |
| ----- | ---------- |
| [`ultrasonic`](ultrasonic/) | [HC-SR04](https://www.sparkfun.com/products/15569) ultrasonic sensors |

{{% readfile "/static/include/micro-create-your-own.md" %}}

## API

The micro-RDK [sensor API](/components/sensor/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`GetReadings()`](/components/sensor/#getreadings)
