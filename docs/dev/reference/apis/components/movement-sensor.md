---
title: "Movement sensor API"
linkTitle: "Movement sensor"
weight: 110
type: "docs"
description: "Give commands for getting the current GPS location, linear velocity and acceleration, angular velocity and acceleration and heading."
icon: true
images: ["/icons/components/imu.svg"]
date: "2022-10-10"
aliases:
  - /appendix/apis/components/movement-sensor/
# updated: ""  # When the content was last entirely checked
---

The movement sensor API allows you to give commands to your [movement sensor components](/operate/reference/components/movement-sensor/) for getting a GPS location, linear velocity and acceleration, angular velocity and acceleration and heading.

Different movement sensors provide different data, so be aware that not all of the methods below are supported by all movement sensors.

{{< alert title="Tip" color="tip" >}}
You can run `GetProperties` on your sensor for a list of its supported methods.
{{< /alert >}}

<!-- IMPORTANT: This resource uses a manual table file. Automation does not update this file! -->
<!-- Please be sure to update this manual file if you are updating movement-sensor! -->

{{< readfile "/static/include/components/apis/movement-sensor.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your movement sensor and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a movement sensor called `"my_movement_sensor"` configured as a component of your machine.
If your movement sensor has a different name, change the `name` in the code.

Import the movement sensor package for the SDK you are using:

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
