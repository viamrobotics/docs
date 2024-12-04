---
title: "Role-Based Access Control"
linkTitle: "Permissions"
description: "Fleet and data management permissions."
weight: 30
type: "docs"
tags: ["data management", "cloud", "app", "fleet management"]
aliases:
  - /fleet/rbac/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
# SME: Devin Hilly
---

Role-Based Access Control (RBAC) is a way to enforce security in the [Viam app](https://app.viam.com) by assigning organization members or API keys roles that confer permissions.
You can assign an owner or an operator role for an {{< glossary_tooltip term_id="organization" text="organization" >}}, {{< glossary_tooltip term_id="location" text="location" >}}, or {{< glossary_tooltip term_id="machine" text="machine" >}}.

- **Owner**: Can see and edit [every tab on the machine page](/cloud/machines/#navigating-the-machine-page) and perform equivalent operations from the APIs.
- **Operator**: Can see and use only the [**CONTROL**](/fleet/control/) tab and perform equivalent operations from the APIs.
  Cannot see or edit the [**CONFIGURE**](/cloud/machines/#configure), [**LOGS**](/cloud/machines/#logs), or **CONNECT** tabs.

The following sections describe the permissions for each user role when it comes to managing machines, locations, organizations, fragments, and data.

## Machines

Permissions for managing {{< glossary_tooltip term_id="machine" text="machines" >}} are as follows:

<!-- prettier-ignore -->
| Permissions | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ----------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| Control the machine from the **CONTROL** tab | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |
| See all tabs (such as **CONFIGURE** and **LOGS**) | **Yes** | No | **Yes** | No | **Yes** | No |
| Edit machine name | **Yes** | No | **Yes** | No | **Yes** | No |
| Delete the machine | **Yes** | No | **Yes** | No | **Yes** | No |
| Add a new {{< glossary_tooltip term_id="part" text="part" >}} | **Yes** | No | **Yes** | No | **Yes** | No |
| Edit {{< glossary_tooltip term_id="part" text="part" >}} name | **Yes** | No | **Yes** | No | **Yes** | No |
| Restart the machine | **Yes** | No | **Yes** | No | **Yes** | No |
| Edit a machine config (including data capture and sync) | **Yes** | No | **Yes** | No | **Yes** | No |

## Locations

Permissions for managing {{< glossary_tooltip term_id="location" text="locations" >}} are as follows:

<!-- prettier-ignore -->
| Permissions | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ----------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| Edit location info (rename, delete location) | **Yes** | No | **Yes** for this and any child locations | No | No | No |
| Create a new machine | **Yes** | No | **Yes** in this and any child locations | No | No | No |
| Move the location (to new parent location) | **Yes** | No | **Yes**, to other locations they have access to | No | No | No |
| Create a new location in the organization | **Yes** | No | No | No | No | No |
| Delete location | **Yes** | No | **Yes** | No | No | No |
| Add/remove Viam support team permissions | **Yes** | No | **Yes** | No | No | No |
| Add a shared location | **Yes** | No | **Yes** | No | No | No |
| Remove a shared location | **Yes** | No | **Yes** | No | No | No |
| Use Try Viam from within the org\* | **Yes** | No | No | No | No | No |

If a user has access to a child location but not its parent location, the user cannot see machines in the parent location.

If a user is an owner of an organization with which a location was shared (that is, a _secondary_ organization owner), that user _can_ share the location with other organizations.

\*Users can only use Try Viam from within an organization they own because doing so creates a new location in the org.

## Organization settings and roles

Only {{< glossary_tooltip term_id="organization" text="organization" >}} owners can edit or delete an organization, or see and edit the organization billing page.

Permissions for managing org settings and user roles are as follows:

<!-- prettier-ignore -->
| Permissions | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ----------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| See billing page | **Yes** | No | No | No | No | No |
| Get billing-related emails | **Yes** | No | No | No | No | No |
| Edit org name | **Yes** | No | No | No | No | No |
| Delete the org | **Yes** | No | No | No | No | No |
| Leave the org | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |
| See their own role | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |
| See other peoples' roles | **Yes** | **Yes** | **Yes\*** | **Yes\*** | **Yes\*** | **Yes\*** |
| See all org members (including email and date joined) | **Yes** | **Yes** | No | No | No | No |
| Invite, resend invite, and revoke invite | **Yes** | No | **Yes\*** | No | **Yes\*** | No |
| Change someone else's role | **Yes** | No | **Yes\*** | No | **Yes\*** | No |
| Create a new organization | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |
| Delete modules | **Yes** | No | No | No | No | No |
| Make public modules private | **Yes** | No | No | No | No | No |

\*For locations/machines they have access to

## Fragments

Permissions for managing {{< glossary_tooltip term_id="fragment" text="fragments" >}} are as follows:

<!-- prettier-ignore -->
| Permissions | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ----------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| Create a new fragment in the {{< glossary_tooltip term_id="organization" text="org" >}} | **Yes** | No | No | No | No | No |
| See and use fragments in the {{< glossary_tooltip term_id="organization" text="org" >}} | **Yes** | No | **Yes** | No | **Yes** | No |
| Edit and delete fragments | **Yes** | No | No | No | No | No |

## Data and machine learning

Permissions for [data management](/fleet/data-management/) and [machine learning](/services/ml/) are as follows:

<!-- prettier-ignore -->
| Permissions | Org owner | Org operator | Location owner | Location operator | Machine owner | Machine operator |
| ----------- | --------- | ------------ | -------------- | ----------------- | ------------- | ---------------- |
| View data | **Yes** | **Yes** | **Yes\*** | **Yes\*** | **Yes\*\*** | **Yes\*\*** |
| See data tags | **Yes** | No | Only tags applied to data they have access to | No | Only tags applied to data they have access to | No |
| Edit data (add tags, delete info) | **Yes** | No | **Yes\*** | No | **Yes\*\*** | No |
| Train models | **Yes** | No | **Yes** on data they have access to | No | **Yes** on data they have access to | No |
| Upload organization models/packages | **Yes** | No | **Yes** | No | **Yes** | No |
| View organization models/packages | **Yes** | No | **Yes** | No | **Yes** | No |
| Use organization models/packages | **Yes** | No | **Yes** | No | **Yes** | No |
| Delete organization models/packages | **Yes** | No | No | No | No | No |
| Export data with the CLI or the app | **Yes** | **Yes** | **Yes\*** | **Yes\*** | **Yes\*\*** | **Yes\*\*** |
| See dataset names | Can see all names in current org | No | Can see all names in current org | No | Can see all names in current org | No |
| Click into datasets / load them | Can click into dataset and see all data in it | No | Can see the data in the dataset that they have permission to access | No | Can see the data in the dataset that they have permission to access | No |
| Create new dataset | **Yes** | No | **Yes** | No | **Yes** | No |
| Rename dataset | **Yes** | No | No | No | No | No |
| Delete dataset | **Yes** | No | No | No | No | No |
| Add images to dataset | **Yes** | No | Can add images they have permissions on | No | Can add images they have permissions on | No |
| Remove image from dataset | **Yes** | No | Can remove images in the dataset that they can see | No | Can remove images in the dataset that they can see | No |
| Train on dataset | **Yes** | No | Trains on the portion of the dataset that they have access to | No | Trains on the portion of the dataset that they have access to | No |

\*For data from the location

\*\*For data from the machine
