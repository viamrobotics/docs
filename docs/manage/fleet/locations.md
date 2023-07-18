---
title: "Manage Locations and Sub-locations"
linkTitle: "Locations"
weight: 30
type: "docs"
no_list: true
description: A location is a virtual grouping of robots that allows you to organize robots and manage access to your fleets.
tags: ["fleet management", "cloud", "app"]
---

In Viam, every robot belongs to a location.
A location is a virtual grouping of robots that allows you to organize robots and manage access.
Generally, a location defines a group of robots that are geographically close to each other.
If you are familiar with Google Drive, you can think of a location as similar to a folder within a shared drive.

For example, an organization called Good Robots Inc has two warehouses across New York and Oregon.
Good Robots Inc can organize its robots into two locations based on their physical presence in a warehouse.

You can also use locations as proxies for environments such as "Production" and "Testing" or other groupings.
Locations do not have to correspond with physical locations.

Each robot you add to Viam belongs to a location.
Each location belongs to an organization.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/eb7v6dabCGQ">}}

### Add a location

When you create a new organization, Viam automatically creates a new location for you.
You can create additional locations by typing a new location name in the **New Location** field in the left side navigation bar on the [**FLEET** page](https://app.viam.com/robots) and clicking **Add**.

Click a location's name to display the list of robots associated with that location.

### Create a sub-location

To create a sub-location you must first create the sub-location as a location and then choose a parent location:

1. Create a location and add at least one robot to it.
2. At the bottom of the location's page, use the **New Parent Location** drop-down to choose a parent location.
3. Click **Change**.

You can nest locations up to three levels deep.

To move a sub-location to the top level of locations, select **Root** from the **New Parent Location** drop-down and then click **Change**.

### Share a location

A location always belongs to the organization it was created in.
Members of the organization have access to all locations in the organization by default.

There are two ways to share a location beyond its organization:

- [Share a location with an additional organization](#share-a-location-with-an-additional-organization)
- [Share a location using location secret keys](#share-a-location-using-location-secret-keys)

#### Share a location with an additional organization

Share your location with another organization you belong to by selecting the organization from the **Add Organization** drop-down menu and clicking **Share**.

![The Add Organization drop-down in the Viam app displays all organizations the user is a member of.](/manage/app-usage/add-org-drop-down.png)

The location's page lists newly added organization, along with the organization identified as the **primary owner**:

![After adding another org, the Viam app lists it under the orgs that share this location list.](/manage/app-usage/after-add-org.png)

##### Remove an organization from a shared location

You can remove any organization except the primary owner from the shared list by clicking the **X** to the right of the location in the shared list.

#### Share a location using location secret keys

Grant programmatic access to your location by sharing a location secret key.

You can see the secret keys for a location in the **Location Secret Keys** drop-down:

![Screenshot of the list of secret keys that can grant access to a location displays in the location secret keys drop down menu of the Viam app.](/manage/app-usage/location-secret-keys-drop-down.png)

Copy the location secret key by clicking on the clipboard icon.
Use these keys in your SDK code and scripts to authenticate your access to the robots in your location in the cloud.

{{% snippet "secret-share.md" %}}

##### Rotate a secret key

If you ever need to rotate this key, click on the **Generate Key** button to generate a new key.

Viam supports flexible key rotation with up to two keys in use at one time.
After generating a new secret key, update all references to the key in your code as soon as possible and then remove the old key.

#### Share a location with Viam Support

If you request support, you must share your location with the Viam Support team.
To do so, navigate to the location you need support with and click, **Add Viam support**.

Once you have received support, you can remove Viam Support from your location by clicking **Remove Viam support**.

### Delete a location

You can delete a location that is *empty of robots* by clicking the trash can icon next to the location name at the top of the page for that location.
The icon will not appear if there are any robots in the location.
