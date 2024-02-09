---
title: "Configure a Fake Generic Service"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake generic service using the generic service API."
tags: ["generic", "services"]
---

Configure a `fake` generic service to test implementing a generic service on your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Services** subtab and click **Create service**.
Select the `generic` type, then select the `fake` model.
Enter a name for your generic service and click **Create**.

![An example configuration for a fake generic service in the Viam app Config Builder.](/components/generic/fake-generic-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-generic-service-name>",
  "model": "fake",
  "type": "generic",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for the `fake` generic service.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/services/generic/fake/generic.go) for API call return specifications.
