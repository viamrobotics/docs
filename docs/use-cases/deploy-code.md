---
title: "Manage and deploy code versions"
linkTitle: "Manage and deploy code versions"
type: "docs"
weight: 30
tags: []
no_list: true
description: "Deploy and manage module versions as public or private resources with the Viam CLI."
---

You can upload custom modules, either as public resources accessible to all Viam users or as private modules shared exclusively within your organization.

Once uploaded, you can update and manage module versions by using the [modular registry](https://app.viam.com/registry) to ensure your modules are accessible and kept up to date.
This functionality is accessed through the [Viam CLI](/fleet/cli/), which provides an alternative method for module management.

For example, you might want to use the registry to contribute to collaborative projects, share modules with a select group of people, or maintain a private collection of modules designed for your machine's needs.

<table>
    <tr>
        <th>{{<imgproc src="/use-cases/create-module-command.png" class="fill alignright" resize="450x" declaredimensions=true alt="Create module command">}}
            <b>1. Create your module</b>
            <br><br><p>Use the Viam CLI <code>create</code> command to choose a custom module name using the <code>name</code> flag, generate the required metadata.</p>
            <p>By default, a new module is created as private.<p>
            </p>
        </th>
    </tr>
    <tr>
        <td>{{<imgproc src="/use-cases/upload-module-command.png" class="fill alignright" resize="450x" declaredimensions=true alt="Upload module command">}}
        <b>2. Upload your modular resource</b>
            <br><br><p>Use the <code>upload</code> command to <a href="/upload/#upload-a-custom-module">Uupload your modular resource</a> to the registry.</p>
            <p>You can also use the <code>--version</code> argument to set the version of your module for the upload.</p>
        </td>
    </tr>
    <tr>
        <td>{{<imgproc src="/use-cases/update-module-command.png" class="fill alignright" resize="450x" declaredimensions=true alt="Update module command">}}
            <b>3. Manage your modular resource</b>
            <br><br><p>Manage and update your existing module's version in the registry <a href="/registry/upload/#update-an-existing-module-using-the-viam-cli">manually</a> by using the Viam CLI <code>update</code> command, or automatically by using a <a href="/registry/upload/#update-an-existing-module-using-a-github-action">GitHub action</a>.</p>
        </th>
    </tr>
</table>

## Next Steps

{{< cards >}}
{{% card link="/registry/upload/" %}}
{{% card link="/registry/create/" %}}
{{% card link="/registry/examples/" %}}
{{< /cards >}}
