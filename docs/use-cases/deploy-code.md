---
title: "Manage and deploy code versions for an existing machine"
linkTitle: "Manage and deploy code versions"
weight: 40
tags: []
no_list: true
description: "Deploy and manage module versions as public or private resources with the Viam CLI"
---

You can upload custom modules, either as public resources accessible to all Viam users or as private modules shared exclusively within your organization.

Once uploaded, you can update and manage module versions by using the [modular registry](https://app.viam.com/registry) to ensure your modules are accessible and kept up to date.
This functionality is accessed through the [Viam CLI](/fleet/cli/), which provides an alternative method for module management.

For example, you might want to use the registry to contribute to collaborative projects, share modules with a select group of people, or maintain a private collection of modules designed for your machine's needs.

<table>
    <tr>
        <th> {{<imgproc src="/use-cases/create-module-command.png" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
            <b> 1. Create your module </b>
            <p> [Create a module](/create/) that implements an existing Viam [API](/build/program/apis/) as either a public or private module.
            By default, a new module is created as private.
            You can later make a private module public using the `viam module update` command, but once you make a module public, you cannot change it back to private.<br>
            You can also use the Viam CLI `create` command to choose a custom module name using the `name` command, generate the required metadata, and optionally set your module's privacy level by filling the `visibility` field in the JSON file resulting from the `create` command.
            </p>
        </th>
    </tr>
    <tr>
        <td> {{<imgproc src="/use-cases/upload-module-command.png" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
        <b> 2. Upload your modular resource </b>
            <p> [Upload your modular resource](/upload/#upload-a-custom-module) to the registry by using the `upload` command. <br> You can also use the `--version` argument to set the version of your module for the upload.  <br>
            </p>
        </th>
    </tr>
    <tr>
        <td> {{<imgproc src="/use-cases/update-module-command.png" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
            <b> 3. Manage your modular resource </b>
            <p> Once you've uploaded your module, manage and update your existing modules in the registry [manually](/registry/upload/#update-an-existing-module-using-the-viam-cli) by using the Viam CLI `update` command, or automatically by using a [GitHub action](/registry/upload/#update-an-existing-module-using-a-github-action). <br>
            You can also choose to pin to a specific patch version, permit upgrades within major release families or only within minor releases, or permit continuous updates.</p>
        </th>
    </tr>
</table>

## Next Steps

{{< cards >}}
{{% card link="/registry/upload/" %}}
{{% card link="/registry/create/" %}}
{{% card link="/registry/examples/" %}}
{{< /cards >}}
