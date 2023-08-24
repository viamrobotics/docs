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

## Set up requirements

Flash your Intel-based board with:

1. The Ubuntu `"Server install image"` version of the operating system. For example, `ubuntu-22.04.2-live-server-amd64.iso`.
Follow [these instructions](https://ubuntu.com/tutorials/install-ubuntu-server) to do so.
1. The [pin control driver](https://github.com/up-division/pinctrl-upboard).
Follow [these instructions](https://github.com/up-division/pinctrl-upboard) to do so.
This driver stabilizes the [GPIO pin mapping definition](https://github.com/up-board/up-community/wiki/Pinout) on the board to make it identical to a [`pi`](/components/board/pi/) board.

{{< tabs name="Configure an upboard Board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your board, and select the type `board`.
Next, select the **Model** card.
Type in `upboard` and hit enter to select the `upboard` model.

Click **Create component**.

![An example configuration for a upboard board in the Viam app Config Builder.](/components/board/upboard-ui-config.png)

Edit and fill in the attributes as applicable.

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
        "i2cs": [],
        "digital_interrupts": []
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `upboard` boards:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `digital_interrupts` | object | Optional | Any digital interrupts's {{< glossary_tooltip term_id="pin-number" text="pin number" >}} and name. See [configuration info](/components/board/#digital_interrupts). |
| `i2cs` | object | Optional | Any Inter-Integrated Circuit (I<sup>2</sup>C) pins' bus index and name. See [configuration info](/components/board/#i2cs). |
