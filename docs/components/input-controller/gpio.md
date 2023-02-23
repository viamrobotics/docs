---
title: "Configure a GPIO/ADC based input controller"
linkTitle: "gpio"
weight: 30
type: "docs"
description: "Configure a GPIO or ADC based device as an input controller."
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `gpio` input controller allows you to use a GPIO or ADC based device to communicate with your robot.

## Configuration

Refer to the following example configuration for an input controller of model `gpio` with a GPIO based board device:

{{< tabs name="Configure a `gpio` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gpio-input-controller-ui-config.png" alt="Example of what configuration for a GPIO based device input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "components": [
    {
      "name": "gpio-input-controller",
      "type": "input_controller",
      "model": "gpio",
      "attributes": {
        "board": <your-GPIO-board>,
        "buttons": {
          "interrupt1": {
            "control": "ButtonNorth",
            "invert": false,
            "debounce_msec": 5
          },
          "interrupt2": {
            "control": "ButtonSouth",
            "invert": true,
            "debounce_msec": 5
          }
        },
        "axes": {
          "analogReader1": {
            "control": "AbsoluteX",
            "min": 0,
            "max": 1023,
            "poll_hz": 50,
            "deadzone": 30,
            "min_change": 5,
            "bidirectional": false,
            "invert": false
          },
          "analogReader2": {
            "control": "AbsoluteY",
            "min": 0,
            "max": 1023,
            "poll_hz": 50,
            "deadzone": 30,
            "min_change": 5,
            "bidirectional": true,
            "invert": true
          }
        }
      },
      "depends_on": [
        <your-GPIO-board>
      ]
    }, ...
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gamepad` input controllers:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `board` | *Required* | The name of the board component with GPIO or ADC pins to use as the controlling device. |
| `buttons` | *Required* | The [Buttons](../#buttons) available for control. These should be physically attached to the GPIO/ADC board. |
| `axes` | *Required* | The [Axes](../#axes) available for control. These should be physically attached to the GPIO/ADC board. |

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
