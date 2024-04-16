---
title: "Configure a BeagleBone Board"
linkTitle: "beaglebone"
weight: 40
type: "docs"
description: "Configure a BeagleBone board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/beaglebone/"
# SMEs: Gautham, Rand
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/get-started/installation/prepare/beaglebone-setup/) to prepare your BeagleBone for running `viam-server` before configuring a `beaglebone` board.

{{% /alert %}}

Configure a `beaglebone` board to integrate [BeagleBoard's BeagleBone AI 64](https://www.beagleboard.org/boards/beaglebone-ai-64) into your machine:

{{< tabs name="Configure an beaglebone Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `beaglebone` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example configuration for a beaglebone board in the Viam app Config Builder.](/components/board/beaglebone-ui-config.png)

Edit the attributes as applicable to your board, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-beaglebone-board>",
      "model": "beaglebone",
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

The following attributes are available for `beaglebone` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts). |

## Attribute configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts) into your machine.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
