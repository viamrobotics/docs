---
title: "Configure a Fake Gantry"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake gantry."
tags: ["gantry", "components"]
icon: true
images: ["/icons/components/gantry.svg"]
aliases:
  - "/components/gantry/fake/"
component_description: "A model used for testing, with no physical hardware."
toc_hide: true
# SME: Rand
---

Configure a `fake` gantry to test implementing a gantry component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `gantry` type, then select the `fake` model.
Enter a name or use the suggested name for your gantry and click **Create**.

![An example configuration for a fake gantry.](/components/gantry/fake-gantry-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gantry-name>",
  "model": "fake",
  "api": "rdk:component:gantry",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake gantries.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gantry/fake/gantry.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/gantry.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/gantry/" customTitle="Gantry API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
