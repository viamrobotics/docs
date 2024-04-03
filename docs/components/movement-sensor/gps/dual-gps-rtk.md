---
title: "Configure a Dual GPS Movement Sensor"
linkTitle: "dual-gps-rtk"
weight: 10
type: "docs"
description: "Configure a movement sensor that calculates compass heading from two gps movement sensors."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

The `dual-gps-rtk` model of movement sensor calculates a compass heading from two GPS movement sensors, and returns the midpoint position between the first and second GPS devices as its position.
In addition to [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading), this model provides data for [`GetPosition()`](/components/movement-sensor/#getposition) and [`GetAccuracy()`](/components/movement-sensor/#getaccuracy).

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `movement-sensor` type, then select the `dual-gps-rtk` model.
Enter a name for your movement sensor and click **Create**.

![Creation of a `dual-gps-rtk` movement sensor in the Viam app config builder.](/components/movement-sensor/dual-gps-rtk-builder.png)

Copy and paste the following attribute template into your movement sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your movement sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "first_gps": "<name-of-your-first-gps-movement-sensor>",
  "second_gps": "<name-of-your-second-gps-movement-sensor>",
  "offset_degrees": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "first_gps": "nmea-1",
  "second_gps": "nmea-2",
  "offset_degrees": 90
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "your-dual-gps-rtk",
      "model": "dual-gps-rtk",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "first_gps": "<name-of-your-first-gps-movement-sensor>",
        "second_gps": "<name-of-your-second-gps-movement-sensor>",
        "offset_degrees": <int>
      },
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
      "name": "your-dual-gps-rtk",
      "model": "dual-gps-rtk",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "first_gps": "nmea-1",
        "second_gps": "nmea-2",
        "offset_degrees": 90
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for a `dual-gps-rtk` movement sensor:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `first_gps` | int | **Required** | The name you have configured for the first movement sensor you want to combine the measurements from. Must be a GPS model. |
| `second_gps` | string | **Required** | The name you have configured for the second movement sensor you want to combine the measurements from. Must be a GPS model. |
| `offset_degrees` | int | Optional | The value to offset the compass heading calculation between the two GPS devices based on their positions on the base. Calculate this as the degrees between the vector from `first_gps` to `second_gps` and the vector from the vehicle's back to the vehicle's front, counterclockwise. {{< imgproc src="/components/movement-sensor/offset_degrees.png" alt="Rand's diagram of 3 offset degree calculations." resize="600x" >}} <br> Default: `90` |

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/fleet/machines/#control) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.
The sections in the panel include the position, compass heading, and accuracy.

{{<imgproc src="/components/movement-sensor/movement-sensor-control-tab-dual.png" resize="800x" declaredimensions=true alt="The dual GPS movement sensor component in the control tab">}}
