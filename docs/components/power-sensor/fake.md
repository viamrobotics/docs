---
title: "Configure a Fake Power Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake power sensor to test software without the physical hardware."
tags: ["sensor", "power sensor"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/power-sensor/fake/"
component_description: "A digital power sensor for testing."
# SME: #team-bucket
---

Configure a `fake` power sensor to test implementing a power sensor component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Power Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `power_sensor` type, then select the `fake` model.
Enter a name or use the suggested name for your power sensor and click **Create**.

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
