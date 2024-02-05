---
title: "Configure a Fake Base"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Configure a fake base to use for testing without physical hardware."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/fake/"
# SMEs: Steve B
---

Configure a `fake` base to test implementing a base component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `fake` model.
Enter a name for your base and click **Create**.

![An example configuration for a fake base in the Viam app Config Builder.](/components/base/fake-base-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-base-name>",
  "type": "base",
  "model": "fake",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` bases.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/base/fake/fake.go) for API call return specifications.

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}
