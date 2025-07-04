---
title: "Configure a Fake Encoder"
linkTitle: "fake"
type: "docs"
description: "Configure a fake encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
weight: 10
aliases:
  - "/components/encoder/fake/"
component_description: "An encoder model for testing."
toc_hide: true
# SMEs: Rand
---

The `fake` encoder is an encoder model for testing code without any hardware.

{{< tabs name="Configure an fake encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `encoder` type, then select the `fake` model.
Enter a name or use the suggested name for your encoder and click **Create**.

![Configuration of a fake encoder.](/components/encoder/configure-fake.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "fake",
  "api": "rdk:component:encoder",
  "attributes": {}
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "myEncoder",
  "model": "fake",
  "api": "rdk:component:encoder",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` encoders.

## Test the encoder

Once your encoder is configured and your machine is connected, go to the [**CONTROL** tab](/manage/troubleshoot/teleoperate/default-interface/) and click on the encoder's dropdown panel.
The ticks count is displayed.

![Encoder control panel.](/components/encoder/control.png)

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/encoder.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/encoder/" customTitle="Encoder API" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
