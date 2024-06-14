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
  - /appendix/apis/fleet/
  - /build/program/apis/fleet/
---

The fleet management API allows you to [manage your machine fleet](/fleet/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).
With it you can

- create and manage organizations, locations, and individual machines
- manage permissions and authorization
- create and manage fragments

{{% alert title="Support Notice" color="note" %}}

Fleet management API methods are only available in the Python SDK.

{{% /alert %}}

## Establish a connection

To use the Viam fleet management API, you first need to instantiate a [`ViamClient`](https://python.viam.dev/autoapi/viam/app/viam_client/index.html#viam.app.viam_client.ViamClient) and then instantiate an [`AppClient`](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient).
See the following example for reference.

<!-- After sveltekit migration we should also be able to get a key from the UI-->

Use the Viam CLI [to generate an API key to authenticate](/cli/#authenticate).

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
    # Instantiate an AppClient called "fleet"
    # to run fleet management API methods on
    fleet = viam_client.app_client

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

Once you have instantiated an `AppClient`, you can run the following [API methods](#api) against the `AppClient` object (named `fleet` in the examples).

## API

The fleet management API supports the following methods (among [others](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient)):

{{< readfile "/static/include/app/apis/generated/app-table.md" >}}

{{< readfile "/static/include/app/apis/generated/app.md" >}}

## Find part ID

To copy the ID of your machine part, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**.

For example:

![Part ID displayed in the Viam app.](/build/program/data-client/grab-part-id.png)

## Find machine ID

To copy the ID of your {{< glossary_tooltip term_id="machine" text="machine" >}}, click the **...** (Actions) button in the upper-right corner of your machine's page, then click **Copy machine ID**:

![Machine ID in the actions dropdown in the Viam app.](/fleet/app-usage/copy-machine-id.png)
