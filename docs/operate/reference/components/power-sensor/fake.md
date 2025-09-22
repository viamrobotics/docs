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
component_description: "A model for testing, with no physical hardware."
toc_hide: true
# SME: #team-bucket
---

Configure a `fake` power sensor to test implementing a power sensor component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Power Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `power_sensor` type, then select the `fake` model.
Enter a name or use the suggested name for your power sensor and click **Create**.

![Fake power sensor configuration panel. No attributes are configured.](/components/power-sensor/fake-config-builder.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-sensor-name>",
  "model": "fake",
  "api": "rdk:component:power_sensor",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` power sensors.

{{< readfile "/static/include/components/test-control/power-sensor-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/power-sensor.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/power-sensor/" customTitle="Power sensor API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
