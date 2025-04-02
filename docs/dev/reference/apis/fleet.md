---
title: "Manage Your Fleet with Viam's Fleet Management API"
linkTitle: "Fleet Management"
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

The fleet management API allows you to manage your machine fleet with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).
With it you can

- create and manage organizations, locations, and individual machines
- manage permissions and authorization
- create and manage fragments

{{% alert title="Support Notice" color="note" %}}

Fleet management API methods are only available in the Python SDK.

{{% /alert %}}

The fleet management API supports the following methods:

{{< readfile "/static/include/app/apis/generated/app-table.md" >}}

## Establish a connection

To use the Viam fleet management API, you first need to instantiate a `ViamClient` and then instantiate an `AppClient`.

You will also need an API key and API key ID to authenticate your session.
To get an API key (and corresponding ID), you have two options:

- [Create an API key using the Viam app](/operate/control/api-keys/#add-an-api-key)
- [Create an API key using the Viam CLI](/dev/tools/cli/#create-an-organization-api-key)

The following example instantiates a `ViamClient`, authenticating with an API key, and then instantiates an `AppClient`:

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
        # Replace "<API-KEY>" (including brackets) with your API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your API key
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
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="3,5"}
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

const viamClient = await connect();
const appClient = appClient.appClient;
```

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

{{<imgproc src="/build/program/data-client/grab-part-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Part ID displayed in the Viam app.">}}

## Find machine ID

To copy the ID of your {{< glossary_tooltip term_id="machine" text="machine" >}}, click the **...** (Actions) button in the upper-right corner of your machine's page, then click **Copy machine ID**:

{{<imgproc src="/fleet/app-usage/copy-machine-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Machine ID in the actions dropdown in the Viam app.">}}
