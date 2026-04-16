---
title: "single"
linkTitle: "single"
type: "docs"
description: "Reference for the single encoder model. Single encoder with a microcontroller."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - /micro-rdk/encoder/single/
  - /build/micro-rdk/encoder/single/
  - /components/encoder/single-micro-rdk/
  - "/operate/reference/components/encoder/single-micro-rdk/"
micrordk_component: true
# SMEs: Rand
---

A `single` encoder sends a signal from the rotating encoder over a single wire to one pin on the [board](/reference/components/board/).
The direction of spin is dictated by the [motor](/reference/components/motor/) that has this encoder's name in its `encoder` attribute field.

To be able to test the encoder as you configure it, connect the encoder to your machine's computer and power both on.

{{< tabs name="Configure an single encoder" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "single",
  "api": "rdk:component:encoder",
  "attributes": {
    "pin": <int>,
    "dir_flip": <boolean>
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "single",
  "api": "rdk:component:encoder",
  "attributes": {
    "pin": 22,
    "dir_flip": false
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `single` encoders:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | object | **Required** | GPIO number of the pin to which the encoder is wired. |
| `dir_flip` | boolean | **Required** | If the encoder's count should increment or decrement in its initial state before a [`SetPower()`](/reference/apis/components/motor/#setpower) call is made to an encoded [motor](/reference/components/motor/). `true` implies decrement. |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
