---
title: "Configure a Fake Servo"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake servo."
tags: ["servo", "components"]
icon: true
images: ["/icons/components/servo.svg"]
aliases:
  - "/components/servo/fake/"
# SME: Rand
---

Configure a `fake` servo to test implementing a servo component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `servo` type, then select the `fake` model.
Enter a name or use the suggested name for your servo and click **Create**.

{{< imgproc src="/components/servo/fake-servo-ui-config.png" alt="An example configuration for a fake servo in the Viam app Config Builder." resize="1200x" style="width:650px" >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-servo-name>",
  "model": "fake",
  "type": "servo",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake servos.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/servo/fake/servo.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/servo-control.md" >}}
