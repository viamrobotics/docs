---
title: "Debug SDK Code"
linkTitle: "Debug"
weight: 80
type: "docs"
description: "How to use Viam debugging tools."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

## Debug

{{< tabs >}}
{{% tab name="App UI" %}}

Check the Logs tab to check for any errors or other info from viam-server.

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

<!-- Should there be a separate section for handling errors in Go etc.?  -->