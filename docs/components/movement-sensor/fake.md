---
title: "Configure a Fake Movement Sensor"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake movement sensor to test software without any hardware."
images: ["/icons/components/imu.svg"]
toc_hide: true
aliases:
  - "/components/movement-sensor/fake/"
component_description: "Used to test code without hardware."
# SMEs: Rand
---

You can use the `fake` movement sensor model to test movement sensor code without connecting to any actual hardware.

The `fake` model supports all movement sensor methods: `Accuracy`, `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `Properties`, and `Readings`.
Note that this model does not get any actual readings, so it supports these methods by returning placeholder data.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `fake` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/fake-builder.png" alt="Creation of an `fake` movement sensor in the Viam app config builder." resize="1200x" style="width:650px" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "model": "fake",
      "type": "movement_sensor",
      "namespace": "rdk",
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
      "type": "movement_sensor",
      "namespace": "rdk"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/fleet/control/) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.
The sections in the panel include the position, orientation, angular velocity, linear velocity, and linear acceleration.

{{<imgproc src="/components/movement-sensor/movement-sensor-control-tab.png" resize="800x" declaredimensions=true alt="The movement sensor component in the control tab">}}
