---
title: "Configure an ESP32 board"
linkTitle: "esp32"
weight: 20
type: "docs"
description: "Configure an esp32 board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow the [setup guide](/installation/prepare/microcontrollers/) to prepare your ESP32 for running the micro-RDK before configuring an `esp32` board.

Viam recommends purchasing the ESP32 with a development board. The following ESP32 microcontrollers are supported:

- ESP32-WROOM Series
- ESP-32-WROVER Series

Your microcontroller should have the following resources available to work with the micro-RDK:

- 2 Cores + 384kB SRAM + 4MB Flash

{{% /alert %}}

To add an `esp32` board, navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com) and select **Raw JSON** mode.

{{< alert title="Info" color="info" >}}

The`esp32` [board](/components/board/) model is not currently available as a built-in option in [the Viam app](https://app.viam.com), so you cannot use **Builder** mode to configure this board.

{{< /alert >}}

Copy the following JSON template and paste it into your configuration inside the `"components"` array:

{{< tabs name="Configure an esp32 Board" >}}
{{% tab name="JSON Template"%}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-board-name>",
  "model": "esp32",
  "type": "board",
  "namespace": "rdk",
  "attributes": {
    "pins": [
      <int>
    ],
    "analogs": [
      {
        "pin": <int>,
        "name": "<your-analog-name>"
      }
    ]
  },
  "depends_on": []
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "board",
  "model": "esp32",
  "type": "board",
  "namespace": "rdk",
  "attributes": {
    "pins": [15, 34],
    "analogs": [
      {
        "pin": "34",
        "name": "sensor"
      }
    ]
  },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable.
Click **Save config**.

The following attributes are available for `esp32` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](#i2cs). |
| `digital_interrupts` | object | Optional | Any digital interrupts' GPIO number. See [configuration info](#digital_interrupts). |
| `pins` | object | Required | The GPIO number of any GPIO pins you wish to use as input/output with the [`GPIOPin` API](/program/apis/#gpio-pins). |

Any pin not specified in either `"pins"` or `"digital_interrupts"` cannot be interacted with through the [board API](/components/board/#api).
Interaction with digital interrupts is only supported with the [board API](/components/board/#api); these digital interrupts cannot be used as software interrupts in driver implementations.

### `analogs`

The following properties are available for `analogs`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name` | string | **Required** | Your name for the analog reader. |
|`pin`| integer | **Required** | The GPIO number of the ADC's connection pin, wired to the board.

### `i2cs`

The following properties are available for `i2cs`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name`| string| **Required** | `name` of the I<sup>2</sup>C bus. |
|`bus`| string | **Required** | The index of the I<sup>2</sup>C bus. Must be either `i2c0` or `i2c1`. |
|`data_pin`| integer | **Required** | The GPIO number of the data pin. |
|`clock_pin`| integer | **Required** | The GPIO number of the clock pin. |
|`baudrate_hz`| integer | Optional | The baudrate in HZ of this I<sup>2</sup>C bus. <br> Default: `1000000` |
|`timeout_ns`| integer | Optional | Timeout period for this I<sup>2</sup>C bus in nanoseconds. <br> Default: `0` |

### `digital_interrupts`

The following properties are available for `digital_interrupts`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`pin`| string | **Required** | The GPIO number of the board's GPIO pin that you wish to configure the digital interrupt for. |
