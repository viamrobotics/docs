---
title: "Work with ML training jobs with Viam's ML training API"
linkTitle: "ML training client"
weight: 10
type: "docs"
description: "Use the ML training client API to manage ML training jobs taking place in Viam's cloud app."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "ml model", "ml"]
aliases:
  - /program/apis/ml_training-client/
  - /build/program/apis/ml-training-client/
  - /appendix/apis/ml-training-client/
date: "2024-09-16"
# updated: ""  # When the content was last entirely checked
---

The ML training API allows you to get information about and cancel ML training jobs running on Viam.

The ML training client API supports the following methods:

{{< readfile "/static/include/app/apis/generated/mltraining-table.md" >}}

## Establish a connection

To use the ML training client API, you need to instantiate a `ViamClient` and then instantiate an `MLTrainingClient`.

You need an API key and API key ID with [Org owner permissions](/manage/manage/rbac/#organization-settings-and-roles) to use the MLTraining client API.
To get an API key (and corresponding ID), use the [web UI](/operate/control/api-keys/#add-an-api-key)
to the [Viam CLI](/dev/tools/cli/#create-an-organization-api-key).

{{< tabs >}}
{{% tab name="From a client application" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="12, 16"}
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
    # Instantiate an MLTrainingClient to run ML training client API methods on
    ml_training_client = viam_client.ml_training_client

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

  mlTrainingClient := viamClient.MLTrainingClient()
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="3, 5"}
async function connect(): Promise<VIAM.ViamClient> {
  // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
  // API key ID
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
const mlTrainingClient = viamClient.mlTrainingClient;
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{% tab name="From within a Module" %}}

See [Use platform APIs from within a module](/operate/modules/other-hardware/create-module/platform-apis/).

{{% /tab %}}
{{< /tabs >}}

Once you have instantiated an `MLTrainingClient`, you can run the following [API methods](#api) against the `MLTrainingClient` object (named `ml_training_client` in the examples).

## API

{{< readfile "/static/include/app/apis/generated/mltraining.md" >}}
