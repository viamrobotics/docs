---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake gantry model. Fake gantry."
tags: ["gantry", "components"]
icon: true
images: ["/icons/components/gantry.svg"]
aliases:
  - "/operate/reference/components/gantry/fake/"
  - "/components/gantry/fake/"
  - "/reference/components/gantry/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: Rand
---

Configure a `fake` gantry to test implementing a gantry component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gantry-name>",
  "model": "fake",
  "api": "rdk:component:gantry",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake gantries.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gantry/fake/gantry.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}
