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
component_description: "A model that wraps other base models with feedback control from a movement sensor"
# SMEs: Rand H., Martha J.
---

A `sensor-controlled` base supports a robotic base with feedback control from a movement sensor.

{{% alert title="Requirements" color="note" %}}
In order to use feedback control, you must provide a movement sensor that implements [AngularVelocity()](/components/movement-sensor/#getangularvelocity) and [LinearVelocity()](/components/movement-sensor/#getlinearvelocity). This will enable feedback control for [SetVelocity()](/components/base/#setvelocity).

In order to use feedback control for [Spin()](/components/base/#spin), you must also provide a movement sensor that implements [Orientation()](/components/movement-sensor/#getorientation).

In order to use feedback control for [MoveStraight()](/components/base/#spin), you must also provide a movement sensor that implements [Position()](/components/movement-sensor/#getposition). Additionally, heading feedback control while moving straight can be used by providing a movement sensor that implements [Orientation()](/components/movement-sensor/#getorientation) or [CompassHeading()](/components/movement-sensor/#getcompassheading).
{{% /alert %}}

To configure a `sensor-controlled` base as a component of your machine, first configure the [model of base](/components/base/) you want to wrap with feedback control and each required [movement sensor](/components/movement-sensor/).
To see what models of movement sensor report which feedback, reference the appropriate column in [Movement Sensor API](/components/movement-sensor/#api).

Configure a `sensor-controlled` base as follows:

{{< tabs name="Configure a Sensor-Controlled Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `base` type, then select the `sensor-controlled` model.
Enter a name or use the suggested name for your base and click **Create**.

{{< imgproc src="/components/base/sensor-controlled-base-ui-config.png" alt="An example configuration for a sensor-controlled base in the Viam app config builder" resize="1200x" style="width: 600x">}}

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
| `movement_sensor` | array | **Required** | Array with the `name`s of any movement sensors on your base you want to gather feedback from. The driver will select the first movement sensor providing appropriate feedback for either the `SetVelocity()` or the `Spin()` endpoint. <br> If your sensor has an adjustable frequency or period, set the frequency to something greater than or equal to the default base control loop frequency of 10Hz, or set the period to something less than or equal to the corresponding period of 100msecs. |
| `base` | string | **Required** | String with the `name` of the base you want to wrap with sensor control. |
| `control_parameters` | object | Optional | A JSON object containing the coefficients for the proportional, integral, and derivative terms for linear and angular velocity. If you want these values to be auto-tuned, you can set all values to 0: `[ { "type": "linear_velocity", "p": 0, "i": 0, "d": 0 }, { "type": "angular_velocity", "p": 0, "i": 0, "d": 0 } ]`, and `viam-server` will auto-tune and log the calculated values. Tuning takes several seconds and spins the motors. Copy the values from the logs and add them to the configuration once tuned for the values to take effect. If you need to auto-tune multiple controlled components that depend on the same hardware, such as a sensor controlled base and one of the motors on the base, run the auto-tuning process one component at a time. For more information see [Feedback control](#feedback-control). |

## Feedback control

### SetVelocity

{{< readfile "/static/include/components/base-sensor.md" >}}

### Spin

When the `control_parameters` attribute is set, `Spin` implements a form of feedback control that polls the provided movement sensor and corrects any error between the desired angular velocity and the actual angular velocity using a PID control loop. `Spin` also monitors the angular distance traveled and stops the base when the goal angle is reached.

### MoveStraight

When `control_parameters` is set, `MoveStraight` calculates the required velocity to reach the desired velocity and distance. It then polls the provided velocity movement sensor and corrects any error between this calculated velocity and the actual velocity using a PID control loop. `MoveStraight` also monitors the position and stops the base when the goal distance is reached. If a compass heading movement sensor is provided, `MoveStraight` will attempt to keep the heading of the base fixed in the original direction it was faced at the beginning of the `MoveStraight` call.

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

The following base control API methods are available on a `sensor-controlled` base:

- [SetVelocity()](/components/base/#setvelocity): available if base is configured to receive angular and linear velocity feedback.
- [Spin()](/components/base/#spin): available if base is configured to receive orientation feedback.
- [MoveStraight()](/components/base/#movestraight): available if base is configured to receive position feedback.

For example, a [Viam Rover](/get-started/try-viam/rover-resources/) using `sensor-controlled` base following both an [angular](/components/base/#spin) and [linear](/components/base/#movestraight) velocity command:

{{<gif webm_src="/components/encoded-motor/base_moving.webm" mp4_src="/components/encoded-motor/base-moving.mp4" alt="A Viam rover turning in a half circle" max-width="400px" >}}

The position, orientation, and linear and angular velocity of the rover changing as it moves, as measured by a [movement sensor](/components/movement-sensor/):

{{<gif webm_src="/components/encoded-motor/controls_change.webm" mp4_src="/components/encoded-motor/controls_change.mp4" alt="The control tab of a movement sensor on a base with encoded motors as it turns">}}
