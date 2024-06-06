---
title: "Role-Based Access Control"
linkTitle: "Manage Access"
description: "Fleet and data management permissions."
weight: 50
type: "docs"
tags: ["data management", "cloud", "app", "fleet management"]
aliases:
  - /fleet/rbac/
# SME: Devin Hilly
---

Role-Based Access Control (RBAC) is a way to enforce security in the [Viam app](https://app.viam.com) by assigning organization members roles that confer permissions.
Users can have access to different fleet management capabilities depending on whether they are an owner or an operator of a given {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="machine" text="machine" >}}.

- **Owner**: Can see and edit [every tab on the machine page](/cloud/machines/#navigating-the-machine-page).
  Can manage users in the app.
- **Operator**: Can see and use only the [**CONTROL**](/fleet/control/) tab.
  Cannot see or edit the [**CONFIGURE**](/cloud/machines/#configure), [**LOGS**](/cloud/machines/#logs), or **CONNECT** tabs.

For more detailed information on the permissions each role confers for different resources, see [Permissions](/cloud/rbac/#permissions).

## Change a user's access

If you have the **Owner** role, you can [invite new users](/cloud/organizations/#invite-someone-to-an-organization) and change the roles assigned to an organization member on a per machine, location, or organization level.

To view the roles each organization member has, click on the organization dropdown in the top navigation bar and click on **Settings**.

{{<imgproc src="/cloud/rbac.png" resize="700x" declaredimensions=true alt="Organization page">}}

### Limit access

To limit the access of a user, first open the access settings for the user by clicking on the user.
Then either change the role of the user from owner to operator with the dropdown or click on **Limit access** and change the resource the user has access.

You can also remove the user by clicking on **Remove user**.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/limit-access.png" resize="800x" declaredimensions=true >}}

For more information on the permissions the roles assign for each resource, see [Permissions](/cloud/rbac/#permissions).

### Grant additional access

To grant additional access to a user, first open the access settings for the user by clicking on the user.
Then either change the role of the user from operator to owner with the dropdown or click on **Grant additional access** and change the resource the user has access.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/grant-access.png" resize="800x" declaredimensions=true >}}

For more information on the permissions the roles assign for each resource, see [Permissions](/cloud/rbac/#permissions).

{{< alert title="Note" color="note" >}}
The option to grant additional access is only visible if you can grant the user additional access.
{{< /alert >}}

### Use the mobile app

You can also use the [Viam mobile app](/fleet/#the-viam-mobile-app) to grant or revoke organization owner or operator access to users on the go.
Navigate to your organizations on the mobile app by swiping left to right or clicking on the menu in the top left corner.
Click the gear icon associated with the organization where you want to manage access or invite new people.

## API keys

API keys grant access to organizations, locations, and machines.
If at the organization level, they grant access to all locations and machines contained within that organization.
If at the location level, they grant access to all of the machines contained within that location.

To view all API keys in use for your organization and the locations and machines inside it, click on the organization dropdown in the top navigation bar and click on **Settings**.

View a table with each key, ID, name (if assigned), time created, and entities it provides access to:

{{<imgproc src="/fleet/api-keys.png" resize="700x" declaredimensions=true alt="API Keys table">}}

In each row, click the copy icon to copy the API key and key ID.
Click the duplicate icon to duplicate the API key.
Click the trash can icon to delete the API key.

### Add an API key

Click **Generate key** to generate a new key.
Optionally, give the key a name of your choice.
Click on the **Resource** menu and choose what organization, location, or machine you want the key to grant access to.
For **Role**, assign either an **Owner** or **Operator** role.
See [Permissions](#permissions) for information about the privilege each role entails at each resource level.

### View an API key's details

To view the role of an API key and what it grants access to, click on **Show details** in the key's row of the key table's **Resources** column:

{{<imgproc src="/fleet/additional-details.png" resize="700x" declaredimensions=true alt="Additional details for a key">}}

### Change an API key's access

To edit an API key, click on **Show details** in the key's row of the key table's **Resources** column.

To edit the role, click on the dropdown menu next to the role and select **Owner** or **Operator**.
See [Permissions](#permissions) for information about the privilege each role entails at each resource level.

To change the entities it is able to access, click **+ Grant additional access**.
Select which organization, location, or machine you want the key to grant access to.
Click **Choose** to confirm your selection.

## Permissions

The following sections describe the permissions for each user role when it comes to managing machines, locations, organizations, fragments, and data.

### Machines

Permissions for managing {{< glossary_tooltip term_id="machine" text="machines" >}} are as follows:

| Permissions                                                   | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ------------------------------------------------------------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| Control the machine from the **CONTROL** tab                  | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**       | **Yes**          |
| See all tabs (such as **CONFIGURE** and **LOGS**)             | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Edit machine name                                             | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Delete the machine                                            | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Add a new {{< glossary_tooltip term_id="part" text="part" >}} | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Edit {{< glossary_tooltip term_id="part" text="part" >}} name | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Restart the machine                                           | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Edit a machine config (including data capture and sync)       | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |

### Locations

Permissions for managing {{< glossary_tooltip term_id="location" text="locations" >}} are as follows:

| Permissions                                  | Org owner | Org operator | Location owner                                  | Location operator | Machine owner | Machine operator |
| -------------------------------------------- | --------- | ------------ | ----------------------------------------------- | ----------------- | ------------- | ---------------- |
| Edit location info (rename, delete location) | **Yes**   | No           | **Yes** for this and any child locations        | No                | No            | No               |
| Create a new machine                         | **Yes**   | No           | **Yes** in this and any child locations         | No                | No            | No               |
| Move the location (to new parent location)   | **Yes**   | No           | **Yes**, to other locations they have access to | No                | No            | No               |
| Create a new location in the organization    | **Yes**   | No           | No                                              | No                | No            | No               |
| Delete location                              | **Yes**   | No           | **Yes**                                         | No                | No            | No               |
| Add/remove Viam support team permissions     | **Yes**   | No           | **Yes**                                         | No                | No            | No               |
| Add a shared location                        | **Yes**   | No           | **Yes**                                         | No                | No            | No               |
| Remove a shared location                     | **Yes**   | No           | **Yes**                                         | No                | No            | No               |
| Use Try Viam from within the org\*           | **Yes**   | No           | No                                              | No                | No            | No               |

If a user has access to a child location but not its parent location, the user cannot see machines in the parent location.

If a user is an owner of an organization with which a location was shared (that is, a _secondary_ organization owner), that user _can_ share the location with other organizations.

\*Users can only use Try Viam from within an organization they own because doing so creates a new location in the org.

### Organization settings and roles

Only {{< glossary_tooltip term_id="organization" text="organization" >}} owners can edit or delete an organization, or see and edit the organization billing page.

Permissions for managing org settings and user roles are as follows:

| Permissions                                           | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ----------------------------------------------------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| See billing page                                      | **Yes**   | No           | No             | No                | No            | No               |
| Get billing-related emails                            | **Yes**   | No           | No             | No                | No            | No               |
| Edit org name                                         | **Yes**   | No           | No             | No                | No            | No               |
| Delete the org                                        | **Yes**   | No           | No             | No                | No            | No               |
| Leave the org                                         | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**       | **Yes**          |
| See their own role                                    | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**       | **Yes**          |
| See other peoples' roles                              | **Yes**   | **Yes**      | **Yes\***      | **Yes\***         | **Yes\***     | **Yes\***        |
| See all org members (including email and date joined) | **Yes**   | **Yes**      | No             | No                | No            | No               |
| Invite, resend invite, and revoke invite              | **Yes**   | No           | **Yes\***      | No                | **Yes\***     | No               |
| Change someone else's role                            | **Yes**   | No           | **Yes\***      | No                | **Yes\***     | No               |
| Create a new organization                             | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**       | **Yes**          |
| Delete modules                                        | **Yes**   | No           | No             | No                | No            | No               |
| Make public modules private                           | **Yes**   | No           | No             | No                | No            | No               |

\*For locations/machines they have access to

### Fragments

Permissions for managing {{< glossary_tooltip term_id="fragment" text="fragments" >}} are as follows:

| Permissions                                                                             | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| --------------------------------------------------------------------------------------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| Create a new fragment in the {{< glossary_tooltip term_id="organization" text="org" >}} | **Yes**   | No           | No             | No                | No            | No               |
| See and use fragments in the {{< glossary_tooltip term_id="organization" text="org" >}} | **Yes**   | No           | **Yes**        | No                | **Yes**       | No               |
| Edit and delete fragments                                                               | **Yes**   | No           | No             | No                | No            | No               |

### Data and machine learning

Permissions for [data management](/services/data/) and [machine learning](/services/ml/) are as follows:

| Permissions                         | Org owner                                     | Org operator | Location owner                                                      | Location operator | Machine owner                                                       | Machine operator |
| ----------------------------------- | --------------------------------------------- | ------------ | ------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------- | ---------------- |
| View data                           | **Yes**                                       | No           | **Yes\***                                                           | No                | **Yes\*\***                                                         | No               |
| See data tags                       | **Yes**                                       | No           | Only tags applied to data they have access to                       | No                | Only tags applied to data they have access to                       | No               |
| Edit data (add tags, delete info)   | **Yes**                                       | No           | **Yes\***                                                           | No                | **Yes\*\***                                                         | No               |
| Train models                        | **Yes**                                       | No           | **Yes** on data they have access to                                 | No                | **Yes** on data they have access to                                 | No               |
| Upload organization models/packages | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No               |
| View organization models/packages   | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No               |
| Use organization models/packages    | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No               |
| Delete organization models/packages | **Yes**                                       | No           | No                                                                  | No                | No                                                                  | No               |
| Export data with the CLI or the app | **Yes**                                       | No           | **Yes\***                                                           | No                | **Yes\*\***                                                         | No               |
| See dataset names                   | Can see all names in current org              | No           | Can see all names in current org                                    | No                | Can see all names in current org                                    | No               |
| Click into datasets / load them     | Can click into dataset and see all data in it | No           | Can see the data in the dataset that they have permission to access | No                | Can see the data in the dataset that they have permission to access | No               |
| Create new dataset                  | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No               |
| Rename dataset                      | **Yes**                                       | No           | No                                                                  | No                | No                                                                  | No               |
| Delete dataset                      | **Yes**                                       | No           | No                                                                  | No                | No                                                                  | No               |
| Add images to dataset               | **Yes**                                       | No           | Can add images they have permissions on                             | No                | Can add images they have permissions on                             | No               |
| Remove image from dataset           | **Yes**                                       | No           | Can remove images in the dataset that they can see                  | No                | Can remove images in the dataset that they can see                  | No               |
| Train on dataset                    | **Yes**                                       | No           | Trains on the portion of the dataset that they have access to       | No                | Trains on the portion of the dataset that they have access to       | No               |

\*For data from the location

\*\*For data from the machine
