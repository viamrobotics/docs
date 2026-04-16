---
title: "merged"
linkTitle: "merged"
weight: 40
type: "docs"
description: "Reference for the merged movement-sensor model. Merged movement sensor."
images: ["/icons/components/imu.svg"]
aliases:
  - "/components/movement-sensor/merged/"
  - "/operate/reference/components/movement-sensor/merged/"
component_description: "A model that allows you to aggregate the API methods supported by multiple sensors into a singular sensor client, effectively merging the models of the individual resources."
# SMEs: Rand
---

The `merged` movement sensor model is an abstraction that combines data from multiple movement sensors.
This allows you to aggregate the API methods supported by multiple sensors into a singular sensor client.

This is especially useful if you want to get readings of position and orientation _or_ linear and angular velocity at the same time, which are normally separately supported and returned by [`GPS`](/reference/components/movement-sensor/) or [`IMU`](/reference/components/movement-sensor/) models, respectively.

To reduce velocity error when your machine is using the [navigation service](/operate/reference/services/navigation/), aggregate `Position()` from a [`GPS`](/reference/components/movement-sensor/) and `Orientation()` from an [`IMU`](/reference/components/movement-sensor/) movement sensor in a `merged` model.

Configure a [navigation service](/operate/reference/services/navigation/) to use your merged sensor to navigate.

Before configuring a `merged` movement sensor, configure each movement sensor you want to merge as an individual component according to its [model's configuration instructions](/reference/components/movement-sensor/).
Reference the `name` you configure for each individual component in the `merged` sensor's configuration attributes:

{{< tabs >}}
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
- Get the properties supported by each model from its [model configuration documentation](/reference/components/movement-sensor/), or by calling [`GetProperties()`](/reference/apis/components/movement-sensor/#getproperties) on the sensor.
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
