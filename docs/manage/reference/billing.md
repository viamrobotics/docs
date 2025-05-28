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

## Replace credit card payment method

To replace the credit card payment method for an organization, the billing person must have access to the organization's billing settings. Follow these steps:

### 1. Create an account

If the billing person doesn't already have a Viam account:

1. Go to [app.viam.com](https://app.viam.com)
2. Create a new account using the billing person's email address

### 2. Request access to the organization

The billing person needs to be granted access to the organization that requires the payment method change:

1. An existing organization owner should navigate to the organization settings:
   - Click on the organization dropdown in the top right corner
   - Select **Settings**
2. In the **Members** section, click **Grant access**
3. Enter the billing person's email address
4. Select the organization as the **Entity** to share
5. Assign the **Owner** role (required for billing access)
6. Click **Invite**

Alternatively, the billing person can request an invite by providing their email address to an existing organization owner.

### 3. Access payment and billing settings

Once the billing person has organization access:

1. Log in to [app.viam.com](https://app.viam.com)
2. Click on the organization dropdown in the top right corner
3. Select **Payment and billing**

### 4. Remove existing payment method

1. On the **Payment and billing** page, locate the current payment method
2. Click **Remove payment method**
3. Confirm the removal when prompted

### 5. Add new payment method

1. Click **Add payment method**
2. Enter the new credit card information:
   - Card number
   - Expiration date
   - CVV/CVC code
   - Billing address
3. Click **Save** or **Add payment method** to complete the process

{{< alert title="Important" color="caution" >}}
Ensure the new payment method is added immediately after removing the old one to avoid any service interruptions. Organizations without valid payment methods may experience limitations on their services.
{{< /alert >}}

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
