---
title: "Configure an UP Board"
linkTitle: "upboard"
weight: 70
type: "docs"
description: "Configure an UP board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/upboard/"
# SMEs: Susmita
---

Configure an `upboard` board to integrate an Intel-based board like the [UP 4000](https://github.com/up-board/up-community/wiki/Pinout_UP4000) into your machine.

Complete the following setup requirements, then move on to configuring your board in [the Viam app](https://app.viam.com):

## Setup requirements

You must flash your Intel-based board with:

1. The Ubuntu `"Server install image"` version of the operating system.
   For example, `ubuntu-22.04.2-live-server-amd64.iso`.
   Follow [these instructions](https://ubuntu.com/tutorials/install-ubuntu-server) to install Ubuntu Server.
2. The [pin control driver](https://github.com/up-division/pinctrl-upboard).
   This driver is necessary to stabilize the [GPIO pin mapping definition](https://github.com/up-board/up-community/wiki/Pinout) on the board, making the pin mapping identical to that of a [Raspberry Pi](/components/board/pi/).
   Follow [these instructions](https://github.com/up-division/pinctrl-upboard) to install the pin control driver.

{{< tabs name="Configure an upboard Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `upboard` model.
Enter a name for your board and click **Create**.

![An example configuration for a upboard board in the Viam app Config Builder.](/components/board/upboard-ui-config.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "digital_interrupts": [
    {
      "name": "<your-digital-interrupt-name>",
      "pin": "<pin-number>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "digital_interrupts": [
    {
      "name": "your-interrupt",
      "pin": "18"
    }
  ]
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
      "name": "<your-upboard-board>",
      "model": "upboard",
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
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-upboard-board>",
      "model": "upboard",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "your-interrupt",
            "pin": "18"
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

The following attributes are available for `upboard` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/components/board/#digital_interrupts). |

## Attribute configuration

Configuring these attributes on your board allows you to integrate [digital interrupts](#digital_interrupts) into your machine.

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}
