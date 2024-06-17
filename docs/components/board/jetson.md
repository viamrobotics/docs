---
title: "Configure a Jetson Board"
linkTitle: "jetson"
weight: 20
type: "docs"
description: "Configure a jetson board to integrate an NVIDIA Jetson Orin Module and Developer Kit, NVIDIA Jetson AGX, or NVIDIA Jetson Nano into your machine."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/jetson/"
component_description: "NVIDIA Jetson AGX Orin, NVIDIA Jetson Orin Nano, NVIDIA Jetson Xavier NX, NVIDIA Jetson Nano."
usage: 999999
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow one of our Jetson [setup guides](/get-started/installation/) to prepare your board for running `viam-server` before configuring a `jetson` board.

If you have a CSI camera, follow [these instructions](https://github.com/viamrobotics/csi-camera) to configure it using the `viam:camera:csi` model.

{{% /alert %}}

{{% alert title="CAUTION" color="caution" %}}

The GPIO pins on Jetson boards are rated for 3.3V signals.
5V signals from encoders and sensors can cause damage to a pin.
We recommend selecting hardware that can operate 3.3V signals or lower.
For details, see your board's specification.
For the Jetson Nano, see pages 1-3 of the [Jetson Nano Developer Kit 40-Pin Expansion Header GPIO Usage Considerations Applications Note](https://developer.nvidia.com/jetson-nano-developer-kit-40-pin-expansion-header-gpio-usage-considerations-applications-note).

{{% /alert %}}

Configure a `jetson` board to integrate an [NVIDIA Jetson Orin Module and Developer Kit](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson AGX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), or [NVIDIA Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `jetson` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example configuration for a Jetson board in the Viam app Config Builder.](/components/board/jetson-ui-config.png)

Edit the attributes as applicable to your board, according to the table below.

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
          {
            "name": "<your-digital-interrupt-name>",
            "pin": "<pin-number>"
          }
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |

## Attribute configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts) into your machine.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
