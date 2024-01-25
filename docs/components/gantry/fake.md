---
title: "Configure a Fake Gantry"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake gantry."
tags: ["gantry", "components"]
icon: "/icons/components/gantry.svg"
images: ["/icons/components/gantry.svg"]
aliases:
  - "/components/gantry/fake/"
# SME: Rand
---

Configure a `fake` gantry to test implementing a gantry component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `gantry` type, then select the `fake` model.
Enter a name for your gantry and click **Create**.

![An example configuration for a fake gantry in the Viam app Config Builder.](/components/gantry/fake-gantry-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gantry-name>",
  "model": "fake",
  "type": "gantry",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake gantries.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gantry/fake/gantry.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}
