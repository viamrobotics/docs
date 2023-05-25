---
title: "Debug SDK Code"
linkTitle: "Debug"
weight: 80
type: "docs"
description: "Read and filter logs to fix issues while programming with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk", "logs", "debug"]
---

<!-- TODO: Introduction with more information about what these logs are actually displaying -->

{{< tabs >}}
{{% tab name="App UI" %}}

Navigate to the **Logs** tab of your robot's page in [the Viam app](https://app.viam.com).

 Use the **Filter** input to filter the logs by key terms, and select from the **Levels** drop-down menu to filter the logs by warning level:

![Filtering by log level of info in the logs tab of the Viam app.](../img/sdks/log-level-info.png)

{{% /tab %}}
{{% tab name="CLI" %}}

{{< tabs >}}
{{% tab name="Linux" %}}

``` shell
sudo journalctl --unit=viam-server
```

{{% /tab %}}
{{% tab name="macOS" %}}

``` shell
cat $(brew --prefix)/var/log/viam.log
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}
