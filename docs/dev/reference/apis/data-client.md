---
title: "Upload and Retrieve Data with Viam's Data Client API"
linkTitle: "Data Client"
weight: 10
type: "docs"
description: "Use the data client API to upload and retrieve data directly to the Viam app."
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

The data client API allows you to upload and retrieve data to and from the Viam Cloud.

The data client API supports the following methods:

Methods to upload data like images or sensor readings directly to the [Viam app](https://app.viam.com):

{{< readfile "/static/include/app/apis/generated/data_sync-table.md" >}}

Methods to download, filter, tag, or perform other tasks on data like images or sensor readings:

{{< readfile "/static/include/app/apis/generated/data-table.md" >}}

Methods to work with datasets:

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

## Establish a connection

To use the Viam data client API, you first need to instantiate a `ViamClient` and then instantiate a `DataClient`.

You will also need an API key and API key ID to authenticate your session.
To get an API key (and corresponding ID), you have two options:

- [Create an API key using the Viam app](/operate/control/api-keys/#add-an-api-key)
- [Create an API key using the Viam CLI](/dev/tools/cli/#create-an-organization-api-key)

The following example instantiates a `ViamClient`, authenticating with an API key, and then instantiates a `DataClient`:

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
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
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
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="5"}
async function connect(): Promise<VIAM.ViamClient> {
  // Replace "<API-KEY-ID>" (including brackets) with your machine's
  const API_KEY_ID = "<API-KEY-ID>";
  // Replace "<API-KEY>" (including brackets) with your machine's API key
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

const appClient = await connect();
const dataClient = appClient.dataClient;
```

{{% /tab %}}
{{< /tabs >}}

Once you have instantiated a `DataClient`, you can run [API methods](#api) against the `DataClient` object (named `data_client` in the examples).

## API

{{< readfile "/static/include/app/apis/generated/data_sync.md" >}}

{{< readfile "/static/include/app/apis/generated/data.md" >}}

{{< readfile "/static/include/app/apis/generated/dataset.md" >}}

## Find part ID

To copy the ID of your machine part, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**.

For example:

{{<imgproc src="/build/program/data-client/grab-part-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Part ID displayed in the Viam app.">}}
