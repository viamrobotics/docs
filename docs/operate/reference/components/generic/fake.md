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
---

Configure a `fake` generic component to test implementing a generic component on your machine without any physical hardware:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `generic` type, then select the `fake` model.
Enter a name or use the suggested name for your generic component and click **Create**.

![An example configuration for a fake generic component in the Viam app Config Builder.](/components/generic/fake-generic-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-generic-component-name>",
  "model": "fake",
  "type": "generic",
  "namespace": "rdk",
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
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{< /cards >}}