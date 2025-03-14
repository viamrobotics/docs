---
title: "Configure a Raspberry Pi 5 Board"
linkTitle: "pi5"
weight: 20
type: "docs"
description: "Configure a Raspberry Pi 5 board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
component_description: "Supports Raspberry Pi 5."
usage: 999999
aliases:
  - /components/board/pi5/
# SMEs: Bucket, Alan
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/operate/reference/prepare/rpi-setup/) to prepare your Pi for running `viam-server` before configuring a `pi5` board.

{{% /alert %}}

Configure a `pi5` board to integrate a [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) into your machine.

To configure a Raspberry Pi 4 or earlier, see [`viam:raspberry-pi:rpi`](https://github.com/viam-modules/raspberry-pi).

### Enable hardware PWM

_(Optional)_ If you want to use hardware PWM on {{< glossary_tooltip term_id="pin-number" text="pins" >}} 12 (GPIO 18) and 35 (GPIO 19), edit <file>/boot/firmware/config.txt</file> on your Pi, adding the following line:

```sh {class="line-numbers linkable-line-numbers"}
dtoverlay=pwm-2chan
```

Then reboot the Pi for the change to take effect.

If you do not enable hardware PWM, these pins will have no function.

### Configuration

To test your board as you configure it, power it on.
If you plan to connect hardware to the board's pins, connect the hardware while it's powered off.
Then, configure the board:

{{< tabs name="Configure a pi5 Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `pi5` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi5) are shown. No other attributes are configured.](/components/board/pi5-ui-config.png)

Edit the attributes as applicable to your board, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-pi-board-name>",
      "model": "pi5",
      "api": "rdk:component:board",
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
        ],
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi5` boards:

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

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/board.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/board/" customTitle="Board API" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/tutorials/get-started/blink-an-led/" noimage="true" %}}
{{< /cards >}}
