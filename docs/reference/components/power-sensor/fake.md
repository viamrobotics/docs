---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake power-sensor model. Fake power sensor to test software without the physical hardware."
tags: ["sensor", "power sensor"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/operate/reference/components/power-sensor/fake/"
  - "/components/power-sensor/fake/"
  - "/reference/components/power-sensor/fake/"
component_description: "A model for testing, with no physical hardware."
# SME: #team-bucket
---

Configure a `fake` power sensor to test implementing a power sensor component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Power Sensor" >}}
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
