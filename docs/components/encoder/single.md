---
title: "Configure a single encoder"
linkTitle: "single"
type: "docs"
description: "Configure a single encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - "/components/encoder/single/"
# SMEs: Rand
---

A `single` encoder sends a signal from the rotating encoder over a single wire to one pin on the [board](/components/board/).
The direction of spin is dictated by the [motor](/components/motor/) that has this encoder's name in its `encoder` attribute field.

{{< tabs name="Configure an single encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `encoder` type, then select the `single` model.
Enter a name for your encoder and click **Create**.

![Configuration of a single encoder in the Viam app config builder.](/components/encoder/configure-single.png)

Fill in and edit the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "single",
  "type": "encoder",
  "namespace": "rdk",
  "attributes": {
    "board": "<your-board-name>",
    "pins": {
      "i": "<your-pin-number-on-board>"
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `single` encoders:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/components/board/) to which the encoder is wired. |
| `pins` | object | **Required** | A struct holding the name of the pin wired to the encoder: <ul> <li> <code>i</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of the pin to which the encoder is wired. </li> </ul> |

Viam also supports a model of encoder called [`"incremental"`](../incremental/) which uses two pins.

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
