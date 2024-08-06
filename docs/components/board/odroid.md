---
title: "Configure an Odroid Board"
linkTitle: "odroid"
weight: 50
type: "docs"
description: "Configure an Odroid board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
component_description: "Odroid-C4"
---

{{% alert title="REQUIREMENTS" color="note" %}}

Follow the [setup guide](/installation/prepare/odroid-c4-setup/) to prepare your Odroid-C4 for running `viam-server` before configuring an `odroid` board.

{{% /alert %}}

Configure an `odroid` board to integrate an [Odroid-C4](https://www.hardkernel.com/shop/odroid-c4/) into your machine:

{{< tabs name="Configure an odroid Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `odroid` model.
Enter a name or use the suggested name for your board and click **Create**.

![An example configuration for a odroid board in the Viam app CONFIGURE tab.](/components/board/odroidc4-ui-config.png)

Click the **{}** (Switch to Advanced) button in the top right of the odroid board panel to edit your board's attributes directly with JSON according to the following template.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "analogs": [
    {
      "name": "<your-analog-name>",
      "pin": "<pin-number>"
    }
  ],
  "digital_interrupts": [
    {
      "name": "<your-digital-interrupt-name>",
      "pin": "<pin-number>"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `odroid` boards:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](#digital_interrupts).|
| `analogs` | object | Optional | Attributes of any pins that can be used as Analog-to-Digital Converter (ADC) inputs. See [configuration info](#analogs).|

## Attribute configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts) and [analog-to-digital converters](#analogs) into your machine.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}
