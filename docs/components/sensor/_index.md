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

The _sensor_ component represents a device that can measure information about the outside world.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/0YfP-63OBh8">}}

## Available models

To use a sensor and get its measurements, you have to add it as well as any dependencies, such as a [board component](/components/board/) with a configured analog-to-digital converter (ADC), to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows you the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:sensor" type="sensor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

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

## Related services

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< /cards >}}

## API

The sensor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/sensor-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot/" %}}
{{% card link="/tutorials/projects/tipsy/" %}}
{{< /cards >}}
