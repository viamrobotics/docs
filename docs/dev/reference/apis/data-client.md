---
title: "Upload and retrieve data with Viam's data client API"
linkTitle: "Data client"
weight: 10
type: "docs"
description: "Use the data client API to upload and retrieve data directly."
icon: true
images: ["/services/icons/sdk.svg"]
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "data management",
    "data",
  ]
aliases:
  - /program/apis/data-client/
  - /build/program/apis/data-client/
  - /appendix/apis/data-client/

date: "2024-09-19"
# updated: ""  # When the content was last entirely checked
---

The data client allows you to upload and retrieve data to and from the Viam Cloud.

The data client API supports the following methods:

Methods to upload data like images or sensor readings directly to Viam:

{{< readfile "/static/include/app/apis/generated/data_sync-table.md" >}}

Methods to download, filter, tag, or perform other tasks on data like images or sensor readings:

{{< readfile "/static/include/app/apis/generated/data-table.md" >}}

Methods to work with datasets:

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

## Establish a connection

To use the data client API, you need to instantiate a `ViamClient` and then instantiate a `DataClient`.

You need an API key and API key ID with at least [Machine operator permissions](/manage/manage/rbac/#organization-settings-and-roles) to use the data client API.
To get an API key (and corresponding ID), use the [web UI](/operate/control/api-keys/#add-an-api-key)
to the [Viam CLI](/dev/tools/cli/#create-an-organization-api-key).

{{< tabs >}}
{{% tab name="From a client application" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # TODO: Replace "<API-KEY>" (including brackets) with your machine's
        # API key
        payload='<API-KEY>',
      ),
      # TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    # Make a ViamClient
    viam_client = await connect()
    # Instantiate a DataClient to run data client API methods on
    data_client = viam_client.data_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers" data-line="16"}
package main

import (
  "context"

  "go.viam.com/rdk/app"
  "go.viam.com/rdk/logging"
)

func main() {
  logger := logging.NewDebugLogger("client")
  ctx := context.Background()
  // TODO: Replace "<API-KEY>" (including brackets) with your machine's API key
  // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
  // API key ID
  viamClient, err := app.CreateViamClientWithAPIKey(
    ctx, app.Options{}, "<API-KEY>", "<API-KEY-ID>", logger)
  if err != nil {
    logger.Fatal(err)
  }
  defer viamClient.Close()

  dataClient := viamClient.DataClient()
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="3,5"}
async function connect(): Promise<VIAM.ViamClient> {
  // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
  const API_KEY_ID = "<API-KEY-ID>";
  // TODO: Replace "<API-KEY>" (including brackets) with your machine's API key
  const API_KEY = "<API-KEY>";
  const opts: VIAM.ViamClientOptions = {
    serviceHost: "https://app.viam.com:443",
    credentials: {
      type: "api-key",
      authEntity: API_KEY_ID,
      payload: API_KEY,
    },
  };

  const client = await VIAM.createViamClient(opts);
  return client;
}

const viamClient = await connect();
const dataClient = viamClient.dataClient;
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="From within a Module" %}}

See [Use platform APIs from within a module](/operate/modules/advanced/platform-apis/).

{{% /tab %}}
{{< /tabs >}}

Once you have instantiated a `DataClient`, you can run [API methods](#api) against the `DataClient` object (named `data_client` in the examples).

## API

{{< readfile "/static/include/app/apis/generated/data_sync.md" >}}

{{< readfile "/static/include/app/apis/generated/data.md" >}}

{{< readfile "/static/include/app/apis/generated/dataset.md" >}}
