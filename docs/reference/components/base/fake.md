---
title: "fake"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Reference for the fake base model. Fake base to use for testing without physical hardware."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/fake/"
  - "/reference/components/base/fake/"
component_description: "A model used for testing, with no physical hardware."
# SMEs: Steve B
---

Configure a `fake` base to test implementing a base component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Base" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-base-name>",
  "api": "rdk:component:base",
  "model": "fake",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` bases.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/base/fake/fake.go) for API call return specifications.
