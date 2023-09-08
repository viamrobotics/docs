---
title: "Configure a beaglebone board"
linkTitle: "beaglebone"
weight: 40
type: "docs"
description: "Configure a beaglebone board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow this [setup guide](/installation/prepare/beaglebone-setup/) to prepare your BeagleBone for running `viam-server` before configuring a `beaglebone` board.

{{% /alert %}}

Configure a `beaglebone` board to integrate [BeagleBoard's BeagleBone AI 64](https://www.beagleboard.org/boards/beaglebone-ai-64) into your robot:

{{< tabs name="Configure an beaglebone Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `beaglebone` model.
Enter a name for your board and click **Create**.

![An example configuration for a beaglebone board in the Viam app Config Builder.](/components/board/beaglebone-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-beaglebone-board>",
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
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See [configuration info](/components/board/#spis). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I<sup>2</sup>C) bus pins' index and name. See [configuration info](/components/board/#i2cs). |
