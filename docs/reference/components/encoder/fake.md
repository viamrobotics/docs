---
title: "fake"
linkTitle: "fake"
type: "docs"
description: "Reference for the fake encoder model. Fake encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
weight: 10
aliases:
  - "/operate/reference/components/encoder/fake/"
  - "/components/encoder/fake/"
  - "/reference/components/encoder/fake/"
component_description: "An encoder model for testing."
# SMEs: Rand
---

The `fake` encoder is an encoder model for testing code without any hardware.

{{< tabs name="Configure an fake encoder" >}}
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
