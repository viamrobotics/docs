---
title: "Upload and Retrieve Data with Viam's Data Client API"
linkTitle: "Data Client"
weight: 10
type: "docs"
description: "Use the data client API to upload and retrieve data directly to the Viam app."
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
---

The data client API allows you to upload and retrieve data to and from the [Viam app](https://app.viam.com).

{{% alert title="Support Notice" color="note" %}}

Data client API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam data client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate a [`DataClient`](https://python.viam.dev/autoapi/viam/app/data_client/index.html#viam.app.data_client.DataClient).

You will also need an API key and API key ID to authenticate your session.
To get an API key (and corresponding ID), you have two options:

- [Create an API key using the Viam app](/cloud/rbac/#add-an-api-key)
- [Create an API key using the Viam CLI](/cli/#create-an-organization-api-key)

The following example instantiates a `ViamClient`, authenticating with an API key, and then instantiates a `DataClient`:

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

Once you have instantiated a `DataClient`, you can run [API methods](#api) against the `DataClient` object (named `data_client` in the examples).

## API

The data client API supports the following methods:

Methods to upload data like images or sensor readings directly to the [Viam app](https://app.viam.com):

{{< readfile "/static/include/app/apis/generated/data_sync-table.md" >}}

Methods to download, filter, tag, or perform other tasks on data like images or sensor readings:

{{< readfile "/static/include/app/apis/generated/data-table.md" >}}

Methods to work with datasets:

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

{{< readfile "/static/include/app/apis/generated/data_sync.md" >}}

{{< readfile "/static/include/app/apis/generated/data.md" >}}

{{< readfile "/static/include/app/apis/generated/dataset.md" >}}

## Find part ID

To copy the ID of your machine part, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**.

For example:

![Part ID displayed in the Viam app.](/build/program/data-client/grab-part-id.png)
