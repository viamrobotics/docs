---
title: "Movement sensor API"
linkTitle: "Movement Sensor"
titleMustBeLong: true
weight: 20
type: "docs"
description: "The movement sensor API allows you to give commands to your movement sensor components with code instead of with the graphical interface of the Viam app"
icon: true
images: ["/icons/components/imu.svg"]
---

The movement sensor API allows you to give commands to your [movement sensor components](/components/movement-sensor/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

<!-- IMPORTANT: This resource uses a manual table file. Automation does not update this file! -->
<!-- Please be sure to update this manual file if you are updating movement-sensor! -->

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

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

{{< readfile "/static/include/components/apis/generated/movement_sensor.md" >}}
