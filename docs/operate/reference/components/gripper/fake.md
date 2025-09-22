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
toc_hide: true
# SME: Rand
---

Configure a `fake` gripper to test implementing a gripper on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gripper" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `gripper` type, then select the `fake` model.
Enter a name or use the suggested name for your gripper and click **Create**.

![An example configuration for a fake gripper.](/components/gripper/fake-gripper-ui-config.png)

{{% /tab %}}
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

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/gripper.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/gripper/" customTitle="Gripper API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper/" noimage="true" %}}
{{< /cards >}}
