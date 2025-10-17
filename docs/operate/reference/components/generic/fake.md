---
title: "Configure a Fake Generic Component"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake generic component."
tags: ["generic", "components"]
aliases:
  - "/components/generic/fake/"
component_description: "A model used for testing, with no physical hardware."
toc_hide: true
---

Configure a `fake` generic component to test implementing a generic component on your machine without any physical hardware:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `generic` type, then select the `fake` model.
Enter a name or use the suggested name for your generic component and click **Create**.

![An example configuration for a fake generic component.](/components/generic/fake-generic-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-generic-component-name>",
  "model": "fake",
  "api": "rdk:component:generic",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for the `fake` generic component.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/generic/fake/generic.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/generic-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/generic.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/generic/" customTitle="Generic API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
