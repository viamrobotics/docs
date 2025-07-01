---
title: "Retrieve billing information with Viam's billing client API"
linkTitle: "Billing client"
weight: 90
type: "docs"
description: "Use the billing client API to retrieve billing information from Viam."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "robot api"]
aliases:
  - /program/apis/billing-client/
  - /build/program/apis/billing-client/
  - /appendix/apis/billing-client/
date: "2024-09-14"
# updated: ""  # When the content was last entirely checked
---

The billing client API allows you to retrieve billing information from Viam.

{{% alert title="Support Notice" color="note" %}}

Billing client API methods are only available in the Python and TypeScript SDKs.

{{% /alert %}}

The billing client API supports the following methods:

{{< readfile "/static/include/app/apis/generated/billing-table.md" >}}

## Establish a connection

To use the Viam billing client API, you first need to instantiate a `ViamClient` and then instantiate a `BillingClient`.

You will also need an API key and API key ID to authenticate your session.
Your API key needs to have [Org owner permissions](/manage/manage/rbac/#organization-settings-and-roles) to use the billing client API.
To get an API key (and corresponding ID), you have two options:

- [Create an API key in the web UI](/operate/control/api-keys/#add-an-api-key)
- [Create an API key using the Viam CLI](/dev/tools/cli/#create-an-organization-api-key)

The following example instantiates a `ViamClient`, authenticating with an API key, and then instantiates a `BillingClient`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-line="12, 16"}
import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.app.billing_client import BillingClient


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
    # Instantiate a BillingClient to run data client API methods on
    billing_client = viam_client.billing_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers" data-line="3, 5"}
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
const billingClient = viamClient.billingClient;
```

{{% /tab %}}
{{< /tabs >}}

Once you have instantiated a `BillingClient`, you can run [API methods](#api) against the `BillingClient` object (named `billing_client` in the examples).

## API

{{< readfile "/static/include/app/apis/generated/billing.md" >}}
