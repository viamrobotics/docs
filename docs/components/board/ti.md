---
title: "Configure a ti board"
linkTitle: "ti"
weight: 20
type: "docs"
description: "Configure a ti board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/ti/"
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="caution" %}}

Follow the [setup guide](/get-started/installation/prepare/sk-tda4vm/) to prepare your TDA4VM for running `viam-server` before configuring a `ti` board.

{{% /alert %}}

Configure a `ti` board to integrate a [Texas Instruments TDA4VM](https://devices.amazonaws.com/detail/a3G8a00000E2QErEAN/TI-TDA4VM-Starter-Kit-for-Edge-AI-vision-systems) into your robot:

{{< tabs name="Configure an ti Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `ti` model.
Enter a name for your board and click **Create**.

![An example configuration for a ti board in the Viam app Config Builder.](/components/board/ti-ui-config.png)

{{< readfile "/static/include/components/board-attr-config.md" >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-ti-board>",
      "model": "ti",
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

The following attributes are available for `ti` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |
| `spis` | object | Optional | Any Serial Peripheral Interface (SPI) chip select bus pins' index and name. See [configuration info](#spis). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) bus pins' index and name. See [configuration info](#i2cs). |

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts), and components that must communicate through the [SPI](#spis) and [I<sup>2</sup>C](#i2cs) protocols into your robot.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `spis`

{{< readfile "/static/include/components/board/board-spis.md" >}}

### `i2cs`

{{< readfile "/static/include/components/board/board-i2cs.md" >}}
