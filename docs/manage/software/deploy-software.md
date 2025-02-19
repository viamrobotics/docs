---
linkTitle: "Deploy software"
title: "Deploy software packages to machines (OTA)"
weight: 35
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "Deploy code packages with machine control logic to one or more machines."
languages: []
viamresources: []
platformarea: ["registry", "fleet"]
level: "Intermediate"
date: "2025-02-14"
aliases:
  - /how-tos/deploy-packages/
  - /manage/software/deploy-packages/
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

The following steps show you how to deploy and manage your machine's software over the air (OTA).

For microcontrollers, see [Over-the-air firmware updates](/operate/get-started/other-hardware/micro-module/#over-the-air-updates) for more information.

## Prerequisites

Start by [setting up one machine](/operate/get-started/setup/).
Then, [configure any hardware and software resources](/operate/get-started/supported-hardware/) that you want to use with your machine and drive with your control logic.

## Configure your software

1.  Go to your [machine](#prerequisites) in the [Viam app](https://app.viam.com).
1.  Add drivers for your hardware resources and any other resources you want to use with your control logic.
    For more information, see [Supported hardware](/operate/get-started/supported-hardware/).
1.  If you created a [control logic module](/manage/software/control-logic/), add it to your machine.

    {{<imgproc src="/how-tos/deploy-packages/add-package.png" resize="800x" class="shadow" style="width: 500px" declaredimensions=true alt="Configuration builder UI">}}

## Set the version and update strategy

For each module:

1. Scroll to the module card for your control logic module.
1. Select a **Pinned version type**.

   You can select a specific version or set the machine to always update to the latest major, minor, patch, or pre-release version once new versions are available.
   For more information on these configuration options, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

   {{<imgproc src="/how-tos/deploy-packages/version.png" resize="800x" class="shadow" style="width: 500px" declaredimensions=true alt="Module card UI">}}

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If the module cannot be interrupted, the module will not be upgraded.
{{% /alert %}}

## Create a fragment

Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for using the same configuration on multiple machines.
When deploying or updating software on many machines, you should use fragments to deploy your modules OTA to your machines.
For more detailed information, see [Reuse configuration](/manage/fleet/reuse-configuration/).

1. Navigate to your machine's **CONFIGURE** tab.
1. Switch to **JSON**.
1. Copy the entire raw JSON.
1. Go to [app.viam.com/fragments](https://app.viam.com/fragments).
1. Add a fragment.
1. Paste the copied JSON configuration into it.
1. Set your privacy settings.

   There are three options for this:

   - **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
   - **Private:** No user outside of your organization will be able to view or use this fragment.
   - **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

1. Click **Save**.

## Add the fragment automatically to your machines with provisioning

Provisioning allows you to automatically add fragments to your machines.
See [Provisioning](/manage/fleet/provision/setup/) for more information.

## Add the fragment to your machines manually

You can also add fragments manually to the machines that need it:

1. Navigate to your machine's **CONFIGURE** tab.
1. Click the **+** button.
1. Select **Insert fragment**.

   {{<imgproc src="/how-tos/deploy-packages/insert.png" resize="800x" class="fill alignright imgzoom shadow" style="width: 250px" declaredimensions=true alt="Add fragment">}}

1. Search for your fragment and add it.
1. Click **Save** in the upper right corner of the screen.

{{< alert title="Tip" color="tip" >}}
You can also add multiple fragments to one machine.
{{< /alert >}}
