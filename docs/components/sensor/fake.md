---
title: "Create a Fake Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake sensor to use for testing."
tags: ["sensor", "components"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/sensor/fake/"
# SME: #team-bucket
---

Use a `fake` sensor to test implementing a sensor component on your machine without any physical hardware.

Configure a `fake` sensor as follows:

{{< tabs name="Configure a Fake Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `sensor` type, then select the `fake` model.
Enter a name for your sensor and click **Create**.

![An example configuration for a fake sensor in the Viam app Config Builder. Attributes are left blank.](/components/sensor/fake-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-sensor-name>",
  "model": "fake",
  "type": "sensor",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` sensors.

{{% alert title="Info" color="info" %}}

A call to [`Readings()`](../#getreadings) on a `fake` sensor always returns readings of `{"a":1, "b":2, "c":3}`.

{{% /alert %}}

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}
