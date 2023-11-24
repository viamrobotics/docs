---
title: "Configure a fake encoder"
linkTitle: "fake"
type: "docs"
description: "Configure a fake encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
weight: 10
aliases:
  - "/components/encoder/fake/"
# SMEs: Rand
---

The `fake` encoder is an encoder model for testing code without any hardware.

{{< tabs name="Configure an fake encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `encoder` type, then select the `fake` model.
Enter a name for your encoder and click **Create**.

![Configuration of a fake encoder in the Viam app config builder.](/build/configure/components/encoder/configure-fake.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "fake",
  "type": "encoder",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "myEncoder",
  "model": "fake",
  "type": "encoder",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` encoders.

## Test the encoder

Once your encoder is configured and your robot is connected, go to the [**Control** tab](/fleet/robots/#control) and click on the encoder's dropdown panel.
The ticks count is displayed.

![Encoder control panel.](/build/configure/components/encoder/control.png)
