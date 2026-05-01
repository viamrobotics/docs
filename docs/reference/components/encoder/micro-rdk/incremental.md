---
title: "incremental"
linkTitle: "incremental"
titleMustBeLong: true
type: "docs"
description: "Reference for the incremental encoder model. Incremental encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - "/operate/reference/components/encoder/incremental-micro-rdk/"
  - /micro-rdk/encoder/incremental/
  - /build/micro-rdk/encoder/incremental/
  - /components/encoder/incremental-micro-rdk/
  - "/reference/components/encoder/incremental-micro-rdk/"
micrordk_component: true
# SMEs: Rand
---

Use the `incremental` encoder model to configure [a quadrature encoder](https://en.wikipedia.org/wiki/Incremental_encoder).

Configuring an `incremental` encoder requires specifying the {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} of the two pins on the board to which the encoder is wired.
These two pins provide the phase outputs used to measure the speed and direction of rotation in relation to a given reference point.

To be able to test the encoder as you configure it, connect the encoder to your microcontroller and power both on.

{{< tabs name="Configure an incremental encoder" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "incremental",
  "api": "rdk:component:encoder",
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
      "api": "rdk:component:encoder",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/reference/components/board/) to which the encoder is wired. |
| `a` | string | **Required** | GPIO number of one of the pins to which the encoder is wired |
| `b` | string | **Required** | GPIO number of the second board pin to which the encoder is wired |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
