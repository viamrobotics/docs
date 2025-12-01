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
  - /micro-rdk/sensor/
  - /build/micro-rdk/sensor/
date: "2024-10-21"
hide_children: true
# SME: #team-bucket
---

The sensor component provides an API for getting measurements.

If you have a physical sensor, an API endpoint, or anything else that provides measurements, use a sensor component.

## Configuration

To use a sensor and get its measurements, you need to add it to your machine's configuration.
Physical sensors often require a [board component](/operate/reference/components/board/) with a configured analog-to-digital converter (ADC).
Virtual sensors often function without additional dependencies.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:sensor" type="sensor" no-intro="true">}}

{{< alert title="Add support for other models" color="tip" >}}
If none of the existing models fit your use case, you can [create a modular resource](/operate/modules/support-hardware/) to add support for it.
{{< /alert >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`ultrasonic`](ultrasonic-micro-rdk/) | [HC-SR04](https://www.sparkfun.com/products/15569) ultrasonic sensors |
| [`bme280`](https://github.com/viam-modules/micrordk-bme280) | I2C Driver for the BME280 sensor |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

{{% expand "Measuring movement or power or working with a motor?" %}}

- If your sensor measures GPS, IMU, position, velocity, or acceleration, use a [movement sensor](/operate/reference/components/movement-sensor/).
- If your sensor measured voltage, current, or power consumption of connected hardware use a [power sensor](/operate/reference/components/power-sensor/).
- If your sensor detects speed and direction of rotation of a motor or a joint, use an [encoder](/operate/reference/components/encoder/).

{{% /expand%}}

## API

The [sensor API](/dev/reference/apis/components/sensor/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/sensor-table.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/sensor.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}

To capture data from the sensor, see the [data management service](/data-ai/capture-data/capture-sync/).
