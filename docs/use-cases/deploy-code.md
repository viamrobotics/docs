---
title: "Manage and deploy code versions for an existing machine"
linkTitle: "Manage and deploy code versions"
weight: 40
tags: []
no_list: true
description: ""
image: ""
imageAlt: ""
images: [""]
---

You can upload custom modules, either as public resources accessible to all Viam users or as private modules shared exclusively within your organization.

Once uploaded, you can update and manage module versions by using the [modular registry](https://app.viam.com/registry) to ensure your modules are accessible and kept up to date.
This functionality is accessed through the Viam CLI, which provides an alternative method for module management.

For example, you might want to use the registry to contribute to collaborative projects, share modules to a select group of people, or maintain a private collection of modules tailored to your machine's needs.

<table>
    <tr>
        <th> {{<imgproc src="PLACEHOLDER" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
            <b> 1. Create your module </b>
            <p> [Create a module](/create/) that implements an existing Viam [API](/build/program/apis/) to add support for {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="type" text="types" >}} or {{< glossary_tooltip term_id="model" text="models" >}} that are not built into Viam.
            </p>
        </th>
    </tr>
    <tr>
        <td> {{<imgproc src="PLACEHOLDER" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
        <b> 2. Upload your modular resource </b>
            <p> [Upload your modular resource](/upload/#upload-a-custom-module), either as a public or private module using the `create`, `upload`, and `update` [Viam CLI](/fleet/cli/) commands.</p>
        </th>
    </tr>
    <tr>
        <td> {{<imgproc src="PLACEHOLDER" class="fill alignright"
        style="max-width: 300px" declaredimensions=true alt="">}}
            <b> 3. Manage your modular resource </b>
            <p> After uploading your module, [configure it for automatic version updates](/upload/#update-an-existing-module-using-a-github-action) or [update it manually](/upload/#update-an-existing-module-using-the-viam-cli). Modules added to your machine wil remain at the version installed by default, with the option for manual updates.</p>
        </th>
    </tr>
</table>

## Next Steps

{{< cards >}}
{{% card link="/registry/upload/" %}}
{{% card link="/registry/create/" %}}
{{% card link="/registry/examples/" %}}
{{< /cards >}}
