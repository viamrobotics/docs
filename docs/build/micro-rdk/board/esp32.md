---
title: "Configure an ESP32 Board (Micro-RDK)"
linkTitle: "esp32"
weight: 20
type: "docs"
description: "Configure an esp32 board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - /micro-rdk/board/esp32/
# SMEs: Gautham, Nico, Andrew
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow the [setup guide](/get-started/installation/microcontrollers/) to prepare your ESP32 for running the micro-RDK before configuring an `esp32` board.

Viam recommends purchasing the ESP32 with a development board. The following ESP32 microcontrollers are supported:

- ESP32-WROOM Series (until v0.1.7)
- ESP-32-WROVER Series

Your microcontroller should have at least the following resources available to work with the micro-RDK:

- 2 Cores + 384kB SRAM + 2MB PSRAM + 4MB Flash

{{% /alert %}}

To add an `esp32` board, navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com) and select **JSON** mode.

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
    ],
    "digital_interrupts" : [
        {
         "pin": <int>
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
    ],
    "digital_interrupts": [
      {
        "pin": 4
      }
    ]
  },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable.
Click the **Save** button in the top right corner of the page.

The following attributes are available for `esp32` boards:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](#i2cs). |
| `digital_interrupts` | object | Optional | Any digital interrupts' GPIO number. See [configuration info](#digital_interrupts). |
| `pins` | object | Required | The GPIO number of any GPIO pins you wish to use as input/output with the [`GPIOPin` API](/appendix/apis/#gpio-pins). |

Any pin not specified in either `"pins"` or `"digital_interrupts"` cannot be interacted with through the [board API](/components/board/#api).
Interaction with digital interrupts is only supported with the [board API](/components/board/#api); these digital interrupts cannot be used as software interrupts in driver implementations.

### `analogs`

The following properties are available for `analogs`:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | Your name for the analog reader. |
| `pin`| integer | **Required** | The GPIO number of the ADC's connection pin, wired to the board. |

### `i2cs`

The following properties are available for `i2cs`:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
|`pin`| integer | **Required** | The GPIO number of the board's GPIO pin that you wish to configure the digital interrupt for. |

### PWM signals on `esp32` pins

You can set PWM frequencies with Viam through the [`GPIOPin` API](/build/micro-rdk/board/#api).
Refer to the [Espressif documentation for valid frequencies and duty resolutions](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/peripherals/ledc.html?#supported-range-of-frequency-and-duty-resolutions).
A configured `esp32` board can support a maximum of four different PWM frequencies simultaneously, as the boards only have four available timers.

For example:

| Pin | PWM Frequency (Hz) |
| --- | ------------------ |
| 12  | 2000               |
| 25  | 3000               |
| 26  | 5000               |
| 32  | 6000               |

At this point, if you want to add another PWM signal, you must do the following:

1. Set the PWM frequency before the duty cycle.
2. Set the PWM frequency to one of the above previously set frequencies.

For example, you can set pin 33 to 2000 Hz:

| Pin    | PWM Frequency (Hz) |
| ------ | ------------------ |
| 12, 33 | 2000               |
| 25     | 3000               |
| 26     | 5000               |
| 32     | 6000               |

Then, follow these requirements to change the PWM frequencies of a pin:

1. If no other pins have a signal of the same frequency (for example, pins 25, 26, and 32), you can freely change their PWM frequency.
2. If one or more pins are sharing the old frequency (for example, pins 12 and 33):
   1. If there are less than 4 active frequencies, you can change the PWM frequency freely because there will be a timer available.
   2. If there are already 4 active frequencies, changing the PWM frequency of the pin will raise an error because there are no timers available. Free a timer by setting the PWM frequencies of all of the pins to 0.
