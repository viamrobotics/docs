---
title: "Configure a Fake Movement Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake movement sensor to test software without any hardware."
images: ["/components/img/components/imu.svg"]
# SMEs: Rand
---

You can use the `fake` movement sensor model to test movement sensor code without connecting to any actual hardware.

The `fake` model supports all movement sensor methods: `Accuracy`, `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `Properties`, and `Readings`.
Note that this model does not get any actual readings, so it supports these methods by returning placeholder data.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `fake` model.

Click **Create Component**.

![Creation of an `fake` movement sensor in the Viam app config builder.](../img/fake-builder.png)

Edit and fill in the attributes as applicable.

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
