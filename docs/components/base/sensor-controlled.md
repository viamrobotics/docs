---
title: "Configure a Sensor-Controlled Base"
linkTitle: "sensor-controlled"
weight: 30
type: "docs"
description: "Configure a sensor-controlled base."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/sensor-controlled/"
# SMEs: Rand H., Martha J.
---

A `sensor-controlled` base supports a wheeled robotic base with feedback control from a movement sensor.

{{% alert title="Requirements" color="note" %}}
1 or more [movement sensors](/components/movement-sensor) providing:

- Linear and angular velocity feedback, used by the bases' [SetVelocity()](/components/base/#setvelocity) endpoint
- Orientation feedback, used by the bases' [Spin()](/components/base/#spin) endpoint
{{% /alert %}}

To configure a `sensor-controlled` base as a component of your machine, first configure the base and required [movement sensor(s)](/components/movement-sensor/).
To see what models of movement sensor report which feedback, reference the appropriate column in [Movement Sensor API](/components/movement-sensor/#api).

Configure a `sensor-controlled` base as follows:

{{< tabs name="Configure a Sensor-Controlled Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `sensor-controlled` model.
Enter a name for your base and click **Create**.

{{< imgproc src="/components/base/sensor-controlled-base-ui-config.png" alt="An example configuration for a sensor-controlled base in the Viam app config builder" resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `sensor-controlled` bases:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `left` | array | **Required** | Array with the `name` of any drive motors on the left side of the base. |
| `right` | array | **Required** | Array with the `name` of any drive motors on the right side of the base. |
| `wheel_circumference_mm` | int | **Required** | The outermost circumference of the drive wheels in millimeters. Used for odometry. Can be an approximation. |
| `width_mm` | int | **Required** | Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels. Can be an approximation. |
| `spin_slip_factor` | float | Optional | Can be used in steering calculations to correct for slippage between the wheels and the floor. If utilized, calibrated by the user. |

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}
