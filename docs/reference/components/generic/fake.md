---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake generic model. Fake generic component."
tags: ["generic", "components"]
aliases:
  - "/components/generic/fake/"
  - "/reference/components/generic/fake/"
component_description: "A model used for testing, with no physical hardware."
---

Configure a `fake` generic component to test implementing a generic component on your machine without any physical hardware:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-generic-component-name>",
  "model": "fake",
  "api": "rdk:component:generic",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for the `fake` generic component.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/generic/fake/generic.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/generic-control.md" >}}
