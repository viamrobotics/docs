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

Configure a `beaglebone` board to integrate [BeagleBoard's BeagleBone AI 64](https://www.beagleboard.org/boards/beaglebone-ai-64) into your robot:

{{< tabs name="Configure an beaglebone Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `beaglebone` model.
Enter a name for your board and click **Create**.

![An example configuration for a beaglebone board in the Viam app Config Builder.](/components/board/beaglebone-ui-config.png)

{{< readfile "/static/include/components/board-attr-config.md" >}}

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
      "attributes": {},
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

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts) into your robot.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
