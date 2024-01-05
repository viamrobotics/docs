---
title: "Configure a Fake Power Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake power sensor to test software without the physical hardware."
tags: ["sensor", "power sensor"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/power-sensor/fake/"
# SME: #team-bucket
---

Use a `fake` power sensor to test implementing a power sensor component on your machine without any physical hardware.

Configure a `fake` power sensor to integrate into your machine:

{{< tabs name="Configure a Fake Power Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component** in the lower-left corner.
Select the type `power_sensor`, then select the `fake` model.
Name your sensor, and click **Create**.

![Fake power sensor configuration panel in the Viam app. No attributes are configured.](/components/power-sensor/fake-config-builder.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-sensor-name>",
  "model": "fake",
  "type": "power_sensor",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` power sensors.

{{< readfile "/static/include/components/test-control/power-sensor-control.md" >}}
