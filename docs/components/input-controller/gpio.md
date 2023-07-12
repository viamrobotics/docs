---
title: "Configure a GPIO/ADC based input controller"
linkTitle: "gpio"
weight: 30
type: "docs"
description: "Configure a GPIO or ADC based device as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `gpio` input controller allows you to use a GPIO or ADC based device to communicate with your robot.

## Configuration

Refer to the following example configuration for an input controller of model `gpio` with a GPIO based device serving as the board component.

Be aware that complete configuration is not visible in the "Config Builder" tab:

{{< tabs name="Configure a `gpio` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your input controller, select the type `input_controller`, and select the `gpio` model.

Click **Create component**.

![An example configuration for a GPIO input controller component in the Viam App config builder](../img/gpio-input-controller-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
    {
      "name": "<your-gpio-input-controller-name>",
      "type": "input_controller",
      "model": "gpio",
      "attributes": {
        "board": "<your-board-name>",
        "buttons": {
          "<your-button-name>": {
            "control": "<button-control-name>",
            "invert": <boolean>,
            "debounce_msec": <#>
          }
        },
        "axes": {
          "<nyour-axis-name>": {
            "control": "<axis-control-name>",
            "min": <#>,
            "max": <#>,
            "poll_hz": <#>,
            "deadzone": <#>,
            "min_change": <#>,
            "bidirectional": <boolean>,
            "invert": <boolean>
          }
        }
      },
      "depends_on": [
        "<your-board-name>"
      ]
    }, ... // <INSERT ANY ADDITIONAL COMPONENT CONFIGURATION>
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
    {
      "name": "my_gpio_ic",
      "type": "input_controller",
      "model": "gpio",
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
      "depends_on": [
        "piboard"
      ]
    }, ...
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gpio` input controllers:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required**| The name of the board component with GPIO or ADC pins to use as the controlling device. |
| `buttons` | object | **Required** | The [Buttons](../#button-controls) available for control. These should be connected to the GPIO/ADC board. <pre> **Each buttons's fields:** <br><br> <code>name</code>: Name of the Digital Interrupt the button/switch is connected to, as configured on the board component. <br><br> <code>control</code>: The [Control](../#control-field) type to use when reporting events as this button's state is changed. <br><br> <code>invert</code>: Boolean indicating if the digital input (high/low) should be inverted when reporting button Control value indicating button state. <br> This option is given because digital switches vary between high, `1`, and low, `0`, as their default at rest. <pre> *true:* `0` is pressed, and `1` is released. <br> *false (default):* `0` is released, and `1` is pressed. </pre> <code>debounce_ms</code>: How many milliseconds to wait for the interrupt to settle. This is needed because some switches can be electrically noisy. </pre> |
| `axes` | object | **Required** | The [Axes](../#axis-controls) available for control. These should be connected to the GPIO/ADC board. <pre> **Each axis's fields:** <br><br> <code>name</code>: Name of the Analog Reader that reports ADC values for the axis Control, as configured on the board component. <br><br> <code>control</code>: The [Control](../#control-field) type to use when reporting events as this axis's position is changed. <br><br> <code>min</code>: The minimum ADC value that the analog reader can report as this axis's position changes. <br><br> <code>max</code>: The maximum ADC value that the analog reader can report as this axis's position changes. <br><br> <code>deadzone</code>: The absolute ADC value change from the neutral `0` point to still consider as a neutral position. This option is given so tiny wiggles on loose controls don't result in events being reported. <br><br> <code>min_change</code>: The minimum absolute ADC value change from the previous ADC value reading that can occur before reporting a new [`PositionChangeAbs Event`](../#event-object). This option is given so tiny wiggles on loose controls don't result in events being reported. <br><br> <code>bidirectional</code>: Boolean indicating if the axis changes position in 1 direction, like on an analog trigger or pedal, or 2, like on an analog control stick. <pre> *true:* The axis should report center, `0`, as halfway between the min/max ADC values. <br> *false:* `0` is still the neutral point of the axis, but only positive change values can be reported. </pre> <code>poll_hz</code>: How many times per second to check for a new ADC reading that can generate an event. <br><br> <code>invert</code>: Boolean indicating if the direction of the axis should be flipped when translating ADC value readings to the axis Control value indicating position change. <pre> *true:* flips the direction of the axis so that the minimum ADC value is reported as the maximum axis Control value. <br> *false:* keeps the direction of the axis the same, so that the minimum ADC value is reported as the minimum axis Control value. </pre></pre>|

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
