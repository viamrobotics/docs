---
title: "Power Sensor Component"
linkTitle: "Power Sensor"
childTitleEndOverwrite: "Power Sensor"
weight: 70
no_list: true
type: "docs"
description: "A device that provides information about a machine's power systems, including voltage, current, and power consumption."
tags: ["sensor", "components", "power sensor", "ina219", "ina226", "renogy"]
icon: true
images: ["/icons/components/power-sensor.svg"]
modulescript: true
aliases:
  - "/components/power-sensor/"
hide_children: true
# SME: #team-bucket
---

A power sensor is a device that reports measurements of the voltage, current, and power consumption in your machine's system.
Integrate this component to monitor your power levels.

## Related services

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:power_sensor" type="power_sensor">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your power sensor with Viam’s client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Once connected, you can control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a power sensor called `"my_power_sensor"` configured as a component of your machine.
If your power sensor has a different name, change the `name` in the code.

Import the power sensor package for the SDK you are using:
{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.power_sensor import PowerSensor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/powersensor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The power sensor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/power_sensor-table.md" >}}

{{< readfile "/static/include/components/apis/generated/power_sensor.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
