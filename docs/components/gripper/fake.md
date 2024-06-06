---
title: "Configure a Fake Gripper"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake gripper."
tags: ["gripper", "components"]
icon: true
images: ["/icons/components/gripper.svg"]
aliases:
  - "/components/gripper/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: Rand
---

Configure a `fake` gripper to test implementing a gripper on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gripper" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `gripper` type, then select the `fake` model.
Enter a name or use the suggested name for your gripper and click **Create**.

![An example configuration for a fake gripper in the Viam app Config Builder.](/components/gripper/fake-gripper-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gripper-name>",
  "model": "fake",
  "type": "gripper",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake grippers.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gripper/fake/gripper.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/gripper-control.md" >}}
