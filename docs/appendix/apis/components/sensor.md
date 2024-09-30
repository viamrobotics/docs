---
title: "Sensor API"
linkTitle: "Sensor"
weight: 20
type: "docs"
description: "Commands for getting sensor readings."
icon: true
images: ["/icons/components/sensor.svg"]
---

The sensor API allows you to get measurements from your [sensor components](/components/sensor/).

The sensor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/sensor-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a sensor called `"my_sensor"` configured as a component of your machine.
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

{{< readfile "/static/include/components/apis/generated/sensor.md" >}}
