---
title: "Manage and deploy code versions"
linkTitle: "Manage and deploy code versions"
type: "docs"
weight: 30
description: "Deploy and manage module versions as public or private resources with the Viam CLI."
---

You can extend Viam to include support for any kind of machine, whether proprietary or not, industrial or consumer-based, by creating custom {{< glossary_tooltip term_id="module" text="modules" >}}.

Once created and uploaded, you can update and manage module versions by using the [modular registry](https://app.viam.com/registry) to ensure your modules are accessible and kept up to date.

You can also add an existing module from the [Viam registry](https://app.viam.com/registry), or create your own.

With modules, it is easy to deploy code to a robot or a fleet of robots with robust control over code versioning.

<table>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignleft" style="max-width: 150px" alt="ml collect icon">}}
      <b>1. Search modules</b>
      <br><br>
      <p>First, <a href="/fleet/machines/#add-a-new-robot">create a robot</a> if you haven't yet.</p>
      <p><a href="/registry/configure/">Search for modules</a> that fits your robot's requirements in the Viam Registry and <a href="https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry">add it</a> from your robot's page.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml configure icon">}}
      <b>2. Create your own module</b>
      <br><br>
      <p>If you don't find a module that meets your needs, you can <a href="https://docs.viam.com/registry/create/">create your own module</a> to add support for new hardware, or to extend an existing software service.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/deploy.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml deploy icon">}}
      <b>3. Deploy your module</b>
      <br><br>
      <p>Once you create your module, you can <a href="/registry/upload/">upload</a> it to the Viam registry for deployment. You have the option to customize several aspects of your deployment experience: </p></br>
      <ul>
        <li>
          Deployment Visibility: You can tailor your module's visibility by <a href="https://docs.viam.com/registry/upload/#upload-a-custom-module">uploading it to the registry</a> as either a public or private module.
              <ul>
                <li>A public module is available to all Viam users.</li>
                <li>A private module is visible only to members of your <a href="/fleet/organizations/">organization</a>.</li>
              </ul>
         </li>
      </ul>
      <ul>
        <li>
        Offline Deployment: If your robot was offline when you configured the module for use, it will deploy once your machine is online.
        </li>
        </br>
        <li>
        Local Module Deployment: You can easily deploy to a robot or fleet as a <a href="/registry/configure/#local-modules">local module</a> to develop your module locally before uploading it to the Viam registry.
        </li>
      </ul>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="ml deploy icon">}}
      <b>4. Configure your module
      <br><br>
      <p>Once you've deployed a module to your robot or fleet, <a href="https://docs.viam.com/registry/configure/#edit-the-configuration-of-a-module-from-the-viam-registry">configure the module</a> to set any necessary attributes it may require.</p>
      <p>You can also configure <a href="/registry/configure/#configure-version-update-management-for-a-registry-module">how a deployed module updates itself</a> when new versions of that module become available from the Viam registry.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/build/configure/services/icons/motion.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="controller icon">}}
      <b>5. Update your module</b>
      <br><br>
      <p>When you make code changes to your module, you can <a href="/registry/upload/#update-an-existing-module">update your module</a> with those changes. You can also use a <a href="/registry/upload/#update-an-existing-module-using-a-github-action">GitHub action to automate module releases</a> as part of a continuous integration (CI) workflow.</p>
      <p>These options make it easy to push changes to a fleet of robots.</p>
    </th>
  </tr>
</table>
