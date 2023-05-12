---
title: "Configure a jetson board"
linkTitle: "jetson"
weight: 20
type: "docs"
description: "Configure a jetson board."
images: ["/components/img/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow one of our Jetson [setup guides](/installation/prepare) to prepare your board for running `viam-server` before configuring a `jetson` board.

{{% /alert %}}

Configure a `jetson` board to integrate a [NVIDIA Jetson AGX Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), or [NVIDIA Jetson  Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) into your robot:

{{< tabs name="Configure an jetson Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `jetson` model.

![An example configuration for a jetson board in the Viam app Config Builder.](../img/jetson-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-jetson-board>",
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
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See configuration info [here](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's [pin number](/appendix/glossary/#term-pin-number) and name. See configuration info [here](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See configuration info [here](/components/board/#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See configuration info [here](/components/board/#i2cs). |
