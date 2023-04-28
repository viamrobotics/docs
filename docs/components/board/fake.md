---
title: "Configure a fake board"
linkTitle: "fake"
weight: 80
type: "docs"
description: "Configure a fake board."
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

Configure a `fake` board to test integrating a board into your robot without physical hardware:

{{< tabs name="Configure an fake Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `fake` model.

![An example configuration for a fake board in the Viam app Config Builder.](../img/fake-ui-config.png)

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
<!-- | `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See configuration info [here](/components/board/#analogreader). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See configuration info [here](/components/board/#digital-interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See configuration info [here](/components/board/#spi-buses). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I2C) bus pins' index and name. See configuration info [here](/components/board/#i2cs). | -->
