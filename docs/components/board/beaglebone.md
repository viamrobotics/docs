---
title: "Configure a beaglebone board"
linkTitle: "beaglebone"
weight: 20
type: "docs"
description: "Configure a beaglebone board."
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow this [setup guide](/installation/prepare/beaglebone-setup/) to prepare your BeagleBone for running `viam-server` before configuring a `beaglebone` board.

{{% /alert %}}

Configure a `beaglebone` board to integrate [BeagleBoard's BeagleBone AI 64](https://beagleboard.org/ai-64) into your robot:

{{< tabs name="Configure an beaglebone Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `beaglebone` model.

![An example configuration for a beaglebone board in the Viam app Config Builder.](../img/beaglebone-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <"your-beaglebone-board">,
      "type": "board",
      "model": "beaglebone",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `beaglebone` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See configuration info [here](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's pin number and name. See configuration info [here](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See configuration info [here](/components/board/#spis). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I<sup>2</sup>C) bus pins' index and name. See configuration info [here](/components/board/#i2cs). |
