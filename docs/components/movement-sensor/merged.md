---
title: "Configure an merged movement sensor"
linkTitle: "merged"
weight: 40
type: "docs"
description: "Configure an merged movement sensor."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

The `merged` movement sensor model supports a movement sensor that allows you to get multiple [`Readings`](/components/movement-sensor/#getreadings), including angular and linear velocity, from *one* movement sensor {{< glossary_tooltip term_id="resource" text="resource" >}} on your robot.

This lets you aggregate [`Readings`](/components/movement-sensor/#getreadings) from multiple sensors into a singular sensor instance, effectively merging the models of the individual resources.

In other words, when you call [`GetReadings()`](/components/movement-sensor/#getreadings) on a `merged` sensor, the `Readings` each sensors has taken are combined in one response from your robot.

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
        "angular_velocity":["<your-angular-velocity-sensor-name-2>"],
        "linear_velocity": ["<your-gps-sensor-name-1>"],
        "linear_acceleration": ["<your-adxl345-sensor-name-1>"]
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
        "angular_velocity":[""],
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
- Retrieve this information for your movement sensor by calling [`GetProperties()`](/components/movement-sensor/#getproperties) on the sensor.
- Use this information to determine which attribute to put its `name` inside the array of.

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`position` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads position. |
`orientation` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads orientation. |
`compass_heading` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads compass heading position. |
`linear_velocity` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads linear velocity. |
`angular_velocity` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads angular velocity. |
`linear_acceleration` | array | **Dependent on Readings Type Supported** | The `name` of the movement sensor you want to merge, if it reads linear acceleration |

Note that `Readings` are only taken and merged from the first sensor in the respective attribute's array that does not produce an error at runtime.
