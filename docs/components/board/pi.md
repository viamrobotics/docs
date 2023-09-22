---
title: "Configure a pi board"
linkTitle: "pi"
weight: 20
type: "docs"
description: "Configure a pi board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow this [setup guide](/installation/prepare/rpi-setup/) to prepare your Pi for running `viam-server` before configuring a `pi` board.

{{% /alert %}}

Configure a `pi` board to integrate a [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) or [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) into your robot:

{{< tabs name="Configure an pi Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `pi` model.
Enter a name for your board and click **Create**.

![An example board configuration in the app builder UI. The name (local), type (board) and model (pi) are shown. No other attributes are configured.](/tutorials/scuttlebot/board-empty-json.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "type": "board",
      "model": "pi",
      "name": "<board_name>"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](/components/board/#analogs). |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/components/board/#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select pins' bus index and name. See [configuration info](/components/board/#spis). Review [these instructions](/installation/prepare/rpi-setup/#enable-communication-protocols) to learn how to enable SPI on a Raspberry Pi 4. |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](/components/board/#i2cs). Review [these instructions](/installation/prepare/rpi-setup/#enable-communication-protocols) to learn how to enable I<sup>2</sup>C on a Raspberry Pi 4. |
