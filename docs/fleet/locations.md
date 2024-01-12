---
title: "Manage Locations and Sub-locations"
linkTitle: "Locations"
weight: 30
type: "docs"
no_list: true
description: A location is a virtual grouping of machines that allows you to organize machines and manage access to your fleets.
tags: ["fleet management", "cloud", "app"]
aliases:
  - /manage/fleet/locations/
---

In Viam, every machine belongs to a location.
A location is a virtual grouping of machines that allows you to organize machines and manage access.
Generally, a location defines a group of machines that are geographically close to each other.
If you are familiar with Google Drive, you can think of a location as similar to a folder within a shared drive.

For example, an organization called Good Robots Inc has two warehouses across New York and Oregon.
Good Robots Inc can organize its machines into two locations based on their physical presence in a warehouse.

You can also use locations as proxies for environments such as "Production" and "Testing" or other groupings.
Locations do not have to correspond with physical locations.

Each machine you add to Viam belongs to a location.
Each location belongs to an organization.

{{< alert title="Limit" color="note" >}}
You can create up to 500 locations.
{{< /alert >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/eb7v6dabCGQ">}}

### Add a location

When you create a new organization, Viam automatically creates a new location for you.
You can create additional locations by typing a new location name in the **New Location** field in the left side navigation bar on the [**FLEET** page](https://app.viam.com/robots) and clicking **Add**.

Click a location's name to display the list of machines associated with that location.

### Create a sub-location

To create a sub-location you must first create the sub-location as a location and then choose a parent location:

1. Create a location and add at least one machine to it.
2. At the bottom of the location's page, use the **New Parent Location** dropdown to choose a parent location.
3. Click **Change**.

You can nest locations up to three levels deep.

To move a sub-location to the top level of locations, select **Root** from the **New Parent Location** dropdown and then click **Change**.

### Share a location

A location always belongs to the organization it was created in.
Members of the organization have access to all locations in the organization by default.

You can share a location beyond its organization by [sharing a location with an additional organization](#share-a-location-with-an-additional-organization).

#### Share a location with an additional organization

Share your location with another organization you belong to by selecting the organization from the **Add Organization** dropdown menu and clicking **Share**.

![The Add Organization dropdown in the Viam app displays all organizations the user is a member of.](/fleet/app-usage/add-org-drop-down.png)

The location's page lists newly added organization, along with the organization identified as the **primary owner**:

![After adding another org, the Viam app lists it under the orgs that share this location list.](/fleet/app-usage/after-add-org.png)

##### Remove an organization from a shared location

You can remove any organization except the primary owner from the shared list by clicking the **X** to the right of the location in the shared list.

<!-- location keys are going away and we haven't documented the CLI changes yet that allow you to to create a location level secret.
#### Share a location using location secret keys

Grant programmatic access to your location by sharing a location secret key.

You can see the secret keys for a location in the **Location Secret Keys** dropdown:

![The list of secret keys that can grant access to a location displays in the location secret keys dropdown menu of the Viam app.](/fleet/app-usage/location-secret-keys-dropdown.png)

{{< alert title="Caution" color="caution" >}}
Do not share your location secret, part secret, or machine address publicly.
Sharing this information could compromise your system security by allowing unauthorized access to your machine, or to the computer running your machine.
{{< /alert >}}
-->

##### Rotate a secret key

If you ever need to rotate this key, click on the **Generate Key** button to generate a new key.

Viam supports flexible key rotation with up to two keys in use at one time.
After generating a new secret key, update all references to the key in your code as soon as possible and then remove the old key.

#### Share a location with Viam Support

If you request support, you must share your location with the Viam Support team.
To do so, navigate to the location you need support with and click, **Add Viam support**.

Once you have received support, you can remove Viam Support from your location by clicking **Remove Viam support**.

### Delete a location

You can delete a location that is _empty of machines_ by clicking the trash can icon next to the location name at the top of the page for that location.
The icon will not appear if there are any machines in the location.
