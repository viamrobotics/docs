---
title: "Create a fake Sensor"
linkTitle: "fake"
weight: 90
type: "docs"
description: "Configure a fake sensor to use for testing."
tags: ["sensor", "components"]
icon: "/components/img/components/sensor.svg"
images: ["/components/img/components/sensor.svg"]
# SME: #team-bucket
---

Use a `fake` sensor to test implementing a sensor component on your robot without any physical hardware.

Configure a `fake` sensor as follows:

{{< tabs name="Configure a Fake Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `fake` model.
Click **Create component**.

![An example configuration for a fake sensor in the Viam app Config Builder. Attributes are left blank.](../img/fake-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your_sensor_name>",
    "type": "sensor",
    "model": "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` sensors.

{{% alert title="Note" color="note" %}}

A call to [`Readings()`](../#readings) on a `fake` sensor always returns readings of `{"a":1, "b":2, "c":3}`.

{{% /alert %}}
