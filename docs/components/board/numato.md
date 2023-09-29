---
title: "Configure a numato board"
linkTitle: "numato"
weight: 50
type: "docs"
description: "Configure a numato board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

<!-- TODO: section on why configuring this one WITH another board is necessary & why the module is useful. -->

Configure a `numato` board to integrate [Numato GPIO Peripheral Modules](https://numato.com/product-category/automation/gpio-modules/) into your robot:

{{< tabs name="Configure an numato Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `numato` model.
Enter a name for your board and click **Create**.

![An example configuration for a numato board in the Viam app Config Builder.](/components/board/numato-ui-config.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pins": <int>,
  "analogs": [
    {
      "chip_select": "<chip-select-pin-number-on-board>",
      "name": "<your-analog-reader-name>",
      "pin": "<pin-number-on-adc>",
      "spi_bus": "<your-spi-bus-name>",
      "average_over_ms": <int>,
      "samples_per_sec": <int>
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pins": 32
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
      "name": "<your-numato-board>",
      "type": "board",
      "model": "numato",
      "attributes": {
        "pins": <number>,
        "analogs": [
          {
            "name": "<your-analog>",
            "pin": "<number>",
            "spi_bus": "<your-spi-bus-name>",
            "chip_select": "<number>"
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

The following attributes are available for `numato` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pins` | int | **Required** | Number of GPIO pins available on the module. |
| `analogs` | object | Optional | Attributes of any pins that can be used as inputs for the module's internal analog-to-digital converter (ADC). See [configuration info](/components/board/#analogs). |

<!-- I think these are available but I need to confirm
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See [configuration info](/components/board/#digital-interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select bus pins' index and name. See [configuration info](/components/board/#spi-buses). |
| `i2cs` | object | Optional | Any Inter Integrated Circuit (I2C) bus pins' index and name. See [configuration info](/components/board/#i2cs). | -->
