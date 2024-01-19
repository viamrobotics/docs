---
title: "Manage Organizations"
linkTitle: "Organizations"
weight: 30
type: "docs"
description: "An organization is a group of one or more locations that helps you organize and manage access to your fleet."
tags: ["fleet management", "cloud", "app"]
aliases:
  - /manage/fleet/organizations/
---

An organization is a group of one or more locations that helps you organize your fleet.

An organization is the highest level grouping in the Viam platform, which generally represents a company, or other institution.
You can also use organizations for departments or other entities that can have one or more [locations](/fleet/locations/).
If you are familiar with Google Drive, you can think of an organization as a shared drive.

{{<imgproc src="/fleet/rbac.png" resize="900x" declaredimensions=true alt="Organization page">}}

When you or another user registers for an account with Viam, they become a member of an organization.
If the user was invited to an organization, they become a part of that organization.
If the user registered without invitation, an organization and a {{< glossary_tooltip term_id="location" text="location" >}} is automatically created for the user.

A user can create more organizations at any time.

Any member of an organization can invite new users to that organization.

For example, you may have an account with one organization for your personal smart machines at home and another organization for the smart machines at work.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/eb7v6dabCGQ">}}

You organization is shown in the upper right corner of [the Viam app](https://app.viam.com).
If you click on the organization dropdown, the app displays your name, email, and a list of organizations you belong to.

{{< imgproc alt="The org dropdown showing an example user's name, email, Sign out button, list of organizations, and org settings button." src="/fleet/app-usage/my-org.png" resize="400x" declaredimensions=true >}}

If you used an email invite to sign up, you have two organizations to begin with: the organization that invited you and a personal organization for other projects.

Click an organization's name to navigate to its list of locations.

### Create a new organization

To create a new organization, click on the Org's **Settings** in the top right of the navigation bar.
Then enter the name for your new organization in the **New Organization** field in the upper left of the page.

### Share an organization

To invite a user to your organization, click on the Org's **Settings** in the top right of the navigation bar.
In the members section of the page, click on **Grant access** and enter their email address.
Then select the resource that you would like to grant the user access to and the designated role and click **Invite**.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/fleet/app-usage/invite-user.png" resize="900x" declaredimensions=true >}}

You can grant a user access to the following resources:

- an {{< glossary_tooltip term_id="organization" text="organization" >}}
- a {{< glossary_tooltip term_id="location" text="location" >}}
- a {{< glossary_tooltip term_id="machine" text="machine" >}}

For more information on the permissions the roles assign for each resource, see [Permissions](/fleet/rbac/#permissions).

### Create a namespace for your organization

When uploading [custom modules](/registry/) to the Viam registry, you must set a namespace for your organization to associate your module with.

To create a new namespace for your organization, click on the Org's **Settings** in the top right of the navigation bar, then click the **Set a public namespace** button.
Enter a name for your namespace, and then click **Set namespace**.
Consider the following as you chose a namespace:

- A namespace may only contain letters, numbers, and the dash (`-`) character.
- Once set, a namespace _cannot be changed_: choose your namespace carefully!
- You must pick a unique namespace that is not already in use by another organization.
- As you enter your namespace, a message will appear to the right of the text box indicating whether the namespace is available, or whether an invalid character is detected.

{{< imgproc alt="The namespace creation menu on the Organization settings page." src="/fleet/app-usage/create-namespace.png" resize="700x" declaredimensions=true >}}

### Leave an organization

To leave an organization, click on the Org's **Settings** in the top right of the navigation bar.
Then click **Leave organization**.

### Delete an organization

To delete an organization, click on the Org's **Settings** in the top right of the navigation bar.
Then click **Delete organization**.

If the organization to delete contains any locations, you must delete them before you can delete the organization.
