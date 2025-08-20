---
title: "Payment and billing"
linkTitle: "Billing"
weight: 50
type: "docs"
description: "An overview of the Payments & Billing page."
tags: ["fleet management", "cloud", "app"]
aliases:
  - /fleet/billing/
  - /billing/
date: "2024-03-13"
no_list: true
# updated: ""  # When the content was last entirely checked
---

{{<imgproc src="/billing-menu.png" resize="400x" declaredimensions=true alt="Payment and billing menu item" class="alignright shadow">}}

To access the **Payment and billing** page, click on the organization name in the top right of the navigation bar and then click on **Payment and billing**.
You must be an [organization owner](/manage/manage/rbac/) to see this page.

The **Payment and billing** page shows you:

- your usage for the current billing period
- the date for your next invoice
- the payment method on the account
- a cost breakdown for cloud storage, cloud data upload, cloud data egress, remote control, and standard compute costs
- all your invoices (monthly or annual depending on your billing configuration)

{{< alert title="Note" color="note" >}}

For Pricing information, please see [pricing & billing explained](https://www.viam.com/product/pricing).

{{< /alert >}}

![Payment and billing overview](/billing-overview.png)

## Add a payment method

1. Click on the organization name in the top right of the navigation bar and then click on **Payment and billing**.
   You must be an [organization owner](https://docs.viam.com/manage/manage/rbac/) to see this page.
1. Under **Payment method**, click **Add payment method**.
1. Fill in the form with your credit card details or a US bank account.

## Change payment method

To replace the credit card details or bank account details used for an organization, you must have access to the organization's billing settings.
Follow these steps:

1. Click on the organization name in the top right of the navigation bar and then click on **Payment and billing**.
   You must be an [organization owner](https://docs.viam.com/manage/manage/rbac/) to see this page.
1. Under **Payment method**, click **Remove payment method**.
1. Confirm the removal when prompted.
1. Under **Payment method**, click **Add payment method**.
1. Fill in the form with your credit card details or a US bank account.

{{< alert title="Caution" color="caution" >}}
Ensure the new payment method is added immediately after removing the old one to avoid any service interruptions.
Organizations without valid payment methods may experience limitations on their services.
{{< /alert >}}

## Download an invoice

You can view all your invoices for your organization:

1. Click on the organization name in the top right of the navigation bar and then click on **Payment and billing**.
   You must be an [organization owner](https://docs.viam.com/manage/manage/rbac/) to see this page.
1. Find the **Invoices** section of the **Payment & Billing** page.
1. Click on **Download (PDF)** next to the relevant billing period.

{{< alert title="Note" color="note" >}}
Invoices may be generated monthly or annually depending on your billing configuration. Organizations using annual billing will receive invoices every 12 months instead of monthly.
{{< /alert >}}

## Set billing alerts

You can set alerts to receive an email notification when your monthly spend exceeds a certain threshold:

1. Click on the organization name in the top right of the navigation bar and then click on **Payment and billing**.
   You must be an [organization owner](https://docs.viam.com/manage/manage/rbac/) to see this page.
1. Scroll to the bottom of the **Payment & Billing** page.
1. Click **Set amount** and enter a monthly threshold amount.

## Receive billing emails at a different email or and email alias

You cannot currently specify an additional email address to receive billing emails at.
You can, however, create an account for the email address and make it part of your organization.

## Help

For questions about your bill, email [billing@viam.com](mailto:billing@viam.com).
You can expect a response within 1–3 business days.

## Access billing information programmatically

The [billing client API](/dev/reference/apis/billing-client/) supports the following methods to retrieve billing information from [Viam](https://app.viam.com):

{{< readfile "/static/include/services/apis/billing-client.md" >}}
