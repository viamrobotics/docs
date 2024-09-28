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
hide_children: true
# SME: #team-bucket
---

Sensor components provide an API for getting measurements.

If you have a physical sensor, an API endpoint, or anything else that provides measurements, use a sensor component.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/0YfP-63OBh8">}}

## Available models

To use a sensor and get its measurements, you need to add it to your machine's configuration.
Physical sensors often require a [board component](/components/board/) with a configured analog-to-digital converter (ADC).
Virtual sensors often function without additional dependencies.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows you the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:sensor" type="sensor" no-intro="true">}}

{{< alert title="Add support for other models" color="tip" >}}
If none of the existing models fit your use case, you can [create a modular resource](/how-tos/sensor-module/) to add support for it.
{{< /alert >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`ultrasonic`](ultrasonic-micro-rdk/) | [HC-SR04](https://www.sparkfun.com/products/15569) ultrasonic sensors |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

{{% expand "Measuring movement or power or working with a motor?" %}}

- If your sensor measures GPS, IMU, position, velocity, or acceleration, use a [movement sensor](/components/movement-sensor/).
- If your sensor measured voltage, current, or power consumption of connected hardware use a [power sensor](/components/power-sensor/).
- If your sensor detects speed and direction of rotation of a motor or a joint, use an [encoders](/components/encoder/).

{{% /expand%}}

## API

The [sensor API](/appendix/apis/components/sensor/), which supports the following methods:

{{< readfile "/static/include/components/apis/generated/sensor-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/how-tos/collect-sensor-data/" noimage="true" %}}
{{< /cards >}}

To capture data from the sensor, see the [data management service](/services/data/).
