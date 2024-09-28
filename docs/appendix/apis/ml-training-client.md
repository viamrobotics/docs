---
title: "Work with ML Training Jobs with Viam's ML Training API"
linkTitle: "ML Training Client"
weight: 10
type: "docs"
description: "Use the ML training client API to manage ML training jobs taking place in Viam's cloud app."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "ml model", "ml"]
aliases:
  - /program/apis/ml_training-client/
  - /build/program/apis/ml-training-client/
date: "2024-09-18"
# updated: ""  # When the content was last entirely checked
---

The ML training API allows you to get information about and cancel ML training jobs taking place on the [Viam app](https://app.viam.com).

{{% alert title="Support Notice" color="note" %}}

ML training client API methods are only available in the Python SDK.

{{% /alert %}}

The ML training client API supports the following methods:

{{< readfile "/static/include/app/apis/generated/mltraining-table.md" >}}

## Establish a connection

To use the Viam ML training client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`MLTrainingClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient.ml_training_client).
See the following example for reference.

You can create an [API key](/cloud/rbac/#api-keys) on your settings page.

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
    # Instantiate an MLTrainingClient to run ML training client API methods on
    ml_training_client = viam_client.ml_training_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated an `MLTrainingClient`, you can run the following [API methods](#api) against the `MLTrainingClient` object (named `ml_training_client` in the examples).

## API

{{< readfile "/static/include/app/apis/generated/mltraining.md" >}}
