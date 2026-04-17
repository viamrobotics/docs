---
linkTitle: "Billing"
title: "Billing and payment"
weight: 50
layout: "docs"
type: "docs"
description: "View usage, manage payment methods, download invoices, and set billing alerts for your organization."
aliases:
  - /fleet/billing/
  - /billing/
  - /manage/reference/billing/
  - /reference/account/billing/
---

The billing page shows your organization's current usage, payment method, and invoice history.
You must be an organization owner to access it.

To open the billing page, click the organization name in the top navigation bar and select **Payment and billing**.

## Understand your usage

The billing page displays three sections about your current and upcoming charges:

**Current month usage**: your total charges so far for the current billing period.

**Next invoice**: the date and estimated amount of your next invoice.

**Monthly usage breakdown**: an itemized list of charges by resource type.
Each line shows the resource, the quantity used, and the cost.
Resource types include:

| Category      | Resources                                                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Storage       | Image and video data, tabular/JSON data, recent data, pipeline sink data, packages, config history, logs, ML training logs |
| Compute       | Standard compute, recent data compute, pipeline sink compute                                                               |
| Data transfer | Cloud data upload, cloud data egress, binary data egress, tabular data egress                                              |
| Other         | Remote control sessions, per-machine charges, trigger notifications                                                        |

For pricing details, see [Viam pricing](https://www.viam.com/product/pricing).

## Manage your payment method

The billing page shows the payment method on file: the last four digits and expiration date for a credit card, or the account type and last four digits for a US bank account.

### Add a payment method

1. On the billing page, under **Payment method**, click **Add payment method**.
1. Enter your credit card details or US bank account information.
1. Submit the form.

### Replace a payment method

To replace the payment method on file, remove the existing one and add a new one:

1. Under **Payment method**, click **Remove payment method**.
1. Confirm the removal in the dialog.
1. Click **Add payment method** and enter the new payment details.

Add the new payment method immediately after removing the old one.
Organizations without a valid payment method may experience service limitations.

## View and download invoices

The **Invoices** section lists all invoices for your organization.
Each invoice shows:

| Column    | Description                                                            |
| --------- | ---------------------------------------------------------------------- |
| Date      | The billing period end date                                            |
| Amount    | The total charge for that period                                       |
| Status    | **Paid**, **Overdue**, **Free** (no charge), or **Payment Processing** |
| Paid date | When payment was received                                              |
| Download  | Link to download the invoice as a PDF                                  |

Invoices are generated monthly or annually depending on your billing configuration.

To download an invoice, click **Download (PDF)** next to the billing period you need.

### Overdue invoices

If your organization has an overdue balance, a banner appears at the top of the billing page.
Contact [billing@viam.com](mailto:billing@viam.com) to resolve overdue payments.

## Set billing alerts

You can receive an email notification when your monthly spend exceeds a threshold you set:

1. Scroll to the bottom of the billing page.
1. Click **Set amount**.
1. Enter a monthly threshold in dollars.

When your current month's usage exceeds this amount, you receive an email notification.

## Free credits

If your organization has free trial credits, a banner at the top of the billing page shows the remaining credit amount.
Usage within the credit amount does not require a payment method on file.

## Help

For questions about your bill, email [billing@viam.com](mailto:billing@viam.com).
Expect a response within 1 to 3 business days.

## Programmatic access

You can retrieve billing information programmatically using the [billing client API](/reference/apis/billing-client/).
