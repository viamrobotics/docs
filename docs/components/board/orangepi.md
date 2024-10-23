---
title: "Configure an orangepi Board"
linkTitle: "orangepi"
weight: 70
type: "docs"
description: "Configure an Orange Pi board."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "orangepi"]
component_description: "Supports Orange Pi Zero2, Orange Pi Zero 2W or OrangePi 3 LTS."
# SMEs: Olivia Miller, Steve Briskin
---

Configure an `orangepi` board to integrate the GPIO pins of an [Orange Pi Zero2](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-Zero-2.html), [Orange Pi Zero 2W](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-Zero-2W.html) or [OrangePi 3 LTS](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/orange-pi-3-LTS.html) into your machine.

First, follow the installation guide for your specific Orange Pi board:

- For an Orange Pi Zero2: follow the [Orange Pi Zero2 installation guide](/installation/prepare/orange-pi-zero2/).
- For an Orange Pi 3 LTS, follow the [Orange Pi 3 LTS installation guide](/installation/prepare/orange-pi-3-lts/).

{{% alert title="Note" color="note" %}}
There is no setup guide available for the Orange Pi Zero 2W.
If you have one of these boards, you can image it with [an Ubuntu image](https://drive.google.com/drive/folders/1g806xyPnVFyM8Dz_6wAWeoTzaDg3PH4Z) to prepare it for running `viam-server`.
{{% /alert %}}

Once you have prepared your board, add a new machine in the [Viam app](https://app.viam.com) and follow your new machine part's {{< glossary_tooltip term_id="setup" text="setup instructions" >}} to install `viam-server` on your board and connect to the Viam app.

To use the GPIO pins on your board to [configure a smart machine](/configure/) with your Orange Pi computer, configure your board as a {{< glossary_tooltip term_id="component" text="component" >}} of your machine in the [Viam app](https://app.viam.com):

{{< tabs name="Configure an orangepi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `orangepi` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example configuration for a orangepi board in the Viam app Config Builder.](/components/board/orangepi-ui-config.png)

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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |

## Attribute configuration

Configure these attributes on your board to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/board.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/board/" customTitle="Board API" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/tutorials/get-started/blink-an-led/" noimage="true" %}}
{{< /cards >}}
