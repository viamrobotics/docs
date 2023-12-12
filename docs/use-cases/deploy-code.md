---
title: "Manage and deploy code versions"
linkTitle: "Manage and deploy code versions"
weight: 40
type: "docs"
weight: 30
description: "Deploy and manage module versions as public or private resources with the Viam CLI."
---

You can upload custom modules, either as public resources accessible to all Viam users or as private modules shared exclusively within your organization.

Once uploaded, you can update and manage module versions by using the [modular registry](https://app.viam.com/registry) to ensure your modules are accessible and kept up to date.
This functionality is accessed through the [Viam CLI](/fleet/cli/), which provides an alternative method for module management.

For example, you might want to use the registry to contribute to collaborative projects, share modules with a select group of people, or maintain a private collection of modules designed for your machine's needs.

<table>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignleft" style="max-width: 150px" alt="ml collect icon">}}
      <b>1. Search for a module</b>
      <br><br>
      <p>First, <a href="/fleet/machines/#add-a-new-robot">create a robot</a> if you haven't yet.</p>
      <p><a href="/registry/configure/">Search for a module</a> that fits your machine's requirements in the Viam Registry and <a href="https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry">add it</a> from your robot's page.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml configure icon">}}
      <b>2. Create your own module</b>
      <br><br>
      <p>If you don't find a module that meets your needs, you can <a href="https://docs.viam.com/registry/create/">create your own module</a> to add support for hardware with no built-in support, or to extend an existing software service.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml deploy icon">}}
      <b>3. Deploy your module</b>
      <br><br>
      <p>Once you create your module, you can <a href="/registry/upload/">deploy it to the Viam registry</a>.</p>
      <p>You can register your module as public and extend accessibility to all Viam users, or as private and limit accessibility to users in your organization. Visit <a href="/registry/upload/#upload-a-custom-module">Upload a custom module</a> for more information.</p>
      <p>You can easily deploy to robot or fleet directly from your robot's page in the Viam app or as a <a href="/registry/configure/#local-modules">local module</a> if desired.</p>  
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml configure icon">}}
      <b>4. Configure your module</b>
      <br><br>
      <p><a href="https://docs.viam.com/registry/configure/#edit-the-configuration-of-a-module-from-the-viam-registry">Configure your module</a> and set the necessary attributes it may require.</p>
      <p>You can also configure how your module updates itself when a new version becomes available.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/icons/components/controller.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="controller icon">}}
      <b>5. Update your module</b>
      <br><br>
      <p>You have the option to <a href="/registry/upload/#update-an-existing-module">update your module</a> in the registry with the latest changes.
      This makes it easy to push changes to a fleet of machines.</p>
    </th>
  </tr>
</table>
