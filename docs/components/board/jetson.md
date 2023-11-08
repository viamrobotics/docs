---
title: "Configure a jetson board"
linkTitle: "jetson"
weight: 20
type: "docs"
description: "Configure a jetson board to integrate a NVIDIA Jetson Orin Module and Developer Kit, NVIDIA Jetson AGX, or NVIDIA Jetson Nano into your robot."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow one of our Jetson [setup guides](/installation/) to prepare your board for running `viam-server` before configuring a `jetson` board.

If you have a CSI camera, follow [these instructions](/registry/examples/csi/) to configure it using the `viam:camera:csi` model.

{{% /alert %}}

{{% alert title="CAUTION: Use 3.3V inputs and outputs" color="caution" %}}

The GPIO pins on Jetson boards are rated 3.3V signals. 5V signals from encoders and sensors can cause damage to a pin. We recommend selecting hardware that can operate 3.3V signals or lower. For details, see your boards specification. For the Jetson Nano, see pages 1-3 of the [Jetson Nano Developer Kit 40-Pin Expansion Header GPIO Usage Considerations Applications Note](https://developer.nvidia.com/jetson-nano-developer-kit-40-pin-expansion-header-gpio-usage-considerations-applications-note).

{{% /alert %}}

Configure a `jetson` board to integrate a [NVIDIA Jetson Orin Module and Developer Kit](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson AGX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), or [NVIDIA Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) into your robot:

{{< tabs name="Configure an jetson Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `jetson` model.
Enter a name for your board and click **Create**.

![An example configuration for a jetson board in the Viam app Config Builder.](/components/board/jetson-ui-config.png)

{{< readfile "/static/include/components/board-attr-config.md" >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-jetson-board-name>",
      "model": "jetson",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "digital_interrupts": [
          <...See table below...>
        ],
        "spis": [
          <...See table below...>
        ],
        "i2cs": [
          <...See table below...>
        ]
      },
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
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See [configuration info](#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](#i2cs). |

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts), and components that must communicate through the [SPI](#spis) and [I<sup>2</sup>C](#i2cs) protocols into your robot.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `spis`

{{< readfile "/static/include/components/board/board-spis.md" >}}

### `i2cs`

{{< readfile "/static/include/components/board/board-i2cs.md" >}}
