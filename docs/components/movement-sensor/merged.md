---
title: "Configure an merged movement sensor"
linkTitle: "merged"
weight: 40
type: "docs"
description: "Configure an merged movement sensor."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

The `merged` movement sensor model supports a movement sensor that allows you to get multiple types of [`Readings`](/components/movement-sensor/#getreadings), including angular and linear velocity, from *one* movement sensor {{< glossary_tooltip term_id="resource" text="resource" >}} on your robot.

This allows you to aggregate the API methods supported by multiple sensors into a singular sensor client, effectively merging the models of the individual resources.

In other words, the models of the `merged` sensors are combined, making the movement sensor API methods each aggregated model supports available on the `merged` model.

This is especially useful if you want to get readings of position and orientation *or* linear and angular velocity at the same time, which are normally separately supported and returned by [`GPS`](/components/movement-sensor/#configuration) or [`IMU`](/components/movement-sensor/#configuration) models, respectively.

{{% alert title="Usage Tip: Navigation Service" color="tip" %}}
Aggregating the readings of a [`GPS`](/components/movement-sensor/#configuration) and [`IMU`](/components/movement-sensor/#configuration) movement sensor in a `merged` model allows you to reduce velocity error when your robot is trying to [navigate](/services/navigation/) with these position and orientation readings.
{{% /alert %}}

Before configuring a `merged` movement sensor, configure each movement sensor you want to merge as an individual component according to its [model's configuration instructions](/components/movement-sensor/#configuration).
Reference the `name` you configure for each individual component in the `merged` sensor's configuration attributes as shown:

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
        "angular_velocity":["vectornav"],
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
- Use this information to determine which attribute to put its `name` inside the array of.
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
The first sensor in the array that has implemented the relevant API method in its model and does not raise an error at runtime is used by your robot to get that type of reading.
