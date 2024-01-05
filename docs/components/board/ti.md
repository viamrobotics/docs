---
title: "Configure a TI Board"
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

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
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

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts) into your machine.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
