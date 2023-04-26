---
title: "Configure a ti board"
linkTitle: "ti"
weight: 20
type: "docs"
description: "Configure a ti board."
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow this [setup guide](/installation/prepare/sk-tda4vm/) to prepare your TDA4VM for running `viam-server` before configuring a `ti` board.

{{% /alert %}}

Configure a `ti` board to integrate a [Texas Instruments TDA4VM](https://devices.amazonaws.com/detail/a3G8a00000E2QErEAN/TI-TDA4VM-Starter-Kit-for-Edge-AI-vision-systems) into your robot:

{{< tabs name="Configure an ti Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `ti` model.

![An example configuration for a ti board in the Viam app Config Builder.](../img/ti-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <"your-ti-board">,
      "type": "board",
      "model": "ti",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `ti` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See configuration info [here](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's pin number and name. See configuration info [here](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select bus pins' index and name. See configuration info [here](/components/board/#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) bus pins' index and name. See configuration info [here](/components/board/#i2cs). |
