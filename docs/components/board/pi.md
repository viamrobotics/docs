---
title: "Configure a Raspberry Pi 4, 3, or Zero 2 W Board"
linkTitle: "pi"
weight: 20
type: "docs"
description: "Configure a Raspberry Pi 4, 3, or Zero 2 W board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/pi/"
component_description: "Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero 2 W."
usage: 999999
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/installation/prepare/rpi-setup/) to prepare your Pi for running `viam-server` before configuring a `pi` board.

{{% /alert %}}

Configure a `pi` board to integrate a [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/), or [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) into your machine.

To configure a Raspberry Pi 5, see [Configure a Raspberry Pi 5 board](/components/board/pi5/).

{{< tabs name="Configure a pi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `pi` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/components/board/pi-ui-config.png)

Edit the attributes as applicable to your board, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-pi-board-name>",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "analogs": [
          {
            "name": "<your-analog-reader-name>",
            "pin": "<pin-number-on-adc>",
            "spi_bus": "<your-spi-bus-index>",
            "chip_select": "<chip-select-index>",
            "average_over_ms": <int>,
            "samples_per_sec": <int>
          }
        ],
        "digital_interrupts": [
          {
            "name": "<your-digital-interrupt-name>",
            "pin": "<pin-number>"
          }
        ]
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi` boards:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |

## Attribute configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

[Interrupts](https://en.wikipedia.org/wiki/Interrupt) are a method of signaling precise state changes.
Configuring digital interrupts to monitor GPIO pins on your board is useful when your application needs to know precisely when there is a change in GPIO value between high and low.

- When an interrupt configured on your board processes a change in the state of the GPIO pin it is configured to monitor, it ticks to record the state change.
  You can stream these ticks with the board API's [`StreamTicks()`](/appendix/apis/components/board/#streamticks), or get the current value of the digital interrupt with [`Value()`](/appendix/apis/components/board/#value).
- Calling [`GetGPIO()`](/appendix/apis/components/board/#getgpio) on a GPIO pin, which you can do without configuring interrupts, is useful when you want to know a pin's value at specific points in your program, but is less precise and convenient than using an interrupt.

Integrate `digital_interrupts` into your machine in the `attributes` of your board by following the **Config Builder** instructions, or by adding the following to your board's JSON configuration:

{{< tabs name="Configure a Digital Interrupt" >}}
{{% tab name="Config Builder" %}}

On your board's panel, click **Show more**, then select **Add digital interrupt**.
Assign a name to your digital interrupt and then enter a pin number.

![An example configuration for digital interrupts in the Viam app Config Builder.](/components/board/digital-interrupts-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"digital_interrupts": [
  {
    "name": "<your-digital-interrupt-name>",
    "pin": "<pin-number>"
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "pi",
      "name": "your-board",
      "type": "board",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "your-interrupt-1",
            "pin": "15"
          },
          {
            "name": "your-interrupt-2",
            "pin": "16"
          }
        ]
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `digital_interrupts`:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
|`name` | string | **Required** | Your name for the digital interrupt. |
|`pin`| string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the board's GPIO pin that you wish to configure the digital interrupt for. |
|`type`| string | Optional | <ul><li>`basic`: Recommended. Tracks interrupt count. </li> <li>`servo`: For interrupts configured for a pin controlling a [servo](/components/servo/). Tracks pulse width value. </li></ul> |

#### Test `digital_interrupts`

{{< readfile "/static/include/components/board/test-board-digital-interrupts.md" >}}

## Next steps

To get started using your board, see the [board API](/appendix/apis/components/board/).
For more configuration and development info, see

{{< cards >}}
{{% card link="/appendix/apis/components/board/" customTitle="Board API" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/tutorials/get-started/blink-an-led/" noimage="true" %}}
{{< /cards >}}
