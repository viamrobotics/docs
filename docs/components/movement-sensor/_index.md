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

A movement sensor component is a sensor that gives data on where a machine is and how fast it is moving.
Examples of movement sensors include global positioning systems (GPS), inertial measurement units (IMUs), accelerometers and gyroscopes.

{{% alert title="Tip" color="tip" %}}

Viam also supports generic [sensors](/components/sensor/) and [encoders](/components/encoder/).

{{% /alert %}}

## Related services

{{< cards >}}
{{< relatedcard link="/services/motion/" >}}
{{< relatedcard link="/services/navigation/" >}}
{{< relatedcard link="/services/slam/" >}}
{{< /cards >}}

## Supported models

To use your movement sensor component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="RDK" %}}

{{<resources api="rdk:component:movement_sensor" type="movement_sensor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`accel-adxl345`](accel-adxl345-micro-rdk/) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer |
| [`gyro-mpu6050`](gyro-mpu6050-micro-rdk/) | A gyroscope/accelerometer manufactured by TDK InvenSense |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## Control your movement sensor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a movement sensor called `"my_movement_sensor"` configured as a component of your machine.
If your movement sensor has a different name, change the `name` in the code.

Be sure to import the movement sensor package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.movement_sensor import MovementSensor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/movementsensor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

<!-- IMPORTANT: This resource uses a manual table file. Automation does not update this file! -->
<!-- Please be sure to update this manual file if you are updating movement-sensor! -->

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

{{< readfile "/static/include/components/apis/generated/movement_sensor.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

Try adding a movement sensor to your [mobile robot](/components/base/) and writing some code with our [SDKs](/appendix/apis/) to implement closed-loop movement control for your machine.

Or, try configuring [data capture](/services/data/) on your movement sensor.

{{< snippet "social.md" >}}
