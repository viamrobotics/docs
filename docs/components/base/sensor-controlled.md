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
1 or more [movement sensors](/components/movement-sensor/) providing:

- Linear and angular velocity feedback, used by the base's [SetVelocity()](/components/base/#setvelocity) endpoint
- Orientation feedback, used by the base's [Spin()](/components/base/#spin) endpoint
  {{% /alert %}}

To configure a `sensor-controlled` base as a component of your machine, first configure the [model of base](/components/base/) you want to wrap with feedback control and each required [movement sensor](/components/movement-sensor/).
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
| `movement-sensor` | array | **Required** | Array with the `name` of any movement sensors on your base you want to gather feedback from. |
| `base` | string | **Required** | String with the `name` of the base you want to wrap with sensor control. |

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

The following motor control API methods are available with feedback control on a `sensor-controlled` base:

- [SetVelocity()](/components/base/#setvelocity): available if base is configured to receive angular and linear velocity feedback.
- [Spin()](/components/base/#spin): available if base is configured to receive orientation feedback.
