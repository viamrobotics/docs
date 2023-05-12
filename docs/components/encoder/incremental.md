---
title: "Configure an incremental encoder"
linkTitle: "incremental"
type: "docs"
description: "Configure an incremental encoder."
images: ["/components/img/components/encoder.svg"]
tags: ["encoder", "components"]
# SMEs: Rand
---

Use the `incremental` encoder model to configure [a quadrature encoder](https://en.wikipedia.org/wiki/Incremental_encoder).

Configuring an `incremental` encoder requires specifying the {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} of the two pins on the board to which the encoder is wired.
These two pins provide the phase outputs used to measure the speed and direction of rotation in relation to a given reference point.

{{< tabs name="Configure an incremental encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your encoder, select the type `encoder`, and select the `incremental` model.

Click **Create component**.

![Configuration of an incremental encoder in the Viam app config builder.](../img/configure-incremental.png)

Fill in and edit the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-encoder-name>",
    "type": "encoder",
    "model" : "incremental",
    "attributes": {
      "board": "<your-board-name>",
      "pins": {
        "a": "<your-first-pin-number>",
        "b": "<your-second-pin-number>"
      }
    }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {}
    },
    {
      "name": "myEncoder",
      "type": "encoder",
      "model": "incremental",
      "attributes": {
        "board": "local",
        "pins": {
          "a": "13",
          "b": "11"
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `incremental` encoders:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/components/board) to which the encoder is wired. |
| `pins` | object | **Required** | A struct holding the names of the pins wired to the encoder: <ul> <li> <code>a</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of one of the pins to which the encoder is wired. </li> <li> <code>b</code>: Required for two phase encoder. {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} for the second board pin to which the encoder is wired. </li> </ul> |

Viam also supports a model of encoder called [`"single"`](../single) which requires only one pin (`i`).
