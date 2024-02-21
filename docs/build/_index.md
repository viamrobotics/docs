---
title: "Build Your Machine with Flexible Building Blocks"
linkTitle: "Build"
description: "Configure and program your smart machine with Viam."
icon: "/platform/build.svg"
images: ["/platform/build.svg"]
imageAlt: "Tools and building blocks."
weight: 410
type: "docs"
no_list: true
menuindent: true
---

Viam uses a composable system of building blocks called {{< glossary_tooltip term_id="resource" text="resources" >}} which you can combine according to your specific needs.
Components drive your hardware, and services provide high-level software functionality.

Viam's APIs are standardized across all models of a given component or service.
This means you can test and change hardware without changing code.

{{% alert title="Start building" color="tip" %}}

1. To get started, first [install `viam-server`](/get-started/installation/) on your smart machine's computer.
   If you are using a microcontroller instead of a 64-bit computer, you can install a [lightweight version of `viam-server`](/build/micro-rdk/).

2. Then pull together the Viam resources you want to use by [configuring your smart machine](/build/configure/).

3. Finally, [program your smart machine](/build/program/) with an SDK in your preferred coding language.

{{% /alert %}}

<div class="cards max-page">
  <div class="row">
    <div class="col sectionlist">
        <div>
        <h2>Components:</h2>
        {{<sectionlist section="/components/">}}
        </div>
    </div>
    <div class="col sectionlist">
<div><h2>Services:</h2><ul class="sectionlist"><li><a href="/data/" title="Data Management Service"><div><picture><img src="../services/icons/data-capture.svg" alt="Data Management" loading="lazy"></picture><p>Data Management</p></div></a></li></ul><ul class="sectionlist"><li><a href="/mobility/motion/" title="Motion Service"><div><picture><img src="../services/icons/motion.svg" alt="Motion" loading="lazy"></picture><p>Motion</p></div></a></li></ul><ul class="sectionlist"><li><a href="/mobility/frame-system/" title="The Robot Frame System"><div><picture><img src="../services/icons/frame-system.svg" alt="Frame System" loading="lazy"></picture><p>Frame System</p></div></a></li></ul><ul class="sectionlist"><li><a href="/mobility/base-rc/" title="Base Remote Control Service"><div><picture><img src="../services/icons/base-rc.svg" alt="Base Remote Control" loading="lazy"></picture><p>Base Remote Control</p></div></a></li></ul><ul class="sectionlist"><li><a href="/ml/" title="ML Model Service"><div><picture><img src="../services/icons/ml.svg" alt="ML Model" loading="lazy"></picture><p>ML Model</p></div></a></li></ul><ul class="sectionlist"><li><a href="/mobility/navigation/" title="The Navigation Service"><div><picture><img src="../services/icons/navigation.svg" alt="Navigation" loading="lazy"></picture><p>Navigation</p></div></a></li></ul><ul class="sectionlist"><li><a href="/mobility/slam/" title="SLAM Service"><div><picture><img src="../services/icons/slam.svg" alt="SLAM" loading="lazy"></picture><p>SLAM</p></div></a></li></ul><ul class="sectionlist"><li><a href="/ml/vision/" title="Vision Service"><div><picture><img src="../services/icons/vision.svg" alt="Vision" loading="lazy"></picture><p>Vision</p></div></a></li></ul><ul class="sectionlist"><li><a href="/registry/advanced/generic/" title="Generic Service"><div><picture><img src="../icons/components/generic.svg" alt="Generic" loading="lazy"></picture><p>Generic</p></div></a></li></ul></div>
    </div>
  </div>
</div>

If a component or service you want to use for your project is not natively supported, see the [modular resource registry](/registry/).

## SDKs

Each category of resource has a standardized API that you can access with an SDK (software development kit) in your preferred programming language.
For example, you can send the same commands to any kind of motor, using any of the following programming languages:

{{<sectionlist section="/sdks">}}

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/build/program/" %}}
{{% card link="/build/micro-rdk/" %}}
{{< /cards >}}
