---
title: "Configure a Fake Generic Component"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake generic component."
tags: ["generic", "components"]
aliases:
  - "/components/generic/fake/"
---

You can use a `fake` generic component to test implementing a generic component on your machine without any physical hardware.

Configure a `fake` component as follows:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `generic` type, then select the `fake` model.
Enter a name for your generic component and click **Create**.

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

No attributes are available for fake generic components.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/generic/fake/generic.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/generic-control.md" >}}
