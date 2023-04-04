---
title: "Configure a Fake Base"
linkTitle: "fake"
weight: 50
type: "docs"
description: "Configure a fake base to use for testing without physical hardware."
tags: ["base", "components"]
# SMEs: Steve B
---

Configure a `fake` base to test implementing a base component on your robot without any physical hardware.

Configure a `fake` base as follows:

{{< tabs name="Configure a Fake Base" >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": <"base_name">,
    "type": "base",
    "model": "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake bases.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/base/fake/base.go) for API call return specifications.
