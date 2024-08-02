---
title: "Configure a <board-model> Board"
linkTitle: "<board-model>"
weight: 20
type: "docs"
description: "Configure a <board-model> board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/<board-model>/"
draft: true
# SMEs:
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/installation/prepare/board1-setup) to prepare your <model-name> to run `viam-server` before you configure your <model-name> board.

{{% /alert %}}

Configure a `<board-model>` board to integrate an [<board-series-model>](http://www.example.com), [<board-series-model-1>](http://example.com), or [<board-series-model-2>](http://example.com) board into your machine.

{{< tabs name="Configure a <board-model> Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `<board-model>` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example configuration for a <board-model> board in the Viam app Config Builder.](/components/board/pi-ui-config.png)

Click the **{}** (Switch to Advanced) button in the top right of the component panel to edit your board's attributes with JSON, according to the following table.

{{% /tab %}}
{{% tab name="JSON Template" %}}

````json {class="line-numbers linkable-line-numbers"}
{
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
}

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
 "digital_interrupts": [
          {
            "name": "your-digital-interrupt-name",
            "pin": "18"
          }
        ]
}
````

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `<board-model>` boards:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts).|
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See [configuration info](#analogs).|

## Attribute configuration

Configure these attributes on your board to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
