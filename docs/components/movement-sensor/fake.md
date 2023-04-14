---
title: "Configure a Fake Movement Sensor"
linkTitle: "fake"
weight: 15
type: "docs"
description: "Configure a fake movement sensor to test software without any hardware."
# SMEs: Rand
---

You can use the `fake` movement sensor model to test movement sensor code without connecting to any actual hardware.

{{< tabs >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** sub-tab, navigate to the **Create Component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `fake` model.

![Creation of an `fake` movement sensor in the Viam app config builder.](../img/fake-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "fake",
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
      "type": "movement_sensor",
      "model": "fake"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}
