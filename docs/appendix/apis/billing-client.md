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

{{< readfile "/static/include/services/apis/billing-client.md" >}}

### GetCurrentMonthUsage

Access data usage information for the current month for a given organization.
You can also find your usage data on the [**Payment and billing** page](/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- org_id ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the ID of the organization to request usage data for

**Returns:**

- ([viam.proto.app.billing.GetCurrentMonthUsageResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetCurrentMonthUsageResponse)): Current month usage information

```python {class="line-numbers linkable-line-numbers"}
usage = await viam_client.billing_client.get_current_month_usage("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_current_month_usage).

{{% /tab %}}
{{< /tabs >}}

### GetInvoicePdf

Access invoice PDF data and optionally save it to a provided file path.
You can also find your invoices on the [**Payment and billing** page](/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `invoice_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the ID of the invoice being requested
- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the ID of the org to request data from
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): filepath to save the invoice to

**Returns:**

- None.

```python {class="line-numbers linkable-line-numbers"}
await viam_client.billing_client.get_invoice_pdf(
    "<INVOICE-ID>", "<ORG-ID>", "<FILENAME>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_invoice_pdf).

{{% /tab %}}
{{< /tabs >}}

### GetInvoicesSummary

Access total outstanding balance plus invoice summaries for a given org.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- org_id ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): the ID of the org to request data for

**Returns:**

- ([viam.proto.app.billing.GetInvoicesSummaryResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetInvoicesSummaryResponse)): Summary of org invoices

```python {class="line-numbers linkable-line-numbers"}
summary = await viam_client.billing_client.get_invoices_summary("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_invoices_summary).

{{% /tab %}}
{{< /tabs >}}

### GetOrgBillingInformation

Access billing information (payment method, billing tier, etc.) for a given org.
You can also find this information on the [**Payment and billing** page](/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- org_id (str): the ID of the org to request data for

**Returns:**

- ([viam.proto.app.billing.GetOrgBillingInformationResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetOrgBillingInformationResponse)): The org billing information

```python {class="line-numbers linkable-line-numbers"}
information = await viam_client.billing_client.get_org_billing_information(
    "<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_org_billing_information).

{{% /tab %}}
{{< /tabs >}}
