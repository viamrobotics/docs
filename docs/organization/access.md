---
linkTitle: "Control access"
title: "Manage access with role-based access control"
weight: 10
layout: "docs"
type: "docs"
no_list: true
description: "To collaborate with others on your machines, you can grant users permissions for individual machines or entire locations."
aliases:
  - /operate/control/api-keys/
  - /cloud/rbac/
  - /fleet/rbac/
  - /manage/manage/access/
---

To collaborate with others on your machines, you can grant users permissions for individual machines or entire locations.
You can use the [web UI](https://app.viam.com) or the Viam mobile app to grant or revoke organization owner or operator access to users or API keys.

For an overview of the resource hierarchy and how permissions work at each level, see [Organizations, locations, and access](/organization/overview/).
For details on what each role can do, see [Permissions](/organization/rbac/).

## Grant access

### Share resources with users

You must have the **Owner** role to be able to grant permissions.

1. On Viam, click on the organization dropdown in the top navigation bar.
2. Click on **Settings**.
3. Find the **Members** section of the organization settings page.
4. Click on **Grant access**.
5. Enter a user's **Email** address.

   {{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/invite-user.png" resize="700x" declaredimensions=true class="shadow" >}}

6. Select an {{< glossary_tooltip term_id="organization" text="organization" >}}, a {{< glossary_tooltip term_id="location" text="location" >}}, or a {{< glossary_tooltip term_id="machine" text="machine" >}} as the **Entity** to share.

   Users with access to a location or organization can collaborate on the machines within it.

7. Select a role to assign to the user.

   For more information on roles and the permissions they provide, see [Manage access with Role-Based Access Control](/organization/rbac/).

8. Click **invite**.

   {{<imgproc src="/fleet/app-usage/limit-access.png" resize="1000x" style="width: 600px" class="shadow" declaredimensions=true alt="Limit user access">}}

### Share a location with an organization

You must have the **Owner** role to be able to share locations.

1. On Viam, click on the organization dropdown in the top navigation bar.
1. Select the organization that contains the location you want to share.
1. Navigate to the location you want to share.
1. Find the **Members & Sharing** section of the location page.
1. Click **Add organization**.
1. Select an organization you have access to in the dropdown or specify an organization ID (a string like `1ab2c3d1-1234-123a-abcd-abcdef123456`).
   Members of the org can find the organization ID on their organization settings page.
1. Click **Grant access**.

{{< alert title="Note" color="note" >}}
Once you share a _nested_ location (sub-location), its parent location cannot be changed.
{{< /alert >}}

## Limit access

### Limit access for users

You must have the **Owner** role to be able to limit permissions.

1. On Viam, click on the organization dropdown in the top navigation bar.
2. Click on **Settings**.
3. Find the **Members** section of the organization settings page.
4. Click on the user to open the access settings for the user.
5. Either change the role of the user from owner to operator with the dropdown or click on **Limit access** and change the resource the user has [access](/organization/rbac/).
   You can also remove the user by clicking on **Remove user**.
   {{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/limit-access.png" resize="800x" declaredimensions=true class="shadow" >}}

### Remove an organization from a shared location

You must have the **Owner** role to be able to share locations.

1. On [Viam](https://app.viam.com), click on the organization dropdown in the top navigation bar.
2. Select the organization that contains the location you want to share.
3. Navigate to the location you want to unshare.
4. Find the **Members & Sharing** section of the location page.
5. Click the **X** to the right of the organization you want to remove.
6. Click **Remove**.

## Manage API key access

You can also grant access through [API keys](/organization/api-keys/) scoped to an organization, location, or machine.
API keys are useful for programmatic access from SDK scripts, CI/CD pipelines, and automated workflows.

See [Manage API keys](/organization/api-keys/) for instructions on creating, rotating, and revoking API keys.

## Collaborate safely

When you or your collaborators change the configuration of a machine or a group of machines, `viam-server` automatically synchronizes the configuration and updates the running resources within 15 seconds.
This means everyone who has access can change a fleet's configuration, even while your machines are running.

You can see configuration changes made by yourself or by your collaborators by selecting **History** on the right side of your machine part's card on the **CONFIGURE** tab.
You can also revert to an earlier configuration from the History tab.

{{% hiddencontent %}}
If someone updates the configuration and saves it while you are editing, Viam will show you a warning that your configuration is out of date when you try to save.
{{% /hiddencontent %}}

Machine [configuration](/hardware/configure-hardware/) and machine [code](/reference/sdks/) is intentionally kept separate, allowing you to keep track of versioning and debug issues separately.
