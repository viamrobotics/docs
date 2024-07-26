---
title: "Extend Viam with Models from the Viam Registry"
linkTitle: "Registry"
weight: 600
type: "docs"
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Add additional models of components and services or ML models from the Viam Registry, or extend Viam by creating new modular resources."
images: ["/platform/registry.svg"]
no_list: true
modulescript: true
aliases:
  - "/build/program/extend/modular-resources/"
  - "/extend/modular-resources/"
  - "/extend/"
  - "/build/program/extend/modular-resources/key-concepts/"
  - "/modular-resources/key-concepts/"
  - "/modular-resources/"
menuindent: true
---

The [Viam registry](https://app.viam.com/registry) is the central place where you can browse:

{{< cards >}}
{{% manualcard link="#modular-resources" %}}

**Modular resources** that add capabilities to your machine beyond what is built into `viam-server`

{{% /manualcard %}}
{{% manualcard link="#ml-models" %}}

**ML models** to deploy with machine applications like computer vision

{{% /manualcard %}}
{{% manualcard link="#ml-training-scripts" %}}

**Training scripts** to train and produce ML models in the Viam cloud for custom machine learning

{{% /manualcard %}}
{{< /cards >}}

## Modular resources

{{<imgproc src="/platform/registry.svg" class="alignright" resize="x900" declaredimensions=true alt="Representation of the Viam registry, some modules within it, and a rover they support." style="max-width:350px" >}}

Viam provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware {{< glossary_tooltip term_id="component" text="components" >}}.
- High-level functionality exposed as {{< glossary_tooltip term_id="service" text="services" >}}.

If the model of component or service you want to use for your project is not built into `viam-server` and available for configuration by default, you can use a {{< glossary_tooltip term_id="model" text="model" >}} from a {{< glossary_tooltip term_id="module" text="module" >}}.

A module provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, and is packaged in a manner that streamlines deployment to a Viam machine.
Modules run alongside [`viam-server`](/get-started/installation/) as separate processes, communicating with `viam-server` over UNIX sockets.
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and associated [APIs](/appendix/apis/) with `viam-server`, making the new model available for use.

To configure a modular resource on your robot, [add new models that others have created](/registry/configure/#add-a-modular-resource-from-the-viam-registry) from the [Viam registry](https://app.viam.com/registry) or [create your own](#create-your-own-modules).

You can search the available modular resources from the Viam registry here:

<div id="searchbox"></div>
<p>
<div id="searchstats"></div></p>
<div class="mr-component" id="">
  <div class="modellistheader">
    <div class="type">API</div>
    <div class="name">Model</div>
    <div>Description</div>
  </div>
<div id="hits" class="modellist">
</div>
<div id="pagination"></div>
</div>
<noscript>
    <div class="alert alert-caution" role="alert">
        <h4 class="alert-heading">Javascript</h4>
        <p>Please enable javascript to see and search models.</p>
    </div>
</noscript>

You can see details about each module in the [Viam registry](https://app.viam.com/registry) on its dedicated module page.
You can integrate modules into any Viam-powered machine.

Be aware that unlike natively available models, modular resources are not documented on the Viam Documentation.
Documentation for each modular resource is available on its GitHub page, which is linked from the models' page on [the registry](https://app.viam.com/registry) or by clicking on the model name in the above search.

## Use modules

To use a modular resource from the registry, add it from your machine's **CONFIGURE** tab in the Viam app, using the **Create component** button.

After adding a module to your machine, you can choose to [configure](/registry/configure/) it for automatic version updates from the Viam registry, or update your module manually.
By default, newly added modules will remain at the version they were when you installed them, and will not update automatically.

Once you have added and configured the module you would like to use in the Viam app, you can test your added resource using the [**CONTROL** tab](/fleet/control/) and program it using [standardized APIs](/appendix/apis/).

`viam-server` manages the [dependencies](/internals/rdk/#dependency-management), [start-up](/internals/rdk/#start-up), [reconfiguration](/internals/rdk/#reconfiguration), [data management](/services/data/capture/#configure-data-capture-for-individual-components), and [shutdown](/internals/rdk/#shutdown) behavior of your modular resource.

## Create your own modules

If none of the existing modular resources in the Viam registry support your use case, you can create your own modules to provide your own modular resources:

- **Implement a custom component**: Write a driver for an unsupported {{< glossary_tooltip term_id="component" text="component" >}} by implementing the corresponding component API.

- **Implement a custom service**: Implement your own algorithm or {{< glossary_tooltip term_id="model" text="model" >}} against a corresponding service API or use custom algorithms or data models when working with services such as {{< glossary_tooltip term_id="slam" text="SLAM" >}}, vision, or motion planning.

You can write modules in a variety of programming languages, such as, Go, Python, C++, Rust, while implementing the same [APIs](/appendix/apis/).

To create a new module:

1. [Create a module](/use-cases/create-module/) with one or more modular resources by implementing all methods for the component's or service's standardized API.
1. [Upload the module to the Viam registry](/use-cases/create-module//#upload-your-module-to-the-modular-resource-registry) to make it available for deployment to machines or add it as a [local module](/registry/configure/#local-modules).
   You can upload _private_ modules for your {{< glossary_tooltip term_id="organization" text="organization" >}} or _public_ modules.
1. Once you have uploaded your module to the registry, [deploy and configure the module](/registry/configure/) from the Viam app.
   Then, you can test your added resource using the [**CONTROL** tab](/fleet/control/) and [program](/build/program/) it with Viam's Go or Python SDKs.

See the following how-to guide for full instructions, or one of our example tutorials:

{{< cards >}}
{{% card link="/use-cases/create-module/" class="fit-contain" %}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{% card link="/registry/examples/custom-arm/" %}}
{{< /cards >}}

## ML models

Viam provides the ability to train, upload, and deploy machine learning models within the platform.
See [Machine Learning](/services/ml/) for more information.

The Viam registry hosts trained ML models that users have made public, which you can use to deploy classifiers or detectors for your use case onto your robot instead of training your own.
You can also [upload your own model to the registry](/services/ml/upload-model/).

You can search the available ML models from the Viam registry here:

<div id="searchboxML"></div>
<p>
<div id="searchstatsML"></div></p>
<div class="mr-model" id="">
  <div class="modellistheader">
    <div class="name">Model</div>
    <div>Description</div>
  </div>
<div id="hitsML" class="modellist">
</div>
<div id="paginationML"></div>
</div>
<noscript>
    <div class="alert alert-caution" role="alert">
        <h4 class="alert-heading">Javascript</h4>
        <p>Please enable javascript to see and search ML models.</p>
    </div>
</noscript>

To use an existing model from the registry, [deploy the ML model to your robot](/services/ml/deploy/) and use a [Vision service](/services/vision/) to make detections or classifications on-machine.

## ML training scripts

The Viam registry hosts custom Python ML training scripts, which you can use to train custom machine learning models.
You can also upload your own training script by following the guide to [Train a Model with a Custom Python Training Script](/services/ml/upload-training-script/#upload-a-new-training-script-or-new-version).

You can search the available ML training scripts from the Viam registry here:

<div id="searchboxScripts"></div>
<p>
<div id="searchstatsScripts"></div></p>
<div class="training-scripts" id="">
  <div class="modellistheader">
    <div class="name">Script</div>
    <div>Description</div>
  </div>
<div id="hitsScripts" class="modellist">
</div>
<div id="paginationScripts"></div>
</div>
<noscript>
    <div class="alert alert-caution" role="alert">
        <h4 class="alert-heading">Javascript</h4>
        <p>Please enable javascript to see and search ML custom training scripts.</p>
    </div>
</noscript>
