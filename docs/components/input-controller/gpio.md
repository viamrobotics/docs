---
title: "Configure a GPIO/ADC-Based Input Controller"
linkTitle: "gpio"
weight: 30
type: "docs"
description: "Configure a GPIO- or ADC-based device as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/gpio/"
# SMEs: James
---

Configure a `gpio` input controller to use a GPIO- or ADC-based device to communicate with your machine.

{{< tabs name="Configure a `gpio` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `input_controller` type, then select the `gpio` model.
Enter a name for your input controller and click **Create**.

![An example configuration for a GPIO input controller component in the Viam App config builder](/components/input-controller/gpio-input-controller-ui-config.png)

Copy and paste the following attribute template into your input controller's **Attributes** box.
Then remove and fill in the attributes as applicable to your input controller, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "<your-board-name>",
  "buttons": {
    "<your-button-name>": {
      "control": "<button-control-name>",
      "invert": <boolean>,
      "debounce_msec": <int>
    }
  },
  "axes": {
    "<your-axis-name>": {
      "control": "<axis-control-name>",
      "min": <int>,
      "max": <int>,
      "poll_hz": <int>,
      "deadzone": <int>,
      "min_change": <int>,
      "bidirectional": <boolean>,
      "invert": <boolean>
    }
  },
  "depends_on": ["<your-board-name>"]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "piboard",
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
  },
  "depends_on": ["piboard"]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-gpio-input-controller-name>",
      "model": "gpio",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {
        "board": "<your-board-name>",
        "buttons": {
          "<your-button-name>": {
            "control": "<button-control-name>",
            "invert": <boolean>,
            "debounce_msec": <int>
          }
        },
        "axes": {
          "<your-axis-name>": {
            "control": "<axis-control-name>",
            "min": <int>,
            "max": <int>,
            "poll_hz": <int>,
            "deadzone": <int>,
            "min_change": <int>,
            "bidirectional": <boolean>,
            "invert": <boolean>
          }
        }
      },
      "depends_on": ["<your-board-name>"]
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
      "name": "my_gpio_ic",
      "model": "gpio",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {
        "board": "piboard",
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
      "depends_on": ["piboard"]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gpio` input controllers:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required**| The name of the board component with GPIO or ADC pins to use as the controlling device. |
| `buttons` | object | **Required** | The [Buttons](../#button-controls) available for control. These should be connected to the GPIO/ADC board. <br><br> <b>Each button has the following fields:</b> <br><ul><li><code>name</code>: Name of the Digital Interrupt the button/switch is connected to, as configured on the board component.</li><li><code>control</code>: The [Control](../#control-field) type to use when reporting events as this button's state is changed.</li><li><code>invert</code>: Boolean indicating if the digital input (high/low) should be inverted when reporting button Control value indicating button state.<br> This option is given because digital switches vary between high, `1`, and low, `0`, as their default at rest.<ul><li>*true:* `0` is pressed, and `1` is released.</li><li>*false (default):* `0` is released, and `1` is pressed.</li></ul></li><li><code>debounce_ms</code>: How many milliseconds to wait for the interrupt to settle. This is needed because some switches can be electrically noisy.</li></ul> |
| `axes` | object | **Required** | The [Axes](../#axis-controls) available for control. These should be connected to the GPIO/ADC board.<br><br>**Each axis has the following fields:**<ul><li><code>name</code>: Name of the Analog Reader that reports ADC values for the axis Control, as configured on the board component.</li><li><code>control</code>: The [Control](../#control-field) type to use when reporting events as this axis's position is changed.</li><li><code>min</code>: The minimum ADC value that the analog reader can report as this axis's position changes. </li><li><code>max</code>: The maximum ADC value that the analog reader can report as this axis's position changes.</li><li><code>deadzone</code>: The absolute ADC value change from the neutral `0` point to still consider as a neutral position. This option is given so tiny wiggles on loose controls don't result in events being reported.</li><li><code>min_change</code>: The minimum absolute ADC value change from the previous ADC value reading that can occur before reporting a new [`PositionChangeAbs Event`](../#event-object). This option is given so tiny wiggles on loose controls don't result in events being reported.</li><li><code>bidirectional</code>: Boolean indicating if the axis changes position in 1 direction, like on an analog trigger or pedal, or 2, like on an analog control stick.<ul><li>*true:* The axis should report center, `0`, as halfway between the min/max ADC values.</li><li>*false:* `0` is still the neutral point of the axis, but only positive change values can be reported.</li></ul></li><li><code>poll_hz</code>: How many times per second to check for a new ADC reading that can generate an event.</li><li><code>invert</code>: Boolean indicating if the direction of the axis should be flipped when translating ADC value readings to the axis Control value indicating position change.<ul><li>*true:* flips the direction of the axis so that the minimum ADC value is reported as the maximum axis Control value.</li><li>*false:* keeps the direction of the axis the same, so that the minimum ADC value is reported as the minimum axis Control value.</li></ul></li></ul> |

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
