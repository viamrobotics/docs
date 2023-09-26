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

If you have a CSI camera, follow [these instructions](/extend/modular-resources/examples/csi/) to configure it using the `viam:camera:csi` model.

{{% /alert %}}

{{% alert title="CAUTION: Use 3.3V inputs and outputs" color="warning" %}}

The jetson's GPIO pins are rated for inputs and outputs at 3.3V. Signals from encoders and sensors at even 5V can cause damage to a pin. We recommend connecting hardware that can operate and send signals at 3.3V or lower. For details, see pages 1-3 of the [Jetson Nano Developer Kit 40-Pin Expansion Header GPIO Usage Considerations Applications Note](https://developer.nvidia.com/jetson-nano-developer-kit-40-pin-expansion-header-gpio-usage-considerations-applications-note)

{{% /alert %}}

Configure a `jetson` board to integrate a [NVIDIA Jetson Orin Module and Developer Kit](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson AGX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), or [NVIDIA Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) into your robot:

{{< tabs name="Configure an jetson Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `jetson` model.
Enter a name for your board and click **Create**.

![An example configuration for a jetson board in the Viam app Config Builder.](/components/board/jetson-ui-config.png)

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

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See [configuration info](/components/board/#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](/components/board/#i2cs). |
