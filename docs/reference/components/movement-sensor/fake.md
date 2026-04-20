---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake movement-sensor model. Fake movement sensor to test software without any hardware."
images: ["/icons/components/imu.svg"]
aliases:
  - "/components/movement-sensor/fake/"
  - "/reference/components/movement-sensor/fake/"
component_description: "A model for testing, with no physical hardware."
# SMEs: Rand
---

You can use the `fake` movement sensor model to test movement sensor code without connecting to any actual hardware.

The `fake` model supports all movement sensor methods: `Accuracy`, `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `Properties`, and `Readings`.
Note that this model does not get any actual readings, so it supports these methods by returning placeholder data.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "model": "fake",
      "api": "rdk:component:movement_sensor",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myFakeSensor",
      "model": "fake",
      "api": "rdk:component:movement_sensor"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}
