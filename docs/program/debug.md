---
title: "Debug SDK Code"
linkTitle: "Debug"
weight: 60
type: "docs"
description: "Read and filter logs to fix issues while programming with Viam's SDKs."
images: ["/services/icons/sdk.svg"]
tags: ["client", "sdk", "logs", "debug", "robot", "viam-server"]
---

Read and filter a robot's logs to view updates from your robot's `viam-server` instance and troubleshoot issues with your program.

{{< tabs >}}
{{% tab name="App UI" %}}

Navigate to the **Logs** tab of your robot's page in [the Viam app](https://app.viam.com).

Use the **Filter** input to filter the logs by key terms, and select from the **Levels** drop-down menu to filter the logs by warning level:

![Filtering by log level of info in the logs tab of the Viam app.](/program/sdks/log-level-info.png)

{{% /tab %}}
{{% tab name="CLI" %}}

{{< tabs >}}
{{% tab name="Linux" %}}

```sh {class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-server
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {class="command-line" data-prompt="$"}
cat $(brew --prefix)/var/log/viam.log
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}
