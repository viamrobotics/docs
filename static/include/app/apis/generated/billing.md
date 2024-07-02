### GetCurrentMonthUsage

Access data usage information for the current month for a given organization.
You can also find your usage data on the [**Payment and billing** page](/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the organization to request usage data for.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.app.billing.GetCurrentMonthUsageResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetCurrentMonthUsageResponse)): Current month usage information.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
usage = await viam_client.billing_client.get_current_month_usage("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_current_month_usage).

{{% /tab %}}
{{< /tabs >}}

### GetOrgBillingInformation

Access billing information (payment method, billing tier, etc.) for a given org.
You can also find this information on the [**Payment and billing** page](/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request data for.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.app.billing.GetOrgBillingInformationResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetOrgBillingInformationResponse)): The org billing information.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
information = await viam_client.billing_client.get_org_billing_information("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_org_billing_information).

{{% /tab %}}
{{< /tabs >}}

### GetInvoicesSummary

Access total outstanding balance plus invoice summaries for a given org.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request data for.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.app.billing.GetInvoicesSummaryResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetInvoicesSummaryResponse)): Summary of org invoices.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
summary = await viam_client.billing_client.get_invoices_summary("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_invoices_summary).

{{% /tab %}}
{{< /tabs >}}

### GetInvoicePdf

Access invoice PDF data and optionally save it to a provided file path.
You can also find your invoices on the [**Payment and billing** page](/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `invoice_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the invoice being requested.
- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request data from.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): filepath to save the invoice to.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await viam_client.billing_client.get_invoice_pdf("<INVOICE-ID>", "<ORG-ID>", "<FILENAME>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_invoice_pdf).

{{% /tab %}}
{{< /tabs >}}
