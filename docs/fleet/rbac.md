---
title: "Role-Based Access Control"
linkTitle: "Access Control"
description: "Fleet and data management permissions."
weight: 50
type: "docs"
tags: ["data management", "cloud", "app", "fleet management"]
# SME: Devin Hilly
---

Role-Based Access Control (RBAC) is a way to enforce security in the [Viam app](https://app.viam.com) by assigning organization members roles that confer permissions.
Users can have access to different fleet management capabilities depending on whether they are an owner or an operator of a given {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="robot" text="robot" >}}.

- **Owner**: Can see and edit [every tab on the robot page](/fleet/machines/#navigating-the-robot-page).
  Can manage users in the app.
- **Operator**: Can see and use only the [**Control** tab](/fleet/machines/#control).
  Cannot see or edit the [**Setup**](/fleet/machines/#setup), [**Config**](/fleet/machines/#configuration), [**History**](/fleet/machines/#history), [**Logs**](/fleet/machines/#logs), [**Code sample**](/fleet/machines/#code-sample), or [**Security**](/fleet/machines/#security) tabs.

For more detailed information on the permissions each role confers for different resources, see [Permissions](/fleet/rbac/#permissions).

## Change a user's access

If you have the **Owner** role, you can [invite new users](/fleet/organizations/#invite-users-to-your-organization) and change the roles assigned to an organization member on a per robot, location, or organization level.

To view the roles each organization member has, click on the organization dropdown in the top navigation bar and click on **Settings**.

{{<imgproc src="/fleet/rbac.png" resize="700x" declaredimensions=true alt="Organization page">}}

### Limit access

To limit the access of a user, first open the access settings for the user by clicking on the user.
Then either change the role of the user from owner to operator with the dropdown or click on **Limit access** and change the resource the user has access.

You can also remove the user by clicking on **Remove user**.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/limit-access.png" resize="800x" declaredimensions=true >}}

For more information on the permissions the roles assign for each resource, see [Permissions](/fleet/rbac/#permissions).

### Grant additional access

To grant additional access to a user, first open the access settings for the user by clicking on the user.
Then either change the role of the user from operator to owner with the dropdown or click on **Grant additional access** and change the resource the user has access.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/grant-access.png" resize="800x" declaredimensions=true >}}

For more information on the permissions the roles assign for each resource, see [Permissions](/fleet/rbac/#permissions).

{{< alert title="Note" color="note" >}}
The option to grant additional access is only visible if you can grant the user additional access.
{{< /alert >}}

## Permissions

The following sections describe the permissions for each user role when it comes to managing robots, locations, organizations, fragments, and data.

### Robots

Permissions for managing {{< glossary_tooltip term_id="robot" text="robots" >}} are as follows:

| Permissions                                                   | Org owner | Org operator | Location owner | Location operator | Robot owner | Robot operator |
| ------------------------------------------------------------- | --------- | ------------ | -------------- | ----------------- | ----------- | -------------- |
| Control the robot from the **Control** tab                    | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**     | **Yes**        |
| See all tabs (such as **Config** and **Logs**)                | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Edit robot name                                               | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Delete the robot                                              | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Add a new {{< glossary_tooltip term_id="part" text="part" >}} | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Edit {{< glossary_tooltip term_id="part" text="part" >}} name | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Restart the robot                                             | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Edit a robot config (including data capture and sync)         | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |

### Locations

Permissions for managing {{< glossary_tooltip term_id="location" text="locations" >}} are as follows:

| Permissions                                  | Org owner                                                      | Org operator | Location owner                                                 | Location operator | Robot owner | Robot operator |
| -------------------------------------------- | -------------------------------------------------------------- | ------------ | -------------------------------------------------------------- | ----------------- | ----------- | -------------- |
| Edit location info (rename, delete location) | **Yes**                                                        | No           | **Yes** for this and any child locations                       | No                | No          | No             |
| Create a new robot                           | **Yes**                                                        | No           | **Yes** in this and any child locations                        | No                | No          | No             |
| Move the location (to new parent location)   | **Yes**                                                        | No           | **Yes**, to other locations they have access to                | No                | No          | No             |
| Create a new location in the organization    | **Yes**                                                        | No           | No                                                             | No                | No          | No             |
| Delete location                              | **Yes**                                                        | No           | **Yes**                                                        | No                | No          | No             |
| Add/remove Viam support team permissions     | **Yes**                                                        | No           | **Yes**                                                        | No                | No          | No             |
| Add a shared location                        | **Yes**, if they are an owner in the org they are sharing with | No           | **Yes**, if they are an owner in the org they are sharing with | No                | No          | No             |
| Remove a shared location                     | **Yes**                                                        | No           | **Yes**                                                        | No                | No          | No             |
| Use Try Viam from within the org\*           | **Yes**                                                        | No           | No                                                             | No                | No          | No             |

If a user has access to a child location but not its parent location, the user cannot see robots in the parent location.

\*Users can only use Try Viam from within an organization they own because doing so creates a new location in the org.

### Organization settings and roles

Only {{< glossary_tooltip term_id="organization" text="organization" >}} owners can edit or delete an organization, or see and edit the organization billing page.

Permissions for managing {{< glossary_tooltip term_id="organization" text="organization" >}} settings and user roles are as follows:

| Permissions                                           | Org owner | Org operator | Location owner | Location operator | Robot owner | Robot operator |
| ----------------------------------------------------- | --------- | ------------ | -------------- | ----------------- | ----------- | -------------- |
| See billing page                                      | **Yes**   | No           | No             | No                | No          | No             |
| Get billing-related emails                            | **Yes**   | No           | No             | No                | No          | No             |
| Edit org name                                         | **Yes**   | No           | No             | No                | No          | No             |
| Delete the org                                        | **Yes**   | No           | No             | No                | No          | No             |
| Leave the org                                         | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**     | **Yes**        |
| See their own role                                    | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**     | **Yes**        |
| See other peoples' roles                              | **Yes**   | **Yes**      | **Yes\***      | **Yes\***         | **Yes\***   | **Yes\***      |
| See all org members (including email and date joined) | **Yes**   | **Yes**      |
| Invite, resend invite, and revoke invite              | **Yes**   | No           | **Yes\***      | No                | **Yes\***   | No             |
| Change someone else's role                            | **Yes**   | No           | **Yes\***      | No                | **Yes\***   | No             |
| Create a new organization                             | **Yes**   | **Yes**      | **Yes**        | **Yes**           | **Yes**     | **Yes**        |

\*For locations/robots they have access to

### Fragments

Permissions for managing {{< glossary_tooltip term_id="fragment" text="fragments" >}} are as follows:

| Permissions                                                                             | Org owner | Org operator | Location owner | Location operator | Robot owner | Robot operator |
| --------------------------------------------------------------------------------------- | --------- | ------------ | -------------- | ----------------- | ----------- | -------------- |
| Create a new fragment in the {{< glossary_tooltip term_id="organization" text="org" >}} | **Yes**   | No           | No             | No                | No          | No             |
| See and use fragments in the {{< glossary_tooltip term_id="organization" text="org" >}} | **Yes**   | No           | **Yes**        | No                | **Yes**     | No             |
| Edit and delete fragments                                                               | **Yes**   | No           | No             | No                | No          | No             |

### Data and machine learning

Permissions for [data management](/data/) and [machine learning](/ml/) are as follows:

| Permissions                         | Org owner                                     | Org operator | Location owner                                                      | Location operator | Robot owner                                                         | Robot operator |
| ----------------------------------- | --------------------------------------------- | ------------ | ------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------- | -------------- |
| View data                           | **Yes**                                       | No           | **Yes\***                                                           | No                | **Yes\*\***                                                         | No             |
| See data tags                       | **Yes**                                       | No           | Only tags applied to data they have access to                       | No                | Only tags applied to data they have access to                       | No             |
| Edit data (add tags, delete info)   | **Yes**                                       | No           | **Yes\***                                                           | No                | **Yes\*\***                                                         | No             |
| Train models                        | **Yes**                                       | No           | **Yes** on data they have access to                                 | No                | **Yes** on data they have access to                                 | No             |
| Upload organization models/packages | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No             |
| View organization models/packages   | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No             |
| Use organization models/packages    | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No             |
| Delete organization models/packages | **Yes**                                       | No           | No                                                                  | No                | No                                                                  | No             |
| Export data with the CLI or the app | **Yes**                                       | No           | **Yes\***                                                           | No                | **Yes\*\***                                                         | No             |
| See dataset names                   | Can see all names in current org              | No           | Can see all names in current org                                    | No                | Can see all names in current org                                    | No             |
| Click into datasets / load them     | Can click into dataset and see all data in it | No           | Can see the data in the dataset that they have permission to access | No                | Can see the data in the dataset that they have permission to access | No             |
| Create new dataset                  | **Yes**                                       | No           | **Yes**                                                             | No                | **Yes**                                                             | No             |
| Rename dataset                      | **Yes**                                       | No           | No                                                                  | No                | No                                                                  | No             |
| Delete dataset                      | **Yes**                                       | No           | No                                                                  | No                | No                                                                  | No             |
| Add images to dataset               | **Yes**                                       | No           | Can add images they have permissions on                             | No                | Can add images they have permissions on                             | No             |
| Remove image from dataset           | **Yes**                                       | No           | Can remove images in the dataset that they can see                  | No                | Can remove images in the dataset that they can see                  | No             |
| Train on dataset                    | **Yes**                                       | No           | Trains on the portion of the dataset that they have access to       | No                | Trains on the portion of the dataset that they have access to       | No             |

\*For data from the location

\*\*For data from the robot
