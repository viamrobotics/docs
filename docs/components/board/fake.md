---
title: "Configure a Fake Board"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Configure a fake board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/fake/"
# SMEs: Gautham, Rand
---

Configure a `fake` board to test integrating a board into your machine without physical hardware:

{{< tabs name="Configure an fake Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `fake` model.
Enter a name for your board and click **Create**.

![An example configuration for a fake board in the Viam app Config Builder.](/components/board/fake-ui-config.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "fail_new": <boolean>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "fail_new": false
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-fake-board-name>",
      "model": "fake",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "fail_new": <boolean>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `fail_new` | bool | **Required** | If the fake board should raise an error at machine start-up. |
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See [configuration info](#digital_interrupts). |

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
