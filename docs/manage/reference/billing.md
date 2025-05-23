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

The **Payment and billing** page shows you:

- your usage for the current month
- the date for your next invoice
- the payment method on the account
- a cost breakdown for cloud storage, cloud data upload, cloud data egress, remote control, and standard compute costs
- all your monthly invoices

{{< alert title="Note" color="note" >}}

For Pricing information, please see [pricing & billing explained](https://www.viam.com/product/pricing).

{{< /alert >}}

![Payment and billing overview](/billing-overview.png)

## Download an invoice

You can view all your monthly invoices for your organization in the **Invoices** section of the **Payment & Billing** page.
To download an invoice for a month click on **Download (PDF)** next to the relevant month.

## Set billing alerts

You can set alerts to receive an email notification when your monthly spend exceeds a certain threshold.

- Scroll to the bottom of the **Payment & Billing** page.
- Click **Set amount** and enter a monthly threshold.

## Help

For questions about your bill, email [billing@viam.com](mailto:billing@viam.com).
You can expect a response within 1–3 business days.

## Access billing information programmatically

The [billing client API](/dev/reference/apis/billing-client/) supports the following methods to retrieve billing information from the [Viam app](https://app.viam.com):

{{< readfile "/static/include/services/apis/billing-client.md" >}}
