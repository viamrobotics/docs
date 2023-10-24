---
title: "Configure an incremental encoder"
linkTitle: "incremental"
type: "docs"
description: "Configure an incremental encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
# SMEs: Rand
---

Use the `incremental` encoder model to configure [a quadrature encoder](https://en.wikipedia.org/wiki/Incremental_encoder).

Configuring an `incremental` encoder requires specifying the {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} of the two pins on the board to which the encoder is wired.
These two pins provide the phase outputs used to measure the speed and direction of rotation in relation to a given reference point.

{{< tabs name="Configure an incremental encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `encoder` type, then select the `incremental` model.
Enter a name for your encoder and click **Create**.

![Configuration of an incremental encoder in the Viam app config builder.](/components/encoder/configure-incremental.png)

Fill in and edit the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "incremental",
  "type": "encoder",
  "namespace": "rdk",
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
      "name": "myEncoder",
      "model": "incremental",
      "type": "encoder",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/micro-rdk/board/) to which the encoder is wired. |
| `pins` | object | **Required** | A struct holding the names of the pins wired to the encoder: <ul> <li> <code>a</code>: GPIO number of one of the pins to which the encoder is wired. </li> <li> <code>b</code>: GPIO number of the second board pin to which the encoder is wired. </li> </ul> |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
