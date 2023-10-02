---
title: "Configure a fake power sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake power sensor to test software without the physical hardware."
tags: ["sensor", "power sensor"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
# SME: #team-bucket
---

Use a `fake` power sensor to test implementing a power sensor component on your robot without any physical hardware.

Configure a `fake` power sensor to integrate into your robot:

{{< tabs name="Configure a Fake Power Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component** in the lower-left corner.
Select the type `power_sensor`, then select the `fake` model.
Name your sensor, and click **Create**.

{{<imgproc src="/components/power-sensor/fake-config-builder.png" resize="750x" declaredimensions=true alt="Fake power sensor configuration builder">}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-sensor-name>",
  "type": "power_sensor",
  "model": "fake",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` power sensors.

{{< readfile "/static/include/components/test-control/power-sensor-control.md" >}}
