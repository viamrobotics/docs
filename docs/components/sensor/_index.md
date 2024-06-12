---
title: "Sensor Component"
linkTitle: "Sensor"
childTitleEndOverwrite: "Sensor Component"
weight: 70
no_list: true
type: "docs"
description: "A device that sends information about the outside world to the computer controlling a machine."
tags: ["sensor", "components"]
icon: true
images: ["/icons/components/sensor.svg"]
modulescript: true
aliases:
  - "/components/sensor/"
hide_children: true
# SME: #team-bucket
---

A _sensor_ is a device that can measure information about the outside world.
Add a sensor component to your machine to send the information the sensor measures to the computer controlling the machine.

{{% alert title="Tip" color="tip" %}}

Viam has three additional component types defined separately from _sensor_ that you can use to implement sensors with specific functions:

1. [Movement sensors](/components/movement-sensor/) for Global Positioning System (GPS) units, inertial measurement units (IMUs), and other sensors that detect position, velocity, and acceleration.
2. [Power sensors](/components/power-sensor/) for sensors that can detect voltage, current, and power consumption of connected hardware.
3. [Encoders](/components/encoder/) for sensors that can detect speed and direction of rotation of a motor or a joint.

{{% /alert %}}

Most machines with a sensor need at least the following hardware:

- A [board](/components/board/)
- Depending on your sensor's output type (analog or digital), an analog-to-digital converter (ADC) may be necessary to allow the sensor to communicate with the board

## Related services

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:sensor" type="sensor">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your sensor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a sensor called `"my_sensor"` configured as a component of your machine.
If your sensor has a different name, change the `name` in the code.

Be sure to import the sensor package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.sensor import Sensor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/sensor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The sensor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/sensor-table.md" >}}

{{< readfile "/static/include/components/apis/generated/sensor.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot/" %}}
{{% card link="/tutorials/projects/tipsy/" %}}
{{< /cards >}}
