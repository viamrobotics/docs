---
title: "Configure a Single Encoder"
linkTitle: "single"
type: "docs"
description: "Configure a single encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - "/components/encoder/single/"
component_description: "A single pin 'pulse output' encoder which returns its relative position but no direction."
toc_hide: true
# SMEs: Rand
---

A `single` encoder sends a signal from the rotating encoder over a single wire to one pin on the [board](/operate/reference/components/board/).
The direction of spin is dictated by the [motor](/operate/reference/components/motor/) that has this encoder's name in its `encoder` attribute field.

To be able to test the encoder as you configure it, connect the encoder to your machine's computer and power both on.
Then, configure the encoder:

{{< tabs name="Configure an single encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `encoder` type, then select the `single` model.
Enter a name or use the suggested name for your encoder and click **Create**.

![Configuration of a single encoder.](/components/encoder/configure-single.png)

Fill in and edit the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "single",
  "api": "rdk:component:encoder",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/operate/reference/components/board/) to which the encoder is wired. |
| `pins` | object | **Required** | A struct holding the name of the pin wired to the encoder: <ul> <li> <code>i</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of the pin to which the encoder is wired. </li> </ul> |

Viam also supports a model of encoder called [`"incremental"`](../incremental/) which uses two pins.

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/encoder.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/encoder/" customTitle="Encoder API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
