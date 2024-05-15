---
title: "Configure an orangepi Board"
linkTitle: "orangepi"
weight: 70
type: "docs"
description: "Configure an Orange Pi board."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "orangepi"]
# SMEs: Olivia Miller
---

Configure an `orangepi` board to integrate an [Orange Pi Zero2](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-Zero-2.html) or [OrangePi 3 LTS](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/orange-pi-3-LTS.html) into your machine.

If you have an Orange Pi Zero2, follow [this guide to flash your board](/get-started/installation/prepare/orange-pi-zero2/).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} to install `viam-server` on your board and connect to the Viam app.

Then, configure your board as a {{< glossary_tooltip term_id="component" text="component" >}} of your machine in [the Viam app](https://app.viam.com):

{{< tabs name="Configure an orangepi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `orangepi` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example configuration for a orangepi board in the Viam app Config Builder.](/machine/components/board/orangepi-ui-config.png)

Edit the attributes as applicable to your board, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-orangepi-board>",
      "model": "orangepi",
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
      }
      ,
      "depends_on": []
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
      "name": "<your-orangepi-board>",
      "model": "orangepi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "your-interrupt",
            "pin": "18"
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

The following attributes are available for `orangepi` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/machine/components/board/#digital_interrupts). |

## Attribute configuration

Configure these attributes on your board to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
