---
title: "How to configure multiple similar machines"
linkTitle: "Configure many machines"
weight: 40
type: "docs"
tags: ["data management", "data", "services"]
images: ["/how-tos/one-to-many/new-fragment.png"]
description: "Configuring fragments."
aliases:
  - /use-cases/one-to-many/
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
**1. Configure one machine**

Start by configuring one of your machines.

In the [Viam app](https://app.viam.com), use the **CONFIGURE** tab to build a configuration for all components and services you want to use on all your machines.

{{<imgproc src="/how-tos/one-to-many/config.png" resize="800x" class="fill aligncenter" style="max-width: 400px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Copy the raw JSON**

In your machine's **CONFIGURE** tab, switch to **JSON** and copy the raw JSON.

{{<imgproc src="/how-tos/one-to-many/raw-json.png" resize="700x" class="fill aligncenter" style="max-width: 400px" declaredimensions=true alt="JSON subtab of the CONFIGURE tab">}}

{{% /tablestep %}}
{{% tablestep link="/fleet/fragments/" %}}
**3. Create a fragment**

Go to [app.viam.com/fragments](https://app.viam.com/fragments).

Add a fragment, and paste the copied JSON configuration into it.

Set your privacy settings.
There are three options for this:

- **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
- **Private:** No user outside of your organization will be able to view or use this fragment.
- **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

Click **Save**.

If you want to edit the fragment later, do it from this screen.

{{<imgproc src="/how-tos/one-to-many/new-fragment.png" resize="700x" class="fill aligncenter" style="max-width: 350px" declaredimensions=true alt="app.viam.com/fragment interface">}}

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/delete.png" class="fill alignleft" resize="500x" style="max-width: 200px" declaredimensions=true alt="Delete">}}
**4. Delete the original configuration (optional)**

Now that the configuration is saved as a fragment, you can delete each resource in the original config from your machine and _replace the config with the fragment_ in the next step.
In this way, you can keep all your machines up to date whenever you change the fragment.

{{% /tablestep %}}
{{< /table >}}

## Add a fragment to multiple machines

With your fragment created, you can add it to as many machines as you'd like:

{{< table >}}
{{% tablestep %}}
{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="800x" class="fill alignleft imgzoom" style="max-width: 250px" declaredimensions=true alt="Add fragment">}}
**1. Add the fragment to one machine**

On your machine's **CONFIGURE** tab, click the **+** button and select **Insert fragment**.
Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/repeat.svg" class="fill alignleft" style="max-width: 120px"  declaredimensions=true alt="Repeat">}}
**2. Repeat for each machine**

Repeat step 1 for each of the machines that you want to configure in the same way.

If some of your machines have slight differences, you can still add the fragment and then add fragment overwrites in the next section.

{{% /tablestep %}}
{{< /table >}}

## Modify a fragment

If your machines are similar but not identical, you can use a fragment with all of them, and then [overwrite parts of it](/fleet/fragments/#modify-the-config-of-a-machine-that-uses-a-fragment) to customize select fields of the configuration without modifying the upstream fragment.

{{% alert title="Note" color="note" %}}
If you modify fields within a fragment, your modifications will act as overwrites.
If you later update the upstream fragment, the updates to the overwritten fields will effectively not be updated.
{{% /alert %}}

{{< table >}}
{{% tablestep link="/fleet/fragments/#modify-the-config-of-a-machine-that-uses-a-fragment" %}}
{{<gif webm_src="/how-tos/fragment-overwrite.webm" mp4_src="/how-tos/fragment-overwrite.mp4" alt="A motor config panel from a fragment being edited with different direction and pwm pin values." max-width="500px" class="aligncenter" >}}

<!-- markdownlint-disable MD036 -->

**1. Edit your machine's config**

Go to the **CONFIGURE** tab of the machine whose config you want to modify, and make your edits just as you would edit a non-fragment resource.

You can click the **{}** button to switch to advanced view and see the changes.

Don't forget to **Save**.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/reset.png" class="fill alignleft" resize="500x" style="max-width: 250px"  declaredimensions=true alt="Reset to fragment">}}
**2. (Optional) Revert fragment modifications**

If you need to restore the original fragment, click the **...** in the upper right corner of the card you modified, and click **Revert changes**.
Now, the fragment will be identical to the upstream fragment.

{{% /tablestep %}}
{{< /table >}}

## Next steps

To set up a larger fleet without manually adding a fragment to each machine configuration, you can use Viam's provisioning manager, Viam Agent:

{{< cards >}}
{{% card link="/fleet/provision/" %}}
{{< /cards >}}
