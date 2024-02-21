---
title: "Configure a Sensor-Controlled Base"
linkTitle: "sensor-controlled"
weight: 40
type: "docs"
description: "Configure a sensor-controlled base, a robotic base with feedback control from a movement sensor."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/sensor-controlled/"
# SMEs: Rand H., Martha J.
---

A `sensor-controlled` base supports a robotic base with feedback control from a movement sensor.

{{% alert title="Requirements" color="note" %}}
In order to use feedback control for [SetVelocity()](/components/base/#setvelocity), you must provide a movement sensor that implements [AngularVelocity()](/components/base/#getangularvelocity) and [LinearVelocity()](/components/base/#getlinearvelocity).

In order to use feedback control for [Spin()](/components/base/#spin), you must provide a movement sensor that implements [Orientation()](/components/base/#getorientation).
{{% /alert %}}

To configure a `sensor-controlled` base as a component of your machine, first configure the [model of base](/components/base/) you want to wrap with feedback control and each required [movement sensor](/components/movement-sensor/).
To see what models of movement sensor report which feedback, reference the appropriate column in [Movement Sensor API](/components/movement-sensor/#api).

Configure a `sensor-controlled` base as follows:

{{< tabs name="Configure a Sensor-Controlled Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in the [Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `sensor-controlled` model.
Enter a name for your base and click **Create**.

{{< imgproc src="/components/base/sensor-controlled-base-ui-config.png" alt="An example configuration for a sensor-controlled base in the Viam app config builder" resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    { ... INSERT MOVEMENT SENSOR CONFIGURATION },
    { ... INSERT BASE CONFIGURATION },
    {
      "name": "my-sensor-controlled-base",
      "model": "sensor-controlled",
      "type": "base",
      "namespace": "rdk",
      "attributes": {
        "movement_sensor": [
          "<your-orientation-or-velocity-movement-sensor-1>",
          "<your-orientation-or-velocity-movement-sensor-2>"
        ],
        "base": "<your-base>"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `sensor-controlled` bases:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `movement_sensor` | array | **Required** | Array with the `name`s of any movement sensors on your base you want to gather feedback from. The driver will select the first movement sensor providing appropriate feedback for either the `SetVelocity()` or the `Spin()` endpoint. |
| `base` | string | **Required** | String with the `name` of the base you want to wrap with sensor control. |
| `control_parameters` | object | Optional | A JSON object containing the coefficients for the proportional, integral, and derivative terms for linear and angular velocity. If you want these values to be auto-tuned, you can set all values to 0: `[ { "type": "linear_velocity", "p": 0, "i": 0, "d": 0 }, { "type": "angular_velocity", "p": 0, "i": 0, "d": 0 } ]`, and `viam-server` will auto-tune and log the calculated values. Tuning takes several seconds and spins the motors. Copy the values from the logs and add them to the configuration once tuned for the values to take effect. For more information see [Feedback contrel](#feedback-control). |

## Feedback control

### SetVelocity

{{< readfile "/static/include/components/base-sensor.md" >}}

## Spin

Spin implements a basic form of feedback control that, for a spin of less than 360 degrees, monitors how far the base has spun and stops once it has reached the goal position.

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

The following base control API methods are available on a `sensor-controlled` base:

- [SetVelocity()](/components/base/#setvelocity): available if base is configured to receive angular and linear velocity feedback.
- [Spin()](/components/base/#spin): available if base is configured to receive orientation feedback.
