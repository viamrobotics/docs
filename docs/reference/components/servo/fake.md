---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake servo model. Fake servo."
tags: ["servo", "components"]
icon: true
images: ["/icons/components/servo.svg"]
aliases:
  - "/components/servo/fake/"
  - "/reference/components/servo/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: Rand
---

Configure a `fake` servo to test implementing a servo component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Servo" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-servo-name>",
  "model": "fake",
  "api": "rdk:component:servo",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake servos.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/servo/fake/servo.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/servo-control.md" >}}
