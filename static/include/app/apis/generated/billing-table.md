<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetCurrentMonthUsage`](/reference/apis/billing-client/#getcurrentmonthusage) | Access data usage information for the current billing period for a given organization. |
| [`GetOrgBillingInformation`](/reference/apis/billing-client/#getorgbillinginformation) | Access billing information (payment method, billing tier, etc.) for a given org. |
| [`GetInvoicesSummary`](/reference/apis/billing-client/#getinvoicessummary) | Access total outstanding balance plus invoice summaries for a given organization. |
| [`GetInvoicePDF`](/reference/apis/billing-client/#getinvoicepdf) | Access invoice PDF data and optionally save it to a provided file path. |
| [`CreateInvoiceAndChargeImmediately`](/reference/apis/billing-client/#createinvoiceandchargeimmediately) | Create a flat fee invoice and charge the organization immediately. The caller must be an owner of the organization being charged. This function blocks until payment is confirmed, but will time out after 2 minutes if there is no confirmation. |
| [`ChargeOrganization`](/reference/apis/billing-client/#chargeorganization) | Charge an organization for usage. |
