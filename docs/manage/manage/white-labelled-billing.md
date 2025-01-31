---
title: "White-labelled Billing"
linkTitle: "White-labelled Billing"
weight: 70
layout: "docs"
type: "docs"
description: "Set up white-labelled billing."
images: ["/operate/wlbilling.png"]
date: "2025-01-31"
---

You can use Viam to bill your customers using your own logo.
This guide will show you how to set up white-labelled billing.
Once set up:

- You will have a branded billing dashboard for each org
- Invoices will be sent from your provided support email address and will contain your provided logo
- You can set custom pricing

{{<imgproc src="/operate/wlbilling.png" resize="1000x" declaredimensions=true alt="Example billing dashboard" style="width:600px" class="imgzoom">}}

## Prerequisites

{{< table >}}
{{% tablestep %}}
**1. Set organization public namespace**

In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page. Create a **Public namespace**.

{{% /tablestep %}}
{{% tablestep link="/dev/tools/cli/#organizations" %}}
**2. Add your logo**

Add a logo to be displayed on the login screen for your organization.
Your logo can be up to 200KB in size and must be in PNG format.

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organization logo set --logo-path=logo.png --org-id=<org-id>
Successfully set the logo for organization <org-id> to logo at file-path: logo.png
```

You must have [owner permissions](/manage/manage/rbac/#organization-settings-and-roles) on the organization.

{{% /tablestep %}}
{{% tablestep link="/dev/tools/cli/#organizations" %}}
**3. Add support email**

This is the email that will be shown when Viam sends emails to users on your behalf for email verification, password recovery, and other account related emails.

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organization support-email set --support-email=support@logoipsum.com --org-id=<org-id>
Successfully set support email for organization "<org-id>" to "support@logoipsum.com"
```

{{% /tablestep %}}
{{< /table >}}

## Set up custom billing

{{< table >}}
{{% tablestep link="/dev/tools/cli/#organizations" %}}
**1. Enable billing service**

Enable the billing service for your organization:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam organizations billing-service enable --org-id=<org-id> --address="100 Center Street, New York, NY, 10001"
Successfully enabled billing service for organization "<org-id>"
```

{{% /tablestep %}}
{{% tablestep link="/dev/tools/cli/#organizations" %}}
**2. Get billing dashboard URL**

Run the following command to check your billing configuration:

```sh {class="command-line" data-prompt="$" data-output="6-10"}
viam organizations billing-service get-config --org-id="<org-id> "
Billing config for organization: <org-id>
Support Email: npentrel@gmail.com
Billing Dashboard URL: https://app.viam.com/billing/logoipsum
Logo URL: https://storage.googleapis.com/viam-self-service-<org-id>/primary_logo.png

 --- Billing Address ---
Address Line 1: 123 Test Street
City: New York
State: Ny
Postal Code: 10001
Country: USA
```

You can update any value after setup using `viam organizations billing-service update`.

{{% /tablestep %}}
{{% tablestep %}}
**3. Check the billing dashboard**

In the information returned in the previous step, get the billing dashboard URL.
It will be of the form `https://app.viam.com/billing/<public-namespace>`.

To see the billing dashboard for a specific organization, navigate to:

```sh {class="command-line"}
https://app.viam.com/billing/<public-namespace>?id=<org-id>
```

{{<imgproc src="/operate/wlbilling.png" resize="1000x" declaredimensions=true alt="Example billing dashboard" style="width:600px" class="imgzoom">}}

{{% /tablestep %}}
{{< /table >}}

## Set custom pricing

You can set custom pricing for machines within your organization:

{{< table >}}
{{% tablestep link="" %}}
**1. Create a fragment with billing information**

For example:

```json {class="line-numbers linkable-line-numbers" data-line="5"}
{
  "billing": {
    "cost_per_month": {
      "per_machine": 10
    },
    "tier_name": "not-free"
  }
}
```

{{% /tablestep %}}
{{% tablestep link="/manage/fleet/reuse-configuration/" %}}
**2. Add the fragment to each machine**


{{% /tablestep %}}
{{< /table >}}
