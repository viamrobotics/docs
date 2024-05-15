---
title: "Debug SDK Code"
linkTitle: "Debug"
weight: 60
type: "docs"
description: "Read and filter logs to fix issues while programming with Viam's SDKs."
images: ["/machine/services/icons/sdk.svg"]
tags: ["client", "sdk", "logs", "debug", "machine", "viam-server"]
aliases:
  - /program/debug/
---

Read and filter a machine's logs to view updates from your machine's `viam-server` instance and troubleshoot issues with your program.

{{< tabs >}}
{{% tab name="App UI" %}}

Navigate to the **LOGS** tab of your machine's page in [the Viam app](https://app.viam.com).

Use the **Filter** input to filter the logs by key terms, and select from the **Levels** dropdown menu to filter the logs by warning level:

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
