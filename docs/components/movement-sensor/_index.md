---
title: "Movement Sensor Component"
linkTitle: "Movement Sensor"
childTitleEndOverwrite: "Movement Sensor"
weight: 70
type: "docs"
description: "A sensor that measures location, kinematic data, or both."
tags: ["movement sensor", "gps", "imu", "sensor", "components"]
icon: true
images: ["/icons/components/imu.svg"]
no_list: true
modulescript: true
aliases:
  - /components/movement-sensor/
  - /micro-rdk/movement-sensor/
  - /build/micro-rdk/movement-sensor/
# SME: Rand
---

Movement sensors provide an API for GPS location, linear velocity and acceleration, angular velocity and acceleration and heading.

If you have hardware or software that provides such measurements, use a movement sensor component.

## Available models

To use a movement sensor and get its measurements, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:movement_sensor" type="movement_sensor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`accel-adxl345`](accel-adxl345-micro-rdk/) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer |
| [`gyro-mpu6050`](gyro-mpu6050-micro-rdk/) | A gyroscope/accelerometer manufactured by TDK InvenSense |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [movement sensor API](/appendix/apis/components/movement-sensor/) supports the following methods:

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

<!-- IMPORTANT: This resource uses a manual table file. Automation does not update this file! -->
<!-- Please be sure to update this manual file if you are updating movement-sensor! -->

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/how-tos/collect-sensor-data/" noimage="true" %}}
{{< /cards >}}

To capture data from the movement sensor or use it for motion, see the following services:

- [data management service](/services/data/): to capture and sync the movement sensor's data
- [motion service](/services/motion/): to move machines or components of machines
- [navigation service](/services/navigation/): to navigate with GPS
- [SLAM service](/services/slam/): for mapping
