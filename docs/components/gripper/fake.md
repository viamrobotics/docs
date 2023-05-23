---
title: "Configure a fake Gripper"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake gripper."
tags: ["gripper", "components"]
icon: "/components/img/components/gripper.svg"
images: ["/components/img/components/gripper.svg"]
# SME: Rand
---

You can use a `fake` gripper to test implementing a gripper on your robot without any physical hardware.

Configure a `fake` gripper as follows:

{{< tabs name="Configure a Fake Gripper" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your gripper, select the type `gripper`, and select the `fake` model.

Click **Create component**:

![An example configuration for a fake gripper in the Viam app Config Builder.](../img/fake-gripper-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-fake-gripper-name>",
    "type": "gripper",
    "model": "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake grippers.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gripper/fake/gripper.go) for API call return specifications.
