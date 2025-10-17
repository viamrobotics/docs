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
component_description: "A model for testing, with no physical hardware."
toc_hide: true
# SMEs: Rand
---

You can use the `fake` movement sensor model to test movement sensor code without connecting to any actual hardware.

The `fake` model supports all movement sensor methods: `Accuracy`, `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `Properties`, and `Readings`.
Note that this model does not get any actual readings, so it supports these methods by returning placeholder data.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `movement-sensor` type, then select the `fake` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/fake-builder.png" alt="Creation of an `fake` movement sensor." resize="1200x" style="width:650px" class="shadow"  >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
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

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/manage/troubleshoot/teleoperate/default-interface/) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.
The sections in the panel include the position, orientation, angular velocity, linear velocity, and linear acceleration.

{{<imgproc src="/components/movement-sensor/movement-sensor-control-tab.png" resize="800x" declaredimensions=true alt="The movement sensor component in the control tab">}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/movement-sensor.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/movement-sensor/" customTitle="Movement sensor API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
