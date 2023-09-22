---
title: "Configure a fake Gripper"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake gripper."
tags: ["gripper", "components"]
icon: "/icons/components/gripper.svg"
images: ["/icons/components/gripper.svg"]
# SME: Rand
---

You can use a `fake` gripper to test implementing a gripper on your robot without any physical hardware.

Configure a `fake` gripper as follows:

{{< tabs name="Configure a Fake Gripper" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `gripper` type, then select the `fake` model.
Enter a name for your gripper and click **Create**.

![An example configuration for a fake gripper in the Viam app Config Builder.](/components/gripper/fake-gripper-ui-config.png)

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
