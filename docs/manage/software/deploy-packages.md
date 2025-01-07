---
linkTitle: "Deploy packages"
title: "Deploy software packages to machines (OTA)"
weight: 30
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: You can use a fragment to deploy software packages and ML models to many machines, as well as to update deployed versions of those software packages and ML models.
languages: []
viamresources: []
platformarea: ["registry", "fleet"]
level: "Intermediate"
date: "2024-08-28"
aliases:
  - /how-tos/deploy-packages/
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for using the same configuration on multiple machines.
You can use a fragment to deploy software packages and ML models to many machines, as well as to update deployed versions of those software packages and ML models.

For example, you can configure a fragment with one resource, like a speech detection service.
Add the fragment to all machines that need the speech detection service.
As you improve the speech detection service, you can specify the version to deploy and all machines will reconfigure themselves to use the version specified in the update.

## Create a fragment

{{< table >}}
{{% tablestep link="/operate/get-started/supported-hardware/" %}}
**1. Configure your software**

Start by adding a new machine in the [Viam app](https://app.viam.com).
You do not need to follow the setup instructions.

Use the **CONFIGURE** tab to add the resource you want to deploy to your machines.

{{<imgproc src="/how-tos/deploy-packages/add-package.png" resize="800x" class="fill aligncenter" style="width: 400px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Copy the raw JSON**

In your machine's **CONFIGURE** tab, switch to **JSON** and copy the raw JSON.

{{<imgproc src="/how-tos/deploy-packages/json-config.png" resize="800x" class="fill aligncenter" style="width: 600px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep link="/manage/fleet/reuse-configuration/" %}}
**3. Create a fragment**

Go to [app.viam.com/fragments](https://app.viam.com/fragments).

Add a fragment, and paste the copied JSON configuration into it.

{{<imgproc src="/how-tos/deploy-packages/fragment.png" resize="1000x" alt="Configuration builder UI">}}

Set your privacy settings.
There are three options for this:

- **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
- **Private:** No user outside of your organization will be able to view or use this fragment.
- **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

Click **Save**.

If you want to edit the fragment later, do it from this screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/delete.png" class="fill alignleft" resize="500x" style="width: 200px" declaredimensions=true alt="Delete">}}
**4. Delete the original machine configuration (optional)**

Now that the configuration is saved as a fragment, you can delete the machine you created in step 1.
We only created this machine to easily generate the JSON config for the fragment.

{{% /tablestep %}}
{{< /table >}}

## Add the fragment to multiple machines

With your fragment created, add it to all machines that need it:

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/how-tos/deploy-packages/insert.png" resize="800x" class="fill alignleft imgzoom" style="width: 250px" declaredimensions=true alt="Add fragment">}}
**1. Add the fragment to one machine**

On your machine's **CONFIGURE** tab, click the **+** button and select **Insert fragment**.
Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{< alert title="Tip" color="tip" >}}
You can add multiple fragments to one machine.
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/repeat.svg" class="fill alignleft" style="width: 120px"  declaredimensions=true alt="Repeat">}}
**2. Repeat for each machine**

Repeat step 1 for each of the machines that you want to add and manage the package for.

{{% /tablestep %}}
{{< /table >}}
