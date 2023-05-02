---
title: "Configure a fake Servo"
linkTitle: "fake"
weight: 90
type: "docs"
description: "Configure a fake servo."
tags: ["servo", "components"]
icon: "img/components/servo.png"
# SME: Rand
---

You can use a `fake` servo to test implementing a servo component on your robot without any physical hardware.

Configure a `fake` servo as follows:

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your servo, select the type `servo`, and select the `fake` model.

Click **Create component**:

![An example configuration for a fake servo in the Viam app Config Builder.](../img/fake-servo-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-fake-servo-name>",
    "type": "servo",
    "model": "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake servos.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/servo/fake/servo.go) for API call return specifications.
