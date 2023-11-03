---
title: "Configure a fake Gantry"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake gantry."
tags: ["gantry", "components"]
icon: "/icons/components/gantry.svg"
images: ["/icons/components/gantry.svg"]
# SME: Rand
---

You can use a `fake` gantry to test implementing a gantry component on your robot without any physical hardware.

Configure a `fake` gantry as follows:

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
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
