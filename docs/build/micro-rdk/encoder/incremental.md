---
title: "Configure an Incremental Encoder (Micro-RDK)"
linkTitle: "incremental"
type: "docs"
description: "Configure an incremental encoder with a microcontroller."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - /micro-rdk/encoder/incremental/
# SMEs: Rand
---

Use the `incremental` encoder model to configure [a quadrature encoder](https://en.wikipedia.org/wiki/Incremental_encoder).

Configuring an `incremental` encoder requires specifying the {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} of the two pins on the board to which the encoder is wired.
These two pins provide the phase outputs used to measure the speed and direction of rotation in relation to a given reference point.

{{< tabs name="Configure an incremental encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `encoder` type, then select the `incremental` model.
Enter a name or use the suggested name for your encoder and click **Create**.

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
    "a": "<your-first-pin-number>",
    "b": "<your-second-pin-number>"
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
        "a": "13",
        "b": "11"
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
| `board` | string | **Required** | The `name` of the [board](/build/micro-rdk/board/) to which the encoder is wired. |
| `a` | string | **Required** | GPIO number of one of the pins to which the encoder is wired |
| `b` | string | **Required** | GPIO number of the second board pin to which the encoder is wired |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
