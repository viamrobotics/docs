---
linkTitle: "Favorite machines"
title: "Favorite machines"
weight: 55
layout: "docs"
type: "docs"
description: "Mark machines as favorites so they are easy to find across organizations, and manage favorites in the Viam app or with the fleet management API."
capabilities: ["fleet-deployment"]
diataxis: how-to
---

Favorite the machines you work with most so you can find them quickly. Favorites belong to your user account and are stored in Viam Cloud, so they follow you across organizations and devices.

## Favorite a machine in the Viam app

On the **Fleet** > **Machines** page, click the star next to a machine to favorite it. Click the star again to remove the favorite. You can also open a machine's **...** (actions) menu and select **Add to favorites** or **Remove from favorites**.

Favorited machines appear at the top of the machines list. You can turn off favorites-first sorting from the list.

## View all your favorites

To see favorites from every organization in one place, go to your user settings and open the **Machine Favorites** tab. The table shows each favorite machine with its organization and whether it is online. Click a machine name to open it.

## Manage favorites with the SDK

Use the fleet management API to manage favorites programmatically:

| Task                | Method                                                                  |
| ------------------- | ----------------------------------------------------------------------- |
| Add a favorite      | [`AddFavoriteMachine`](/reference/apis/fleet/#addfavoritemachine)       |
| Remove a favorite   | [`RemoveFavoriteMachine`](/reference/apis/fleet/#removefavoritemachine) |
| List your favorites | [`ListFavoriteMachines`](/reference/apis/fleet/#listfavoritemachines)   |

`ListFavoriteMachines` returns machines in the order you favorited them, along with the ID of the organization each machine belongs to.

## Limitations

- Favorites belong to a user, so only a signed-in user can manage them. API keys cannot add, remove, or list favorites.
- You can favorite only machines you have permission to view. If you lose access to a machine or it is deleted, it no longer appears in your favorites.
- Favorites are personal. Other members of your organization cannot see them.

## Related pages

- [Fleet management API](/reference/apis/fleet/) for the full API reference
- [Add custom metadata](/fleet/metadata/) for tagging machines with your own data
