---
title: "Configure a Single Encoder (viam-micro-server)"
linkTitle: "single"
type: "docs"
description: "Configure a single encoder with a microcontroller."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - /micro-rdk/encoder/single/
  - /build/micro-rdk/encoder/single/
micrordk_component: true
# SMEs: Rand
---

A `single` encoder sends a signal from the rotating encoder over a single wire to one pin on the [board](/components/board/).
The direction of spin is dictated by the [motor](/components/motor/) that has this encoder's name in its `encoder` attribute field.

To be able to test the encoder as you configure it, connect the encoder to your machine's computer and power both on.
Then, configure the encoder:

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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | object | **Required** | GPIO number of the pin to which the encoder is wired. |
| `dir_flip` | boolean | **Required** | If the encoder's count should increment or decrement in its initial state before a [`SetPower()`](/appendix/apis/components/motor/#setpower) call is made to an encoded [motor](/components/motor/). `true` implies decrement. |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}

## Next steps

For more configuration and development info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/encoder/" customTitle="Encoder API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{< /cards >}}
