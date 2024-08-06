---
title: "How to configure multiple similar machines"
linkTitle: "Configure many machines"
weight: 40
type: "docs"
tags: ["data management", "data", "services"]
images: ["/platform/fleet.svg"]
description: "How to configure multiple similar or identical machines with fragments."
---

Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for copying parts of a configuration file to multiple machines, as well as for modifying just some sections of a config if your machines are similar but not identical.

When you update a fragment, it updates the configurations of all machines that use that fragment.

{{< alert title="In this page" color="tip" >}}

1. [Create a configuration fragment](#create-a-fragment)
1. [Apply a fragment to multiple machines](#add-a-fragment-to-multiple-machines)
1. [Modify an otherwise identical configuration](#modify-a-fragment)

{{< /alert >}}

For information on provisioning many machines, see [Provisioning](/fleet/provision/).

## Create a fragment

{{< table >}}
{{% tablestep link="/configure/" %}}
{{<imgproc src="/use-cases/one-to-many/config.png" resize="700x" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="Configuration builder UI">}}
**1. Configure one machine**

Start by configuring one of your machines.

In the [Viam app](https://app.viam.com), use the **CONFIGURE** tab to build a configuration for all components and services you want to use on all your machines.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/use-cases/one-to-many/raw-json.png" resize="700x" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="JSON subtab of the CONFIGURE tab">}}
**2. Copy the raw JSON**

In your machine's **CONFIGURE** tab, switch to **JSON** and copy the raw JSON.

{{% /tablestep %}}
{{% tablestep link="/fleet/fragments/#create-a-fragment" %}}
{{<imgproc src="/use-cases/one-to-many/new-fragment.png" resize="700x" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="app.viam.com/fragment interface">}}
**3. Create a fragment**

Go to [app.viam.com/fragments](https://app.viam.com/fragments).

Add a fragment, and paste the copied JSON configuration into it.

Set your privacy settings, then click **Save**.

If you want to edit the fragment later, do it from this screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/use-cases/one-to-many/noun-trash.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Delete">}}
**3. Delete the original configuration (optional)**

Now that the configuration is saved as a fragment, you can delete the original config from your machine and _replace it with the fragment_.
In this way, you can keep all your machines up to date whenever you change the fragment.

{{% /tablestep %}}
{{< /table >}}

## Add a fragment to multiple machines

Now that you have a fragment, you can add it to as many machines as you'd like:

{{< table >}}
{{% tablestep link="/fleet/fragments/#add-a-fragment-to-a-machine" %}}
{{<imgproc src="/get-started/try-viam/rover-resources/fragments/fragments_list.png" resize="700x" class="fill alignleft" style="max-width: 250px" declaredimensions=true alt="Add fragment">}}
**1. Add the fragment to one machine**

On your machine's **CONFIGURE** tab, click the **+** button and select **Insert fragment**.
Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/use-cases/one-to-many/noun-repeat.svg" class="fill alignleft" style="max-width: 100px"  declaredimensions=true alt="Repeat">}}
**2. Repeat for each machine**

Repeat step 1 for each of the machines that you want to configure in the same way.

If some of your machines have slight differences, you can still add the fragment and then add fragment mods in the next section.

{{% /tablestep %}}
{{< /table >}}

## Modify a fragment

If your machines are similar but not identical, you can use a fragment with all of them, and then [edit it](/fleet/fragments/#modify-the-config-of-a-machine-that-uses-a-fragment) to customize select fields of the configuration without modifying the upstream fragment.

{{% alert title="Note" color="note" %}}
If you modify fields within a fragment, your modifications will act as overwrites.
If you later update the upstream fragment, the updates to the overwritten fields will effectively not be updated.
{{% /alert %}}

{{< table >}}
{{% tablestep link="/fleet/fragments/#modify-the-config-of-a-machine-that-uses-a-fragment" %}}
{{<imgproc src="/use-cases/one-to-many/noun-edit.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Edit">}}
**1. Edit your machine's config**

Go to the **CONFIGURE** tab of the machine whose config you want to modify, and make your edits.

Don't forget to **Save**.

{{% /tablestep %}}
{{% tablestep link="/fleet/fragments/#use-fragment_mods" %}}
{{<imgproc src="/use-cases/one-to-many/noun-reset.svg" class="fill alignleft" style="max-width: 100px"  declaredimensions=true alt="Reset to fragment">}}
**2. (Optional) Revert fragment modifications**

When you make edits to fields in your machine's config, a top-level section called `"fragment_mods"` is added to your JSON config with [update operators](https://www.mongodb.com/docs/manual/reference/operator/update/positional/#---update-) that modify each field you edit.

If you need to restore the original fragment, you can go to the **JSON** tab of your machine's **CONFIGURE** tab, and delete the entire `"fragment_mods"` section.
Now, the fragment will be identical to the upstream fragment.

{{% /tablestep %}}
{{< /table >}}

## Next steps

To set up a larger fleet even more quickly with `viam-server` and configurations, you can use Viam's provisioning manager, Viam Agent:

{{< cards >}}
{{% card link="/fleet/provision/" %}}
{{< /cards >}}
