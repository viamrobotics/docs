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
        <th>{{<imgproc src="/ml/collect.svg" class="fill alignright" resize="450x" declaredimensions=true alt="ml collect icon">}}
            <b>1. <a href="/registry/configure/">Search for a module</a></b>
            <br><br>
            <p>First, <a href="/fleet/machines/#add-a-new-robot">create a robot</a></p> if you haven't yet.
            <p>Search for a module that fits your machine's requirements in the Viam Registry.</p>
            <p>You can easily add it from your robot's page.</p>
        </th>
    </tr>
    <tr>
        <td>{{<imgproc src="/ml/configure.svg" class="fill alignright" resize="450x" declaredimensions=true alt="ml configure icon">}}
        <b>2. <a href="https://docs.viam.com/registry/create/">Create your own module</a></b>
            <br><br><p>If you don't find a module that meets your needs, you can create your own module to add support for hardware with no built-in support, or to extend an existing software service.</p>
        </td>
    </tr>
    <tr>
        <td>{{<imgproc src="/ml/deploy.svg" class="fill alignright" resize="450x" declaredimensions=true alt="ml deploy icon">}}
            <b>3. <a href="/registry/upload/">Deploy your module</a></b>
            <br><br><p>You can deploy your module to the Viam registry.</p>
             <p>You can register your module as public and extend accessibility to all Viam users, or as private and limit accessibility to users in your organization.</p>
             <p>Visit <a href="/registry/upload/#upload-a-custom-module">Upload a custom module</a> for more information.</p>
             <p>You can easily deploy to robot or fleet directly from your robot's page in the Viam app or as a <a href="/registry/configure/#local-modules">local module</a> if desired.</p>
        </th>
    </tr>
     <tr>
        <td>{{<imgproc src="/ml/configure.svg" class="fill alignright" resize="450x" declaredimensions=true alt="ml configure icon">}}
            <b>4. <a href="https://docs.viam.com/registry/configure/#edit-the-configuration-of-a-module-from-the-viam-registry">Configure your module</a></b>
            <br><br>
            <p>Configure necessary attributes your module may require.</p>
            <p>You can also configure how your module updates itself when a new version becomes available.</p>
        </td>
    </tr>
    <tr>
        <td>{{<imgproc src="/icons/components/controller.svg" class="fill alignright" resize="450x" declaredimensions=true alt="controller icon">}}
            <b>5. Update your module</b>
            <br><br>
            <p>You have the option to update your module in the registry with the latest changes.</p>
            <p>This makes it easy to push changes to a fleet of machines.</p>
        </td>
    </tr>
</table>
