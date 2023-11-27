---
title: "Configure a single encoder"
linkTitle: "single"
type: "docs"
description: "Configure a single encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - /micro-rdk/encoder/single/
# SMEs: Rand
---

A `single` encoder sends a signal from the rotating encoder over a single wire to one pin on the [board](/build/configure/components/board/).
The direction of spin is dictated by the [motor](/build/configure/components/motor/) that has this encoder's name in its `encoder` attribute field.

{{< tabs name="Configure an single encoder" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "single",
  "type": "encoder",
  "namespace": "rdk",
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
  "type": "encoder",
  "namespace": "rdk",
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
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | object | **Required** | GPIO number of the pin to which the encoder is wired. |
| `dir_flip` | boolean | **Required** | If the encoder's count should increment or decrement in its initial state before a [`SetPower()`](/build/configure/components/motor/#setpower) call is made to an encoded [motor](/build/micro-rdk/motor/). `true` implies decrement. |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
