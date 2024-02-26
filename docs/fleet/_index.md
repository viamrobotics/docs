---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 430
type: "docs"
description: "Configure, control, debug, and manage your machines from the cloud at app.viam.com on your own or with a team."
tags: ["fleet management", "cloud", "app"]
images: ["/platform/fleet.svg"]
no_list: true
aliases:
  - "/manage/fleet-management"
  - "/manage/app-usage"
  - "/product-overviews/fleet-management/"
  - "/fleet/"
  - /manage/fleet/
  - /manage/
menuindent: true
---

Viam fleet management allows you to organize, manage, and control any number of machines alone or in collaboration with others.
You can manage and control your fleet of {{< glossary_tooltip term_id="machine" text="smart machines" >}} from the [Viam app](https://app.viam.com), using the [CLI](/fleet/cli/), or using the [cloud API](/build/program/apis/fleet/).

## Work with groups of machines

To organize your fleet you use

- {{< glossary_tooltip term_id="organization" text="organizations" >}}: the highest level grouping, generally used for different companies.
- {{< glossary_tooltip term_id="location" text="locations" >}}: virtual groupings of devices up with up to three levels of nesting that can represent a grouping of machines that are co-located in a building, like a factory, or a grouping of machines that are thousands of miles apart and are grouped together by function or as an organizational unit.
- {{< glossary_tooltip term_id="machine" text="smart machines" >}}: a grouping of {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} across one {{< glossary_tooltip term_id="part" text="part" >}}, or multiple parts working closely together to complete tasks.
  Each machine resides in a location.

<!-- TODO: Add topology based on Jon's draft -->

![An image of two locations, New York, and Chicago, in one organization, Good Robots](/fleet/locations.png)

The organization structure enables you to:

- configure groups of machines with reusable {{< glossary_tooltip term_id="fragment" text="fragments" >}} that [configure](/build/configure/) a set of resources for each machine that uses the fragment.
- deploy [code packages](/registry/) or [machine learning models](/ml/), without manually copying files by uploading it to Viam's cloud and deploying it to your fleet
- control a machine with code, the app's [**Control** tab](machines/#control), or the [Viam mobile app](#the-viam-mobile-app)
- obtain health metrics, such as status, uptime, version, or [logs](machines/#logs)
- perform debugging

All of this is possible when you are close to your machine, as well as remotely from anywhere in the world.

## Use Viam for collaboration

When you create a Viam account, Viam automatically creates an organization for you.
You can use this organization as your collaboration hub by inviting collaborators to your organization.
You can also add additional organizations as desired at any time.

To facilitate collaboration, you can grant individual collaborators or entire organizations granular permissions for individual machines or entire locations.
This allows you flexibility to manage internal machines, sell devices to external customers and keep managing them, and collaborate with different partners or companies on groups of machines.
For more information, see [Permissions](/fleet/rbac/#permissions).

### Configuration

When you or your collaborators change the configuration of a machine or a group of machines in the Viam app, `viam-server` automatically synchronizes the configuration and updates the running resources within 15 seconds.
This means everyone who has access can change a fleet's [configuration](machines/#configuration), even while your machines are running.

You can see configuration changes made by yourself or by your collaborators on the [History tab](machines/#history).
You can also revert to an earlier configuration from the History tab.

{{< alert title="Simultaneous config edits" color="caution" >}}
If you edit a config while someone else edits the same config, the person who saves last will overwrite any prior changes that aren't reflected in the new config.

Before editing a config, we recommend you refresh the page to ensure you have all the latest changes.
{{< /alert >}}

Machine [configuration](machines/#configuration) and machine [code](/build/program/) is intentionally kept separate, allowing you to keep track of versioning and debug issues separately.

## The Viam mobile app

{{<gif webm_src="/manage/mobile-app-octagon.webm" mp4_src="/manage/mobile-app-octagon.mp4" alt="GIF of red button being pressed and cannon of confetti bot spraying confetti" class="alignright" max-width="200px">}}

<br>

In addition to the [Viam app](https://app.viam.com), the fully featured web application where you can access all fleet management tools, there is a Viam mobile app.
The mobile app is a convenient way to see if your machine is online, access the [control interface](/fleet/machines/#control), [invite people to collaborate with you and modify access](/fleet/rbac/#use-the-mobile-app), check machine [logs](/fleet/machines/#logs), and [upload images to the cloud](/data/upload/#upload-images-with-the-viam-mobile-app).

You can find the mobile app on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

<a href="https://apps.apple.com/vn/app/viam-robotics/id6451424162" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/a470b65d-1b97-412f-9f97-daf902f2f053" width="200px" alt="apple store icon" class="center-if-small" >
</a>

<a href="https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/6ebd6960-08c5-41d4-81f9-42293fbfdfd4" width="200px" alt="google play store icon" class="center-if-small" >
</a>
