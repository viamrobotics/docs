---
title: "Configure a Fake Generic Service"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake generic service using the generic service API."
service_description: "A model used for testing a generic service."
tags: ["generic", "services"]
aliases:
  - /registry/advanced/generic/fake/
  - /services/generic/fake/
---

Configure a `fake` generic service to test implementing a generic service on your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** button and select **Component or service**.
Select the `generic` type, then select the `fake` model.
Enter a name or use the suggested name for your generic service and click **Create**.

![An example configuration for a fake generic service.](/services/fake-generic-service-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-generic-service-name>",
  "model": "fake",
  "api": "rdk:component:generic",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for the `fake` generic service.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/services/generic/fake/generic.go) for API call return specifications.
