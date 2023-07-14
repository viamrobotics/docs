---
title: "Configure a jetson board"
linkTitle: "jetson"
weight: 20
type: "docs"
description: "Configure a jetson board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow one of our Jetson [setup guides](/installation/) to prepare your board for running `viam-server` before configuring a `jetson` board.

{{% /alert %}}

Configure a `jetson` board to integrate a [NVIDIA Jetson Orin Module and Developer Kit](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), or [NVIDIA Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) into your robot:

{{< tabs name="Configure an jetson Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, select the type `board`, and select the `jetson` model.

Click **Create component**.

{{< imgproc src="/components/board/jetson-ui-config.png" alt="An example configuration for a jetson board in the Viam app Config Builder." resize="1000x" >}}

Edit and fill in the attributes as applicable.

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
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See [configuration info](/components/board/#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](/components/board/#i2cs). |
