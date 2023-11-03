---
title: "Manage Organizations"
linkTitle: "Organizations"
weight: 30
type: "docs"
description: "An organization is a group of one or more locations that helps you organize and manage access to your fleet."
tags: ["fleet management", "cloud", "app"]
---

An organization is a group of one or more locations that helps you organize your fleet.

An organization is the highest level grouping in the Viam platform, which generally represents a company, or other institution.
You can also use organizations for departments or other entities that can have one or more [locations](/manage/fleet/locations/).
If you are familiar with Google Drive, you can think of an organization as a shared drive.

When you or another user registers for an account with Viam, they become a member of an organization.
If the user was invited to an organization, they become a part of that organization.
If the user registered without invitation, an organization and a {{< glossary_tooltip term_id="location" text="location" >}} is automatically created for the user.

A user can create more organizations at any time.

Any member of an organization can invite new users to that organization.

For example, you may have an account with one organization for your personal robots at home and another organization for the robots at work.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/eb7v6dabCGQ">}}

You organization is shown in the upper right corner of [the Viam app](https://app.viam.com).
If you click on the organization drop down, the app displays your name, email, and a list of organizations you belong to.

{{< imgproc alt="The org drop down showing an example user's name, email, Sign out button, list of organizations, and org settings button." src="/manage/app-usage/my-org.png" resize="400x" declaredimensions=true >}}

If you used an email invite to sign up, you have two organizations to begin with: the organization that invited you and a personal organization for other projects.

Click an organization's name to navigate to its list of locations.

### Create a new organization

To create a new organization, click on the Org's **Settings** in the top right of the navigation bar.
Then enter the name for your new organization in the **New Organization** field in the upper left of the page.

### Invite users to your organization

To invite a user to your organization, click on the Org's **Settings** in the top right of the navigation bar.
In the members section of the page enter their email address, select a role, and click **Invite**.

{{< imgproc alt="The user invitation menu on the Organization settings page." src="/manage/app-usage/invite-user.png" resize="500x" declaredimensions=true >}}

### Create a namespace for your organization

When uploading [custom modules](/modular-resources/) to the Viam registry, you must set a namespace for your organization to associate your module with.

To create a new namespace for your organization, click on the Org's **Settings** in the top right of the navigation bar, then click the **Set a public namespace** button.
Enter a name for your namespace, and then click **Set namespace**.
Consider the following as you chose a namespace:

- A namespace may only contain letters, numbers, and the dash (`-`) character.
- Once set, a namespace _cannot be changed_: choose your namespace carefully!
- You must pick a unique namespace that is not already in use by another organization.
- As you enter your namespace, a message will appear to the right of the text box indicating whether the namespace is available, or whether an invalid character is detected.

{{< imgproc alt="The namespace creation menu on the Organization settings page." src="/manage/app-usage/create-namespace.png" resize="700x" declaredimensions=true >}}

### Delete an organization

To delete an organization, click on the Org's **Settings** in the top right of the navigation bar.
Then click **Delete organization**.

If the organization to delete contains any locations, you must delete them before you can delete the organization.
