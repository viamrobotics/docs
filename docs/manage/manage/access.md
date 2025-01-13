---
linkTitle: "Control access"
title: "Manage Access with Role-Based Access Control"
weight: 20
layout: "docs"
type: "docs"
no_list: true
description: "To collaborate with others on your machines, you can grant users permissions for individual machines or entire locations."
aliases:
  - /cloud/rbac/
  - /fleet/rbac/
---

To collaborate with others on your machines, you can grant users permissions for individual machines or entire locations.
You can use the [Viam app](https://app.viam.com) or the [Viam mobile app](/manage/troubleshoot/teleoperate/default-interface/#viam-mobile-app) to grant or revoke organization owner or operator access to users or API keys.

## Grant access

### Share resources with users

{{< table >}}
{{% tablestep %}}
**1. Navigate to the organization settings page**

You must have the **Owner** role to be able to grant permissions.

In the [Viam app](https://app.viam.com), click on the organization dropdown in the top navigation bar and click on **Settings**.

{{% /tablestep %}}
{{% tablestep %}}
**2. Grant access**

In the **Members** section of the organization settings page you can click on **Grant access** to invite new users to an organization or a location to [share access](/manage/manage/access/) to the machines within it.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/invite-user.png" resize="900x" declaredimensions=true >}}

{{% /tablestep %}}
{{% tablestep link="/manage/manage/rbac/" %}}
**3. Select a resource and role**

Then select the resource that you would like to grant the user access to and the designated role (owner or operator).
Users with owner access to a location or organization, can collaborate on the [machines](/operate/get-started/setup/#what-is-a-machine) within it.

You can grant a user access to the following resources:

- an {{< glossary_tooltip term_id="organization" text="organization" >}}
- a {{< glossary_tooltip term_id="location" text="location" >}}
- a {{< glossary_tooltip term_id="machine" text="machine" >}}

{{<imgproc src="/fleet/app-usage/limit-access.png" resize="1000x" style="width: 600px" class="aligncenter" declaredimensions=true alt="Limit user access">}}

Click **invite**.

{{% /tablestep %}}
{{< /table >}}

### Share a location with an organization

Share your location with another organization you belong to by selecting the organization from the **Add Organization** dropdown menu and clicking **Share**.

To share your location with an organization you are not a member of, select the location or enter the organization ID (a string like `1ab2c3d1-1234-123a-abcd-abcdef123456`) and click **Share**.
Members of the org can find the org ID on their org settings page.

{{% alert title="Note" color="info" %}}

Once you share a _nested_ location (sub-location), its parent location cannot be changed.

{{% /alert %}}

## Limit access

### Limit access for users

{{< table >}}
{{% tablestep %}}
**1. Navigate to the organization settings page**

You must have the **Owner** role to be able to grant permissions.

In the [Viam app](https://app.viam.com), click on the organization dropdown in the top navigation bar and click on **Settings**.

{{% /tablestep %}}
{{% tablestep link="/manage/manage/rbac/" %}}
**2. Limit access**

In the **Members** section of the organization settings page, click on the user to open the access settings for the user.

Then either change the role of the user from owner to operator with the dropdown or click on **Limit access** and change the resource the user has access.

You can also remove the user by clicking on **Remove user**.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/limit-access.png" resize="800x" declaredimensions=true >}}

{{% /tablestep %}}
{{< /table >}}

### Remove an organization from a shared location

You can remove any organization except the primary owner from the shared list by clicking the **X** to the right of the location in the shared list.

## Collaborate safely

When you or your collaborators change the configuration of a machine or a group of machines in the Viam app, `viam-server` automatically synchronizes the configuration and updates the running resources within 15 seconds.
This means everyone who has access can change a fleet's configuration, even while your machines are running.

You can see configuration changes made by yourself or by your collaborators by selecting **History** on the right side of your machine part's card on the **CONFIGURE** tab.
You can also revert to an earlier configuration from the History tab.

{{< alert title="Simultaneous config edits" color="caution" >}}
If you edit a config while someone else edits the same config, the person who saves last will overwrite any prior changes that aren't reflected in the new config.

Before editing a config, we recommend you refresh the page to ensure you have all the latest changes.
{{< /alert >}}

Machine [configuration](/operate/get-started/supported-hardware/) and machine [code](/dev/reference/sdks/) is intentionally kept separate, allowing you to keep track of versioning and debug issues separately.
