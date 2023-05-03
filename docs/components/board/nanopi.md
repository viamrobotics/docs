---
title: "Configure a nanopi board"
linkTitle: "nanopi"
weight: 20
type: "docs"
description: "Configure a nanopi board."
images: ["/components/img/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

Configure a `nanopi` board to integrate [FriendlyElec’s NanoPi Mini Board](https://www.friendlyelec.com/index.php?route=product/category&path=69) into your robot:

{{< tabs name="Configure an nanopi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `nanopi` model.

Click **Create component**.

![An example configuration for a nanopi board in the Viam app Config Builder.](../img/nanopi-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-nanopi-board>",
      "type": "board",
      "model": "nanopi",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `nanopi` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See configuration info [here](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's [pin number](/appendix/glossary/#term-pin-number) and name. See configuration info [here](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See configuration info [here](/components/board/#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See configuration info [here](/components/board/#i2cs). |
