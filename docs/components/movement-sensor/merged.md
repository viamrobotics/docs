---
title: "Configure a merged movement sensor"
linkTitle: "merged"
weight: 40
type: "docs"
description: "Configure a merged movement sensor."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

The `merged` movement sensor model is an abstraction that combines data from multiple movement sensors.
This allows you to aggregate the API methods supported by multiple sensors into a singular sensor client.

This is especially useful if you want to get readings of position and orientation *or* linear and angular velocity at the same time, which are normally separately supported and returned by [`GPS`](/components/movement-sensor/#configuration) or [`IMU`](/components/movement-sensor/#configuration) models, respectively.

To reduce velocity error when your robot is using the [navigation service](/services/navigation/), aggregate `Position()` from a [`GPS`](/components/movement-sensor/#configuration) and `Orientation()` from an [`IMU`](/components/movement-sensor/#configuration) movement sensor in a `merged` model.

Configure a [navigation service](/services/navigation/) to use your merged sensor to navigate.

Before configuring a `merged` movement sensor, configure each movement sensor you want to merge as an individual component according to its [model's configuration instructions](/components/movement-sensor/#configuration).
Reference the `name` you configure for each individual component in the `merged` sensor's configuration attributes:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `merged` model.

Click **Create Component**.

{{< imgproc src="/components/movement-sensor/merged-config-builder.png" alt="Creation of an `merged` movement sensor in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "merged",
      "attributes": {
        "position": ["<your-gps-sensor-name-1>", "<your-gps-sensor-name-2>"],
        "orientation" : ["<your-imu-sensor-name-1>"],
        "compass_heading" : ["<your-gps-sensor-name-1>"],
        "angular_velocity":["<your-imu-sensor-name-1>"],
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
    "type": "movement_sensor",
    "model": "merged",
    "attributes": {
        "position": ["gps1"],
        "orientation" : ["vectornav"],
        "compass_heading" : ["gps1"],
        "angular_velocity":["vectornav", "mpu6050"],
        "linear_velocity": ["gps1"],
        "linear_acceleration": ["adxl345"]
    }, 
      "depends_on":[]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

Configure an array of the `name` of each movement sensor you want to add to your robot as a merged resource in the attributes of the `merged` movement sensor model:

- The name of each attribute represents the `Property` that that particular movement sensor supports, or the type of reading or measurement that it takes.
- Get the properties supported by each model from its [model configuration documentation](/components/movement-sensor/#configuration), or by calling [`GetProperties()`](/components/movement-sensor/#getproperties) on the sensor.
- Put the `name` of each movement sensor into the attribute array for the type of reading it supports.
You can use the same sensor for multiple attributes if it supports multiple properties.

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`position` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads position. |
`orientation` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads orientation. |
`compass_heading` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads compass heading position. |
`linear_velocity` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads linear velocity. |
`angular_velocity` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads angular velocity. |
`linear_acceleration` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads linear acceleration |

Note that only one sensor from each array can be used to retrieve each type of reading.
Your robot uses the first sensor in the array that has implemented the relevant API method in its model and does not raise an error at runtime.
For instance, in the **JSON Example** above, if both `"vectornav"` and `"mpu6050"` support returning `angular_velocity`, `"mpu6050"` is only used to read angular velocity on the robot if `"vectornav"` returns an error at runtime.
