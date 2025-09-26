---
title: "Configure an Incremental Encoder (Micro-RDK)"
linkTitle: "incremental (Micro-RDK)"
titleMustBeLong: true
type: "docs"
description: "Configure an incremental encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - /micro-rdk/encoder/incremental/
  - /build/micro-rdk/encoder/incremental/
  - /components/encoder/incremental-micro-rdk/
micrordk_component: true
toc_hide: true
# SMEs: Rand
---

Use the `incremental` encoder model to configure [a quadrature encoder](https://en.wikipedia.org/wiki/Incremental_encoder).

Configuring an `incremental` encoder requires specifying the {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} of the two pins on the board to which the encoder is wired.
These two pins provide the phase outputs used to measure the speed and direction of rotation in relation to a given reference point.

To be able to test the encoder as you configure it, connect the encoder to your microcontroller and power both on.
Then, configure the encoder:

{{< tabs name="Configure an incremental encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `encoder` type, then select the `incremental` model.
Enter a name or use the suggested name for your encoder and click **Create**.

![Configuration of an incremental encoder.](/components/encoder/configure-incremental.png)

Fill in and edit the attributes as applicable.

{{% /tab %}}
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
| `board` | string | **Required** | The `name` of the [board](/operate/reference/components/board/) to which the encoder is wired. |
| `a` | string | **Required** | GPIO number of one of the pins to which the encoder is wired |
| `b` | string | **Required** | GPIO number of the second board pin to which the encoder is wired |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/encoder.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/encoder/" customTitle="Encoder API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
