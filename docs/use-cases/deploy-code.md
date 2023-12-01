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

You can create, publish, and manage add functionality to Viam's components and services through the [modular registry](https://app.viam.com/registry).
If the specific component or service you need is not natively supported, you can use pre-written {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} from the registry or create your own.

For example, you can have a variety of modular resources in the registry made for specific tasks, such as [hardware integration](https://app.viam.com/module/viam/agilex-limo),[data filtration](https://app.viam.com/module/erh/filtered-camera), or [service expansion](https://app.viam.com/module/viam/obstacles_2d_lidar).

<table>
    <tr>
        <th> {{<imgproc src="PLACEHOLDER" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
            <b> 1. Create your modular resource </b>
            <p> [Create your own modular resource](/create/) that implements an existing Viam [API](/build/program/apis/) to add support for {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="type" text="types" >}} or {{< glossary_tooltip term_id="model" text="models" >}} that are not built into Viam.
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
            <p> After uploading your module, [configure it for automatic version updates](/upload/#update-an-existing-module-using-a-github-action) or [update it manually](/upload/#update-an-existing-module-using-the-viam-cli). Modules added to your robot wil remain at the version installed by default, with the option for manual updates.</p>
        </th>
    </tr>
    <tr>
        <td> {{<imgproc src="PLACEHOLDER" class="fill alignright" style="max-width: 300px" declaredimensions=true alt="">}}
            <b> 4. Test your modular resource</b>
            <p> Test your modular resource using the Control tab and program it with Viam's Go or Python SDKs.</p>
        </th>
    </tr>
</table>

## Next Steps

{{< cards >}}
{{% card link="/registry/upload/" %}}
{{% card link="/registry/create/" %}}
{{% card link="/registry/examples/" %}}
{{< /cards >}}
