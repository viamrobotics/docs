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
component_description: "A model used for testing, with no physical hardware."
toc_hide: true
# SME: Rand
---

Configure a `fake` servo to test implementing a servo component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `servo` type, then select the `fake` model.
Enter a name or use the suggested name for your servo and click **Create**.

{{< imgproc src="/components/servo/fake-servo-ui-config.png" alt="An example configuration for a fake servo." resize="1200x" style="width:650px" class="shadow"  >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-servo-name>",
  "model": "fake",
  "api": "rdk:component:servo",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake servos.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/servo/fake/servo.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/servo-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/servo.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/servo/" customTitle="Servo API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
