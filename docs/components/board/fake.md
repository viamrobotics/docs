---
title: "Configure a fake board"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Configure a fake board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

Configure a `fake` board to test integrating a board into your robot without physical hardware:

{{< tabs name="Configure an fake Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `fake` model.

Click **Create component**.

{{< imgproc src="/components/board/fake-ui-config.png" alt="An example configuration for a fake board in the Viam app Config Builder." resize="1000x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "your-fake-board",
      "type": "board",
      "model": "fake",
      "attributes": {
        "fail_new": false
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `fail_new` | bool | **Required** | If the fake board should raise an error at robot start-up. |
<!-- | `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See [configuration info](/components/board/#analogreader). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See [configuration info](/components/board/#digital-interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See [configuration info](/components/board/#spi-buses). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I2C) bus pins' index and name. See [configuration info](/components/board/#i2cs). | -->
