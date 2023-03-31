---
title: "Create a Custom Sensor Model"
linkTitle: "fake"
weight: 50
draft: false
type: "docs"
description: "Configure a fake sensor to use for testing."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---

Use a `fake` sensor to test implementing a sensor component on your robot without any physical hardware.

Configure a `fake` sensor as follows:

{{< tabs name="Configure a Fake Sensor" >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** subtab of your robot's page in [the Viam app](https://app.viam.com), navigate to the **Create Component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `fake` model.

<img src="../img/fake-sensor-ui-config.png" alt="An example configuration for a fake sensor in the Viam app Config Builder." style="max-width:900px"/>

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": <"your_sensor_name">,
    "type": "sensor",
    "model": "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` sensors.
Calling [readings](../_index.md#readings) on a `fake` sensor always returns readings of `{"a":1, "b":2, "c":3}`.
