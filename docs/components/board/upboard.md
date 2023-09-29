---
title: "Configure an upboard board"
linkTitle: "upboard"
weight: 70
type: "docs"
description: "Configure an upboard board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Susmita
---

Configure an `upboard` board to integrate an Intel-based board like the [UP4000](https://github.com/up-board/up-community/wiki/Pinout_UP4000) into your robot.

Complete the following setup requirements, then move on to configuring your board in [the Viam app](https://app.viam.com):

## Setup requirements

Flash your Intel-based board with:

1. The Ubuntu `"Server install image"` version of the operating system.
   For example, `ubuntu-22.04.2-live-server-amd64.iso`.
   Follow [these instructions](https://ubuntu.com/tutorials/install-ubuntu-server) to install Ubuntu Server.
1. The [pin control driver](https://github.com/up-division/pinctrl-upboard).
   Follow [these instructions](https://github.com/up-division/pinctrl-upboard) to install the pin control driver.
   This driver stabilizes the [GPIO pin mapping definition](https://github.com/up-board/up-community/wiki/Pinout) on the board to make it identical to that of a [Raspberry Pi](/components/board/pi/).

{{< tabs name="Configure an upboard Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
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
      "pin": "<pin-number>",
      "type": "< basic | servo >"
    }
  ],
  "i2cs": [
    {
      "name": "<your-bus-name>",
      "bus": "<your-bus-index>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "i2cs": [
    {
      "name": "my-i2c-bus1",
      "bus": "1"
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
      "type": "board",
      "model": "upboard",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "<your-digital-interrupt-name>",
            "pin": "<pin-number>",
            "type": "< basic | servo >"
          }
        ],
        "i2cs": [
          {
            "name": "<your-bus-name>",
            "bus": "<your-bus-index>"
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
      "type": "board",
      "model": "upboard",
      "attributes": {
        "i2cs": [
          {
            "name": "my-i2c-bus1",
            "bus": "1"
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
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](/components/board/#i2cs). |
