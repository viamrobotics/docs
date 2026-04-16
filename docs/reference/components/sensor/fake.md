---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake sensor model. Fake sensor to use for testing."
tags: ["sensor", "components"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/sensor/fake/"
  - "/operate/reference/components/sensor/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: #team-bucket
---

Configure a `fake` sensor to test implementing a sensor component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Sensor" >}}
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

A call to [`Readings()`](/reference/apis/components/sensor/#getreadings) on a `fake` sensor always returns readings of `{"a":1, "b":2, "c":3}`.

{{% /alert %}}
