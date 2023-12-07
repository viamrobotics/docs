---
title: "Configure a Raspberry Pi 4, 3, or Zero 2 board"
linkTitle: "pi"
weight: 20
type: "docs"
description: "Configure a Raspberry Pi 4, 3, or Zero 2 board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/pi/"
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/get-started/installation/prepare/rpi-setup/) to prepare your Pi for running `viam-server` before configuring a `pi` board.

{{% /alert %}}

Configure a `pi` board to integrate a [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/), or [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) into your robot.

To configure a Raspberry Pi 5, see [Configure a Raspberry Pi 5 board](/components/board/pi5/).

{{< tabs name="Configure a pi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `pi` model.
Enter a name for your board and click **Create**.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/tutorials/scuttlebot/board-empty-json.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "analogs": [
    {
      "chip_select": "<chip-select-pin-number-on-board>",
      "name": "<your-analog-reader-name>",
      "pin": "<pin-number-on-adc>",
      "spi_bus": "<your-spi-bus-name>",
      "average_over_ms": <int>,
      "samples_per_sec": <int>
    }
  ],
  "digital_interrupts": [
    {
      "name": "<your-digital-interrupt-name>",
      "pin": "<pin-number>",
      "type": "<basic|servo>"
    }
  ],
  "spis": [
    {
      "name": "<your-bus-name>",
      "bus_select": "<your-bus-index>"
    }
  ],
  "i2cs": [
    {
      "name": "<your-bus-name>",
      "bus": "<your-bus-index>"
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
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "analogs": [
          <...See table below...>
        ],
        "digital_interrupts": [
          <...See table below...>
        ],
        "spis": [
          <...See table below...>
        ],
        "i2cs": [
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

The following attributes are available for `pi` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See [configuration info](#spis). Review [these instructions](/get-started/installation/prepare/rpi-setup/#enable-communication-protocols) to learn how to enable SPI on a Raspberry Pi 4. |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](#i2cs). Review [these instructions](/get-started/installation/prepare/rpi-setup/#enable-communication-protocols) to learn how to enable I<sup>2</sup>C on a Raspberry Pi 4. |

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs), [digital interrupts](#digital_interrupts), and components that must communicate through the [SPI](#spis) and [I<sup>2</sup>C](#i2cs) protocols into your robot.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `spis`

{{< readfile "/static/include/components/board/board-spis.md" >}}

### `i2cs`

{{< readfile "/static/include/components/board/board-i2cs.md" >}}
