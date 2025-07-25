---
title: "Configure a Fake Base"
linkTitle: "fake"
weight: 20
type: "docs"
description: "Configure a fake base to use for testing without physical hardware."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/fake/"
component_description: "A model used for testing, with no physical hardware."
toc_hide: true
# SMEs: Steve B
---

Configure a `fake` base to test implementing a base component on your machine without any physical hardware:

{{< tabs name="Configure a Fake Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `base` type, then select the `fake` model.
Enter a name or use the suggested name for your base and click **Create**.

{{< imgproc src="/components/base/fake-base-ui-config.png" alt="An example configuration for a fake base." resize="1200x" style="width: 900px" class="shadow" >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-base-name>",
  "api": "rdk:component:base",
  "model": "fake",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for `fake` bases.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/base/fake/fake.go) for API call return specifications.

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/base.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/base/" customTitle="Base API" noimage="true" %}}
{{% card link="/tutorials/configure/configure-rover/" noimage="true" %}}
{{% card link="/tutorials/control/drive-rover/" noimage="true" %}}
{{< /cards >}}
