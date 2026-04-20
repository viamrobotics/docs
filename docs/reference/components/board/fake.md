---
title: "fake"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Reference for the fake board model. Fake board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/fake/"
  - "/reference/components/board/fake/"
component_description: "A model used for testing, with no physical hardware."
# SMEs: Gautham, Rand
---

The `fake` board returns incrementing values for digital interrupt ticks and analogs.

Configure a `fake` board to test integrating a board into your machine without physical hardware:

{{< tabs name="Configure an fake Board" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-fake-board-name>",
      "model": "fake",
      "api": "rdk:component:board",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `fail_new` | bool | **Required** | If the fake board should raise an error at machine start-up. |
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See [configuration info](#digital_interrupts). |

## Attribute configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
