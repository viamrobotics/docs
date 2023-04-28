---
title: "Configure a fake Gantry"
linkTitle: "fake"
weight: 90
type: "docs"
description: "Configure a fake gantry."
tags: ["gantry", "components"]
icon: "img/components/gantry.png"
# SME: Rand
---

You can use a `fake` gantry to test implementing a gantry component on your robot without any physical hardware.

Configure a `fake` gantry as follows:

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your gantry, select the type `gantry`, and select the `fake` model.

Click **Create component**:

![An example configuration for a fake gantry in the Viam app Config Builder.](../img/fake-gantry-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": <"your-fake-gantry-name">,
    "type": "gantry",
    "model": "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake gantries.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gantry/fake/gantry.go) for API call return specifications.
