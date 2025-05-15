---
title: "Power sensor API"
linkTitle: "Power sensor"
weight: 120
type: "docs"
description: "Commands for getting measurements of voltage, current, and power consumption."
icon: true
images: ["/icons/components/power-sensor.svg"]
date: "2022-10-10"
aliases:
  - /appendix/apis/components/power-sensor/
# updated: ""  # When the content was last entirely checked
---

The power sensor API allows you to give commands to your [power sensor components](/operate/reference/components/power-sensor/) for getting measurements of voltage, current, and power consumption.

The power sensor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/power_sensor-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your power sensor and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Once connected, you can control your machine programmatically by adding API method calls as shown in the following examples.

The following examples assume you have a power sensor called `"my_power_sensor"` configured as a component of your machine.
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

{{< readfile "/static/include/components/apis/generated/power_sensor.md" >}}
