---
title: "Configure a Fake Movement Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake movement sensor to test software without any hardware."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

You can use the `fake` movement sensor model to test movement sensor code without connecting to any actual hardware.

The `fake` model supports all movement sensor methods: `Accuracy`, `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `Properties`, and `Readings`.
Note that this model does not get any actual readings, so it supports these methods by returning placeholder data.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `movement-sensor` type, then select the `fake` model.
Enter a name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/fake-builder.png" alt="Creation of an `fake` movement sensor in the Viam app config builder." resize="600x" >}}

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

{{< readfile "/static/include/components/test-control/movement-sensor-control.md" >}}
