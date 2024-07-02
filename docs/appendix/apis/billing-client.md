---
title: "Retrieve billing information with Viam's Billing Client API"
linkTitle: "Billing Client"
weight: 90
type: "docs"
description: "Use the billing client API to retrieve billing information from the Viam app."
tags: ["cloud", "sdk", "viam-server", "networking", "apis", "robot api"]
aliases:
  - /program/apis/billing-client/
  - /build/program/apis/billing-client/
---

The billing client API allows you to retrieve billing information from the [Viam app](https://app.viam.com).

{{% alert title="Support Notice" color="note" %}}

Billing client API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam billing client API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate a [`BillingClient`](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient).

You will also need an API key and API key ID to authenticate your session.
Your API key needs to have [Org owner permissions](/cloud/rbac/#organization-settings-and-roles) to use the billing client API.
To get an API key (and corresponding ID), you have two options:

- [Create an API key using the Viam app](/cloud/rbac/#add-an-api-key)
- [Create an API key using the Viam CLI](/cli/#create-an-organization-api-key)

The following example instantiates a `ViamClient`, authenticating with an API key, and then instantiates a `BillingClient`:

```python {class="line-numbers linkable-line-numbers"}
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

Once you have instantiated a `BillingClient`, you can run [API methods](#api) against the `BillingClient` object (named `billing_client` in the examples).

## API

The billing client API supports the following methods:

{{< readfile "/static/include/app/apis/generated/billing-table.md" >}}

{{< readfile "/static/include/app/apis/generated/billing.md" >}}
