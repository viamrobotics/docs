---
title: "Manage your fleet with Viam's fleet management API"
linkTitle: "Fleet management"
weight: 20
type: "docs"
description: "Use the fleet management API with Viam's client SDKs to manage your machine fleet with code."
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "cloud management",
    "fleet management",
  ]
aliases:
  - /program/apis/fleet/
  - /dev/reference/apis/fleet/
  - /build/program/apis/fleet/
  - /appendix/apis/fleet/
date: "2024-09-20"
# updated: ""  # When the content was last entirely checked
---

The fleet management API allows you to manage your machine fleet with code the same way you can do in the [web UI](https://app.viam.com/).
With it you can

- create and manage organizations, locations, and individual machines
- manage permissions and authorization
- create and manage fragments

The fleet management API supports the following methods:

{{< readfile "/static/include/app/apis/generated/app-table.md" >}}

## Establish a connection

To use the fleet management API, you need to instantiate a `ViamClient` and then instantiate a `AppClient`.

You need an API key and API key ID at least [Machine operator permissions](/manage/manage/rbac/#organization-settings-and-roles) to use the fleet management API.
To get an API key (and corresponding ID), use the [web UI](/operate/control/api-keys/#add-an-api-key)
to the [Viam CLI](/dev/tools/cli/#create-an-organization-api-key).

{{< tabs >}}
{{% tab name="From a client application" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="12,16"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # TODO: Replace "<API-KEY>" (including brackets) with your API key
        payload='<API-KEY>',
      ),
      # TODO: Replace "<API-KEY-ID>" (including brackets) with your API key
      # ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "cloud"
    # to run fleet management API methods on
    cloud = viam_client.app_client

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
  // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
  viamClient, err := app.CreateViamClientWithAPIKey(
    ctx, app.Options{}, "<API-KEY>", "<API-KEY-ID>", logger)
  if err != nil {
    logger.Fatal(err)
  }
  defer viamClient.Close()

  appClient := viamClient.AppClient()
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
const appClient = appClient.appClient;
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{% tab name="From within a Module" %}}

See [Use platform APIs from within a module](/operate/get-started/other-hardware/create-module/platform-apis/).

{{% /tab %}}
{{< /tabs >}}

Once you have instantiated an `AppClient`, you can run the following [API methods](#api) against the `AppClient` object (named `fleet` in the examples).

{{% hiddencontent %}}
To instantiate an `AppClient` from inside a module, you must authenticate using API keys.
You can use the module environment variables `VIAM_API_KEY` and `VIAM_API_KEY_ID` to access credentials.
{{% /hiddencontent %}}

## API

{{< readfile "/static/include/app/apis/generated/app.md" >}}

## Find part ID

To copy the ID of your machine {{< glossary_tooltip term_id="part" text="part" >}}, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**:

{{<imgproc src="/build/program/data-client/grab-part-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Part ID displayed in the web UI.">}}

## Find machine ID

To copy the ID of your {{< glossary_tooltip term_id="machine" text="machine" >}}, click the **...** (Actions) button in the upper-right corner of your machine's page, then click **Copy machine ID**:

{{<imgproc src="/fleet/app-usage/copy-machine-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Machine ID in the actions dropdown in the web UI.">}}
