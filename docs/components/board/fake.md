---
title: "Configure a fake board"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Configure a fake board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Gautham, Rand
---

Configure a `fake` board to test integrating a board into your robot without physical hardware:

{{< tabs name="Configure an fake Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
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
| `fail_new` | bool | **Required** | If the fake board should raise an error at robot start-up. |
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See [configuration info](#analogs). |
| `digital_interrupts` | object | Optional | Pin and name of any digital interrupts. See [configuration info](#digital_interrupts). |
| `spis` | object | Optional | Any serial peripheral interface (SPI) chip select bus pins' index and name. See [configuration info](#spis). |
| `i2cs` | object | Optional | Any inter-integrated circuit (I2C) bus pins' index and name. See [configuration info](#i2cs). |

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs), [digital interrupts](#digital_interrupts), and components that must communicate through the [SPI](#spis) and [I<sup>2</sup>C](#i2cs) protocols into your robot.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `spis`

{{< readfile "/static/include/components/board/board-spis.md" >}}

### `i2cs`

{{< readfile "/static/include/components/board/board-i2cs.md" >}}
