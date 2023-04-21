---
title: "Configure a jetson board"
linkTitle: "jetson"
weight: 20
type: "docs"
description: "Configure a jetson board."
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow one of our Jetson [setup guides](/installation/prepare) to prepare your board for running `viam-server` before configuring a `jetson` board.

{{% /alert %}}

Configure a `jetson` board to integrate a [NVIDIA Jetson AGX Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), or [NVIDIA Jetson  Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) into your robot:

{{< tabs name="Configure an jetson Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `jetson` model.

![An example configuration for a jetson board in the Viam app Config Builder.](../img/jetson-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <"your-jetson-board">,
      "type": "board",
      "model": "jetson",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `jetson` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See configuration info [here](/components/board/#analogreader). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See configuration info [here](/components/board/#digital-interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See configuration info [here](/components/board/#spi-buses). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I2C) bus pins' index and name. See configuration info [here](/components/board/#i2cs). |
