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

Follow the [setup guide](/installation/prepare/microcontrollers/) to prepare your ESP32 for running micro-RDK before configuring a `esp32` board.

{{% /alert %}}

To add an `esp32` board, navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com) and select **Raw JSON** mode.

Copy the following JSON template and paste it into your configuration inside the `"components"` array:

{{< tabs name="Configure an esp32 Board" >}}
{{% tab name="JSON Template"%}}

```json {class="line-numbers linkable-line-numbers"}
{
  "attributes": {
    "pins": [
      <int>
    ],
    "analogs": [
      {
        "pin": "<number>",
        "name": "<your-analog-name>"
      }
    ]
  },
  "depends_on": [],
  "model": "esp32",
  "name": "<your-board-name>",
  "type": "board"
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "attributes": {
    "pins": [15],
    "analogs": [
      {
        "pin": "34",
        "name": "sensor"
      }
    ]
  },
  "depends_on": [],
  "model": "esp32",
  "name": "board",
  "type": "board"
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
| `pins` | object | Required | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of any GPIO pins you wish to use as input/output with the [`GPIOPin` API](/program/apis/#gpio-pins). |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](/components/board/#analogs). |

{{< alert title="Info" color="info" >}}

The`esp32` [board](/components/board/) model is not currently provided for you as a built-in option in [the Viam app](https://app.viam.com), so you cannot use the **Config Builder** to configure this board.

{{< /alert >}}

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `i2cs`

{{< readfile "/static/include/components/board/board-i2cs.md" >}}
