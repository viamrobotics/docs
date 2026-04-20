---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake gripper model. Fake gripper."
tags: ["gripper", "components"]
icon: true
images: ["/icons/components/gripper.svg"]
aliases:
  - "/components/gripper/fake/"
  - "/reference/components/gripper/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: Rand
---

Configure a `fake` gripper to test implementing a gripper on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gripper" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gripper-name>",
  "model": "fake",
  "api": "rdk:component:gripper",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake grippers.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gripper/fake/gripper.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/gripper-control.md" >}}
