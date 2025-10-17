---
title: "Configure a Merged Movement Sensor"
linkTitle: "merged"
weight: 40
type: "docs"
description: "Configure a merged movement sensor."
images: ["/icons/components/imu.svg"]
toc_hide: true
aliases:
  - "/components/movement-sensor/merged/"
component_description: "A model that allows you to aggregate the API methods supported by multiple sensors into a singular sensor client, effectively merging the models of the individual resources."
toc_hide: true
# SMEs: Rand
---

The `merged` movement sensor model is an abstraction that combines data from multiple movement sensors.
This allows you to aggregate the API methods supported by multiple sensors into a singular sensor client.

This is especially useful if you want to get readings of position and orientation _or_ linear and angular velocity at the same time, which are normally separately supported and returned by [`GPS`](/operate/reference/components/movement-sensor/#configuration) or [`IMU`](/operate/reference/components/movement-sensor/#configuration) models, respectively.

To reduce velocity error when your machine is using the [navigation service](/operate/reference/services/navigation/), aggregate `Position()` from a [`GPS`](/operate/reference/components/movement-sensor/#configuration) and `Orientation()` from an [`IMU`](/operate/reference/components/movement-sensor/#configuration) movement sensor in a `merged` model.

Configure a [navigation service](/operate/reference/services/navigation/) to use your merged sensor to navigate.

Before configuring a `merged` movement sensor, configure each movement sensor you want to merge as an individual component according to its [model's configuration instructions](/operate/reference/components/movement-sensor/#configuration).
Reference the `name` you configure for each individual component in the `merged` sensor's configuration attributes:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `merged` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/merged-config-builder.png" alt="Creation of an `merged` movement sensor." resize="1200x" style="width:650px" class="shadow"  >}}

Fill in the attributes as applicable to your movement sensor, according to the table below.
For example:

{{< imgproc src="/components/movement-sensor/merged-config-builder-attributes.png" alt="Creation of an `merged` movement sensor with attributes filled in." resize="1200x" style="width:650px" >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "model": "merged",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "position": ["<your-gps-sensor-name-1>", "<your-gps-sensor-name-2>"],
        "orientation": ["<your-imu-sensor-name-1>"],
        "compass_heading": ["<your-gps-sensor-name-1>"],
        "angular_velocity": ["<your-imu-sensor-name-1>"],
        "linear_velocity": ["<your-gps-sensor-name-1>"],
        "linear_acceleration": ["<your-accelerometer-sensor-name-1>"]
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
// { "components": [ { ... },
{
  "name": "<your-sensor-name>",
  "model": "merged",
  "api": "rdk:component:movement_sensor",
  "attributes": {
    "position": ["gps1"],
    "orientation": ["imu-wit"],
    "compass_heading": ["gps1"],
    "angular_velocity": ["imu-wit", "mpu6050"],
    "linear_velocity": ["gps1"],
    "linear_acceleration": ["adxl345"]
  },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

Configure an array of the `name` of each movement sensor you want to add to your machine as a merged resource in the attributes of the `merged` movement sensor model:

- The name of each attribute represents the `Property` that the particular movement sensor supports, or the type of reading or measurement that it takes.
- Get the properties supported by each model from its [model configuration documentation](/operate/reference/components/movement-sensor/#configuration), or by calling [`GetProperties()`](/dev/reference/apis/components/movement-sensor/#getproperties) on the sensor.
- Put the `name` of each movement sensor into the attribute array for the type of reading it supports.
  You can use the same sensor for multiple attributes if it supports multiple properties.

<!-- prettier-ignore -->
| Name                  | Type  | Required? | Description |
| --------------------- | ----- | --------- | ----------- |
| `position`            | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads position.                 |
| `orientation`         | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads orientation.              |
| `compass_heading`     | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads compass heading position. |
| `linear_velocity`     | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads linear velocity.          |
| `angular_velocity`    | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads angular velocity.         |
| `linear_acceleration` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads linear acceleration       |

Note that only one sensor from each array can be used to retrieve each type of reading.
Your machine uses the first sensor in the array that has implemented the relevant API method in its model and does not raise an error at runtime.
For instance, in the **JSON Example** above, if both `"imu-wit"` and `"mpu6050"` support returning `angular_velocity`, `"mpu6050"` is only used to read angular velocity on the machine if `"imu-wit"` returns an error at runtime.

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/manage/troubleshoot/teleoperate/default-interface/) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/movement-sensor.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/movement-sensor/" customTitle="Movement sensor API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
