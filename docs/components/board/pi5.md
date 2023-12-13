---
title: "Configure a Raspberry Pi 5 Board"
linkTitle: "pi5"
weight: 20
type: "docs"
description: "Configure a Raspberry Pi 5 board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Bucket, Alan
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/get-started/installation/prepare/rpi-setup/) to prepare your Pi for running `viam-server` before configuring a `pi5` board.

{{% /alert %}}

Configure a `pi5` board to integrate a [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) into your robot.

To configure a Raspberry Pi 4 or earlier, see [Configure a Raspberry Pi 4, 3, or Zero 2 W board](/components/board/pi/).

### Enable hardware PWM

_(Optional)_ If you want to use hardware PWM on {{< glossary_tooltip term_id="pin-number" text="pins" >}} 12 and 35, edit <file>/boot/config.txt</file> on your Pi, adding the following line:

```sh {class="line-numbers linkable-line-numbers"}
dtoverlay=pwm-2chan
```

Then reboot the Pi for the change to take effect.

If you do not enable hardware PWM, these pins will have no function.

### Configuration

{{< tabs name="Configure a pi5 Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `pi5` model.
Enter a name for your board and click **Create**.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi5) are shown. No other attributes are configured.](/components/board/pi5-ui-config.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "analogs": [
    {
      "name": "<your-analog-reader-name>",
      "pin": "<pin-number-on-adc>",
      "spi_bus": "<your-spi-bus-index>",
      "chip_select": "<chip-select-pin-number-on-board>",
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
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
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
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-pi-board-name>",
      "model": "pi5",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "analogs": [
          <...See table below...>
        ],
        "digital_interrupts": [
          <...See table below...>
        ]
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi5` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your robot.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
