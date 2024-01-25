---
title: "Configure a Fake Servo"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake servo."
tags: ["servo", "components"]
icon: "/icons/components/servo.svg"
aliases:
  - "/components/servo/fake/"
# SME: Rand
---

You can use a `fake` servo to test implementing a servo component on your machine without any physical hardware.

Configure a `fake` servo as follows:

{{< tabs name="Configure a Fake Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `servo` type, then select the `fake` model.
Enter a name for your servo and click **Create**.

![An example configuration for a fake servo in the Viam app Config Builder.](/components/servo/fake-servo-ui-config.png)

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
