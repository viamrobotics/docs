---
title: "Configure a pi board"
linkTitle: "pi"
weight: 20
type: "docs"
description: "Configure a pi board."
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow this [setup guide](/installation/prepare/rpi-setup/) to prepare your Pi for running `viam-server` before configuring a `pi` board.

{{% /alert %}}

Configure a `pi` board to integrate a [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) or [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) into your robot:

{{< tabs name="Configure an pi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `pi` model.

![An example configuration for a pi board in the Viam app Config Builder.](../img/pi-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "type": "board",
      "model": "pi",
      "name": <"your_name">
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See configuration info [here](/components/board/#analogreader). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See configuration info [here](/components/board/#digital-interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See configuration info [here](/components/board/#spi-buses). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I2C) bus pins' index and name. See configuration info [here](/components/board/#i2cs). |
