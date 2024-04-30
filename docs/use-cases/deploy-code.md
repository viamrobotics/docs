---
title: "Manage and deploy code versions"
linkTitle: "Manage and deploy code versions"
type: "docs"
weight: 30
images: ["/platform/registry.svg"]
description: "Deploy and manage module versions as public or private resources with the Viam CLI."
---

While Viam provides built-in support for a variety of components and services, you can use {{< glossary_tooltip term_id="module" text="modules" >}} to extend support for any hardware components or software services, across both industrial and consumer domains, whether proprietary or not.

Modules allow you to write and deploy custom code to your machine or fleet of machines, with robust control over how changes to your module's code are distributed to deployed machines.

You can choose to develop your module locally, and deploy to your machine directly using a local module installation, or you can upload your module to the Viam registry, making it easy to deploy to all of your machines.
Further, you can determine the accessibility of your module when you upload it - either keeping it private for exclusive access within your organization or making it public for availability to all Viam users.

When you deploy a module, whether its one you've written yourself or added from the registry, you maintain complete control over how that module's code is deployed to your machine when new updates to the module are available.

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/registry/module-icon.svg" class="fill alignleft" style="max-width: 150px" alt="Search modules">}}
**1. Search modules**

Once you [have created a machine in the Viam app](/fleet/machines/#add-a-new-machine), [search for modules in the Viam registry](/registry/configure/) that fit your machine's requirements, and then [add a module](/registry/configure/#add-a-modular-resource-from-the-viam-registry) from your machine's configuration page in the Viam app.

{{< /tablestep >}}
{{< tablestep >}}

{{<imgproc src="/registry/create-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Create your own module">}}
**2. Create your own module**

Or, you can [create your own module](/registry/create/) to add support for new hardware, or to extend an existing software service.

{{< /tablestep >}}
{{< tablestep >}}

{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Deploy your module">}}
**3. Deploy your module**

Once you have created your new module, you can deploy it to your machine in one of two ways:

- You can [upload your module](/registry/upload/) to the Viam registry using the Viam CLI. Modules available from the Viam registry can be deployed directly to a machine or fleet of machines from the Viam app. When you upload your module to the registry, you can choose to make it **public** to make your module available to all or **private** to make your module only visible to members of your [organization](/fleet/organizations/).
- You can deploy your module directly to your machine as a [local module](/registry/configure/#local-modules). Local modules are not uploaded to the Viam registry, and must be manually added to your machine.

If your machine is offline when you deploy a module, it will deploy once your machine comes back online.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/registry/create-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure your module">}}
**4. Configure your module**

Once you've deployed a module to your machine or fleet, [configure the module](/registry/configure/#edit-the-configuration-of-a-module-from-the-viam-registry) to set any necessary attributes it may require.

You can also configure [how a deployed module updates itself](/registry/configure/#configure-version-update-management-for-a-registry-module) when new versions of that module become available from the Viam registry. You can choose to always update to the latest version as soon as it becomes available, pin to a specific code revision and never update it, or upgrade only within a specified major or minor version.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/registry/upload-module.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Update your module">}}
**5. Update your module**

When you make code changes to your module, you can [update your module](/registry/upload/#update-an-existing-module) with those changes using the Viam CLI.
You can also use a [GitHub action to automate module releases](/registry/upload/#update-an-existing-module-using-a-github-action) as part of a continuous integration (CI) workflow.

These options make it easy to push changes to a fleet of machines.

{{< /tablestep >}}
{{< /table >}}
