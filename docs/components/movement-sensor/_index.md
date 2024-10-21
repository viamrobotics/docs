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
date: "2024-10-21"
aliases:
  - /components/movement-sensor/
  - /micro-rdk/movement-sensor/
  - /build/micro-rdk/movement-sensor/
# SME: Rand
---

The movement sensor component provides an API for GPS location, linear velocity and acceleration, angular velocity and acceleration and heading.

If you have hardware or software that provides such measurements, use a movement sensor component.

## Configuration

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

If your movement sensor is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Review your movement sensor model's documentation to ensure you have configured all required attributes.
3. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the movement sensor there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

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
