### GetCurrentMonthUsage

Access data usage information for the current billing period for a given organization.
This method only returns usage for organizations with monthly billing at the end of the month (`"in_arrears": true`).
You can also find your usage data on the [**Payment and billing** page](/manage/reference/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the organization to request usage data for.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.app.billing.GetCurrentMonthUsageResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetCurrentMonthUsageResponse)): the current month usage information.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
usage = await billing_client.get_current_month_usage("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_current_month_usage).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*GetCurrentMonthUsageResponse)](https://pkg.go.dev/go.viam.com/rdk/app#GetCurrentMonthUsageResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#BillingClient.GetCurrentMonthUsage).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `orgId` (string) (required): The organization ID.

**Returns:**

- (Promise<GetCurrentMonthUsageResponse>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const usage = await billing.getCurrentMonthUsage('<organization-id>');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BillingClient.html#getcurrentmonthusage).

{{% /tab %}}
{{< /tabs >}}

### GetOrgBillingInformation

Access billing information (payment method, billing tier, etc.) for a given org.
You can also find this information on the [**Payment and billing** page](/manage/reference/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request data for.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.app.billing.GetOrgBillingInformationResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetOrgBillingInformationResponse)): the org billing information.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
information = await billing_client.get_org_billing_information("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_org_billing_information).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(*GetOrgBillingInformationResponse)](https://pkg.go.dev/go.viam.com/rdk/app#GetOrgBillingInformationResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#BillingClient.GetOrgBillingInformation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `orgId` (string) (required): The organization ID.

**Returns:**

- (Promise<[GetOrgBillingInformationResponse](https://ts.viam.dev/classes/billingApi.GetOrgBillingInformationResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const billingInfo = await billing.getOrgBillingInformation(
  '<organization-id>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BillingClient.html#getorgbillinginformation).

{{% /tab %}}
{{< /tabs >}}

### GetInvoicesSummary

Access total outstanding balance plus invoice summaries for a given organization.
This includes both monthly and annual invoices depending on the organization's billing configuration.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request data for.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.app.billing.GetInvoicesSummaryResponse](https://python.viam.dev/autoapi/viam/proto/app/billing/index.html#viam.proto.app.billing.GetInvoicesSummaryResponse)): the summaries of all org invoices.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
summary = await billing_client.get_invoices_summary("<ORG-ID>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_invoices_summary).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64)
- [([]*InvoiceSummary)](https://pkg.go.dev/go.viam.com/rdk/app#InvoiceSummary)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#BillingClient.GetInvoicesSummary).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `orgId` (string) (required): The organization ID.

**Returns:**

- (Promise<[GetInvoicesSummaryResponse](https://ts.viam.dev/classes/billingApi.GetInvoicesSummaryResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const invoicesSummary = await billing.getInvoicesSummary(
  '<organization-id>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BillingClient.html#getinvoicessummary).

{{% /tab %}}
{{< /tabs >}}

### GetInvoicePDF

Access invoice PDF data and optionally save it to a provided file path.
You can also find your invoices on the [**Payment and billing** page](/manage/reference/billing/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `invoice_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the invoice being requested.
- `org_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the ID of the org to request data from.
- `dest` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the filepath to save the invoice to.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await billing_client.get_invoice_pdf("<INVOICE-ID>", "<ORG-ID>", "invoice.pdf")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.get_invoice_pdf).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id`
- `orgID` [(string)](https://pkg.go.dev/builtin#string)

**Returns:**

- [([]byte)](https://pkg.go.dev/builtin#byte)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/app#BillingClient.GetInvoicePDF).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): The invoice ID.
- `orgId` (string) (required): The organization ID.

**Returns:**

- (Promise<Uint8Array>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const invoicePdf = await billing.getInvoicePdf(
  '<invoice-id>',
  '<organization-id>'
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BillingClient.html#getinvoicepdf).

{{% /tab %}}
{{< /tabs >}}

### CreateInvoiceAndChargeImmediately

Create a flat fee invoice and charge the organization immediately. The caller must be an owner of the organization being charged. This function blocks until payment is confirmed, but will time out after 2 minutes if there is no confirmation.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `org_id_to_charge` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): the organization to charge.
- `amount` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): the amount to charge in dollars.
- `description` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): a short description of the charge to display on the invoice PDF (must be 100 characters or less).
- `org_id_for_branding` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): the organization whose branding to use in the invoice confirmation email.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await billing_client.create_invoice_and_charge_immediately("<ORG-ID-TO-CHARGE>", <AMOUNT>, <DESCRIPTION>, "<ORG-ID-FOR-BRANDING>")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/billing_client/index.html#viam.app.billing_client.BillingClient.create_invoice_and_charge_immediately).

{{% /tab %}}
{{< /tabs >}}
