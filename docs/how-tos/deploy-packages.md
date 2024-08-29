---
title: "Deploy and update packages across devices"
linkTitle: "Deploy and update packages"
weight: 40
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "You can use a fragment to deploy software packages to many machines, as well as to keep those software packages versioned."
languages: []
viamresources: []
level: "Intermediate"
date: "2024-08-28"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for using the same configuration on multiple machines.
You can use a fragment to deploy software packages to many machines, as well as to keep those software packages versioned.

{{< alert title="In this page" color="tip" >}}

1. [Add a package to a fragment](#create-a-fragment)
1. [Add the fragment to multiple machines](#add-the-fragment-to-multiple-machines)
1. [Testing strategies](#testing-strategies)
1. [Update a package version](#update-a-package-version)

{{< /alert >}}

## Create a fragment

{{< table >}}
{{% tablestep link="/configure/" %}}
**1. Configure your software**

Start by adding a new machine in the [Viam app](https://app.viam.com).
You do not need to follow the setup instructions.

Use the **CONFIGURE** tab to add the component or service you want to deploy across your machines.

{{<imgproc src="/how-tos/deploy-packages/add-package.png" resize="800x" class="fill aligncenter" style="max-width: 400px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Copy the raw JSON**

In your machine's **CONFIGURE** tab, switch to **JSON** and copy the raw JSON.

{{<imgproc src="/how-tos/deploy-packages/json-config.png" resize="800x" class="fill aligncenter" style="max-width: 600px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep link="/fleet/fragments/" %}}
**3. Create a fragment**

Go to [app.viam.com/fragments](https://app.viam.com/fragments).

Add a fragment, and paste the copied JSON configuration into it.

{{<imgproc src="/how-tos/deploy-packages/fragment.png" resize="800x" class="fill aligncenter" style="max-width: 600px" declaredimensions=true alt="Configuration builder UI">}}

Set your privacy settings.
There are three options for this:

- **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
- **Private:** No user outside of your organization will be able to view or use this fragment.
- **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

Click **Save**.

If you want to edit the fragment later, do it from this screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/delete.png" class="fill alignleft" resize="500x" style="max-width: 200px" declaredimensions=true alt="Delete">}}
**4. Delete the original machine configuration (optional)**

Now that the configuration is saved as a fragment, you can delete the machine you created in step 1.
We only created this machine to easily generate the JSON config for the fragment.

{{% /tablestep %}}
{{< /table >}}

## Add the fragment to multiple machines

With your fragment created, you can add it to as many machines as you'd like:

{{< table >}}
{{% tablestep %}}
{{<imgproc src="/how-tos/deploy-packages/insert.png" resize="800x" class="fill alignleft imgzoom" style="max-width: 250px" declaredimensions=true alt="Add fragment">}}
**1. Add the fragment to one machine**

On your machine's **CONFIGURE** tab, click the **+** button and select **Insert fragment**.
Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/repeat.svg" class="fill alignleft" style="max-width: 120px"  declaredimensions=true alt="Repeat">}}
**2. Repeat for each machine**

Repeat step 1 for each of the machines that you want to add and manage the package for.

{{% /tablestep %}}
{{< /table >}}

## Testing Strategies

If you inspect the fragment you have created, you will notice it contains a `version` field.

As you develop new versions of your software, your machines will continue to use the version of the software that you have configured in the fragment.

We generally recommend that you test updates on a subset of machines before deploying it to all machines.

You can either create a second fragment that you add to a subset of machines, or manually overwrite the version of the package for a subset of machines:

{{< tabs >}}
{{< tab name="A second fragment" >}}

{{< table >}}
{{% tablestep %}}
**1. Create a fragment for development**

Copy the JSON object from your primary fragment and create a second fragment.
We recommend you call your second fragment something easily identifiable as your testing environment, such as `FragmentName-DEV`.

Paste the JSON object from your primary fragment.

{{% /tablestep %}}
{{% tablestep %}}
**2. Edit the fragment**

Change the version of your package in the development fragment.
For example:

```json {class="line-numbers linkable-line-numbers" data-line="16"}
{
  "services": [
    {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio",
      "attributes": {}
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      "version": "0.5.3"
    }
  ]
}
```

{{% /tablestep %}}
{{% tablestep %}}
**3. Add the development fragment to a subset of machines**

Configure a subset of your machines with the development fragment.
If you had configured them already with the primary fragment, remove that fragment first.

{{% /tablestep %}}
{{% tablestep %}}
**4. Test the new version**

Test the new version of your package.
When you are satisfied that your package works as expected, continue to [update your primary fragment](#update-a-package-version).

{{% /tablestep %}}
{{< /table >}}

{{< /tab >}}
{{< tab name="Manual testing" >}}

{{< table >}}
{{% tablestep %}}
**1. Change the version of the module**

You can overwrite parts of a fragment to use a new version of a package without modifying the upstream fragment.

For each machine that you would like to test the new version of the package on, go to its **CONFIGURE** tab, find the package, and edit its version number.

{{<imgproc src="/how-tos/deploy-packages/version-change.png" resize="800x" class="fill aligncenter" style="max-width: 600px" declaredimensions=true alt="Configuration builder UI">}}

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
**2. Test the new version**

Test the new version of your package.
When you are satisfied that your package works as expected, continue to [update your primary fragment](#update-a-package-version).

{{% /tablestep %}}
{{< /table >}}

{{% /tab %}}
{{< /tabs >}}

## Update a package version

Once you have confirmed that the new version of your package works, go to your primary fragment and edit it to use the new version of your package.

For example:

```json {class="line-numbers linkable-line-numbers" data-line="16"}
{
  "services": [
    {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio",
      "attributes": {}
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      "version": "0.5.3"
    }
  ]
}
```

Don't forget to **Save**.

All machines configured with your fragment will update when they next check for configuration updates.

## Next steps

If you are setting up a larger fleet, you can use fragments to configure many machines and you can use Viam's provisioning manager, Viam Agent, to automate the process of setting up machines with your fragments:

{{< cards >}}
{{% card link="/how-tos/one-to-many/" %}}
{{% card link="/fleet/provision/" %}}
{{< /cards >}}
