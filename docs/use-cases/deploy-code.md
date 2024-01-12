---
title: "Manage and deploy code versions"
linkTitle: "Manage and deploy code versions"
type: "docs"
weight: 30
description: "Deploy and manage module versions as public or private resources with the Viam CLI."
---

While Viam provides built-in support for a variety of components and services, you can use {{< glossary_tooltip term_id="module" text="modules" >}} to extend support for any hardware components or software services,across both industrial and consumer domains, whether proprietary or not.

Modules allow you to write and deploy custom code to your machine or fleet of machines, with robust control over how changes to your module's code are distributed to deployed machines.

You can choose to develop your module locally, and deploy to your machine directly using a local module installation, or you can upload your module to the Viam registry, making it easy to deploy to all of your machines.
Further, you can determine the accessibility of your module when you upload it - either keeping it private for exclusive access within your organization or making it public for availability to all Viam users.

When you deploy a module, whether its one you've written yourself or added from the registry, you maintain complete control over how that module's code is deployed to your machine when new updates to the module are available.

<table>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignleft" style="max-width: 150px" alt="ml collect icon">}}
      <b>1. Search modules</b>
      <br><br>
      <p>Once you <a href="/fleet/machines/#add-a-new-robot">have created a machine in the Viam app</a>, <a href="/registry/configure/">search for modules in the Viam registry</a> that fit your machine's requirements, and then <a href="/registry/configure/#add-a-modular-resource-from-the-viam-registry">add a module</a> from your machine's configuration page in the Viam app.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml configure icon">}}
      <b>2. Create your own module</b>
      <br><br>
      <p>Or, you can <a href="https://docs.viam.com/registry/create/">create your own module</a> to add support for new hardware, or to extend an existing software service.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml deploy icon">}}
      <b>3. Deploy your module</b>
      <br><br>
       <p>Once you have created your new module, you can deploy it to your machine in one of two ways:</p><br><br><br>
        <ul>
            <li>
            You can <a href="/registry/upload/">upload your module</a> to the Viam registry using the Viam CLI. Modules available from the Viam registry can be deployed directly to a machine or fleet of machines from the Viam app. When you upload your module to the registry, you can choose to make it:
            </li>
            <ul>
                <li>
                    <b>Public:</b> your module is available to all Viam users.
                </li>
                <li>
                    <b>Private:</b> your module is only visible to members of your <a href="/fleet/organizations/">organization</a>. This is the default state of new modules.
                </li>
            </ul>
            <li>
                You can deploy your module directly to your machine as a <a href="/registry/configure/#local-modules">local module</a>. Local modules are not uploaded to the Viam registry, and must be manually added to your machine.
            </li>
        </ul>
        <p> If your machine is offline when you deploy a module, it will deploy once your machine comes back online.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml deploy icon">}}
      <b>4. Configure your module
      <br><br>
      <p>Once you've deployed a module to your machine or fleet, <a href="https://docs.viam.com/registry/configure/#edit-the-configuration-of-a-module-from-the-viam-registry">configure the module</a> to set any necessary attributes it may require.</p>
      <p>You can also configure <a href="/registry/configure/#configure-version-update-management-for-a-registry-module">how a deployed module updates itself</a> when new versions of that module become available from the Viam registry. You can choose to always update to  the latest version as soon as it becomes available, pin to a specific code revision and never update it, or upgrade only within a specified major or minor version.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/navigation.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="controller icon">}}
      <b>5. Update your module</b>
      <br><br>
      <p>When you make code changes to your module, you can <a href="/registry/upload/#update-an-existing-module">update your module</a> with those changes using the Viam CLI. You can also use a <a href="/registry/upload/#update-an-existing-module-using-a-github-action">GitHub action to automate module releases</a> as part of a continuous integration (CI) workflow.</p>
      <p>These options make it easy to push changes to a fleet of machines.</p>
    </th>
  </tr>
</table>
