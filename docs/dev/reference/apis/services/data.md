---
title: "Data Management Service API"
linkTitle: "Data Management"
weight: 10
type: "docs"
description: "Give commands to your data management service to sync data stored on the machine it is deployed on to the cloud."
icon: true
images: ["/icons/components/arm.svg"]
date: "2022-01-01"
aliases:
   - /appendix/apis/services/data/
# updated: ""  # When the content was last entirely checked
---

The data management service API allows you to sync data stored on the machine it is deployed on to the cloud.

The [data management service](/data-ai/capture-data/capture-sync/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/data_manager-table.md" >}}

The data client API supports a separate set of methods that allow you to upload and export data to and from the Viam app.
For information about that API, see [Data Client API](/dev/reference/apis/data-client/).

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on the [Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume that you have a machine configured with an `data_manager` service.

{{< tabs >}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/datamanager"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/data_manager.md" >}}
