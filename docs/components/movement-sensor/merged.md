---
title: "Configure an merged movement sensor"
linkTitle: "merged"
weight: 40
type: "docs"
description: "Configure an merged movement sensor."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

The `merged` movement sensor model supports a movement sensor that allows you to measure angular and linear velocity at the same time.

Use this model of sensor in the following cases:
CASE 1: A SetVelocity call with Y and Z supplied, movement_sensor is LinearVelocitySupporting and AngularVelocitySupporting, use both readings in a feedback loop to reduce velocity error.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `merged` model.

Click **Create Component**.

{{< imgproc src="/components/movement-sensor/mpu6050-builder.png" alt="Creation of an `merged` movement sensor in the Viam app config builder." resize="600x" >}}

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
        "position": ["gps1"],
        "orientation" : ["vectornav"],
        "compass_heading" : ["gps1"],
        "angular_velocity":[""],
        "linear_velocity": ["gps1"],
        "linear_acceleration": ["adxl345"]
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
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {
        "i2cs": [
          {
            "name": "default_i2c_bus",
            "bus": "1"
          }
        ]
      }
    },
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
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`position` | string | **Dependent on Readings Type Supported** If your movement sensor reads position. |
`orientation` | string | **Dependent on Readings Type Supported** If your movement sensor reads orientation. |
`compass_heading` | boolean | **Dependent on Readings Type Supported** If your movement sensor reads compass heading position. |
`linear_velocity` | boolean | **Dependent on Readings Type Supported** If your movement sensor reads linear velocity. |
`angular_velocity` | boolean | **Dependent on Readings Type Supported** If your movement sensor reads angular velocity. |
`linear_acceleration` | boolean | **Dependent on Readings Type Supported** If your movement sensor reads angular velocity. |
