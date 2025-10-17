---
title: "Create a Fake Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake sensor to use for testing."
tags: ["sensor", "components"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/sensor/fake/"
component_description: "A model used for testing, with no physical hardware."
toc_hide: true
# SME: #team-bucket
---

Configure a `fake` sensor to test implementing a sensor component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `sensor` type, then select the `fake` model.
Enter a name or use the suggested name for your sensor and click **Create**.

![An example configuration for a fake sensor. Attributes are left blank.](/components/sensor/fake-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-sensor-name>",
  "model": "fake",
  "api": "rdk:component:sensor",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` sensors.

{{% alert title="Info" color="info" %}}

A call to [`Readings()`](/dev/reference/apis/components/sensor/#getreadings) on a `fake` sensor always returns readings of `{"a":1, "b":2, "c":3}`.

{{% /alert %}}

## Test the sensor

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/sensor.md" >}}

## Next steps

Check out the [sensor API](/dev/reference/apis/components/sensor/) or check out one of these guides:

{{< cards >}}
{{% card link="/dev/reference/apis/components/sensor/" customTitle="Sensor API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{< /cards >}}
