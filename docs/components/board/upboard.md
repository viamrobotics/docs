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

Configure an `upboard` board to integrate an Intel-based board like the [UP4000](https://github.com/up-board/up-community/wiki/Pinout_UP4000) into your robot:

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
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `upboard` boards.
