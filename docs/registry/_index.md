---
title: "Extend Viam with Models from the Viam Registry"
linkTitle: "Registry"
weight: 420
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
description: "Add additional models of components and services or ML Models from the Viam Registry, or extend Viam by creating new modular resources."
image: "/services/icons/modular-registry.svg"
imageAlt: "Integrate other capabilities."
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

The [Viam registry](https://app.viam.com/registry) is the central place where you can browse [ML models](/ml) to deploy with machine applications like [computer vision](/ml/vision/), or {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} that add capabilities to your machine beyond what is built-in to `viam-server`.

### ML models

Viam provides the ability to train, upload, and deploy ML models within the platform.
See [Machine Learning](/ml/) for more information.

You can use these ML models to make detections or classifications on-machine with an [`mlmodel` vision service](/ml/vision/mlmodel/).

The Viam registry hosts pretrained ML models that users have made public, so that you can save time spent training complicated models and quickly deploy functional classifiers or detectors for your use case onto your robot.
You can also upload your own model to the registry.

- You can deploy a model to your robot through an [MLModel service like `tflite_cpu`](/ml/deploy/).
Select **Builder** and **Deploy Model** tabs and follow [these instructions](/ml/deploy/#create-an-ml-model-service) to deploy the model to your robot.
- To add an ML model to the registry, [upload the model publicly](/ml/upload-model/).

### Modular resources

Viam provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware {{< glossary_tooltip term_id="component" text="components" >}}.
- High-level functionality exposed as {{< glossary_tooltip term_id="service" text="services" >}}.

If the model of component or service you want to use for your project is not built-in to `viam-server` and available for configuration by default, you can use a {{< glossary_tooltip term_id="model" text="model" >}} from a {{< glossary_tooltip term_id="module" text="module" >}}.

To configure a modular resource on your robot, [add new models that others have created](/registry/configure/#add-a-modular-resource-from-the-viam-registry) from the [Viam registry](https://app.viam.com/registry) or [create your own](#create-your-own-modules).

You can search the available modular resources from the Viam Registry here:

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

You can see details about each module in the [Viam registry](https://app.viam.com/registry) on its dedicated module page.
You can integrate modules into any Viam-powered machine.

Be aware that unlike natively supported models, modular resources are not documented on the Viam Documentation.
Documentation for each modular resource is available on its GitHub page, which is linked from the models' page on [the registry](https://app.viam.com/registry).

## Use modules

To use a modular resource from the registry, add it from your machine's **Config** tab in the Viam app, using the **Create component** button.

After adding a module to your machine, you can choose to [configure](/registry/configure/) it for automatic version updates from the Viam registry, or update your module manually.
By default, newly added modules will remain at the version they were when you installed them, and will not update automatically.

Once you have added and configured the module you would like to use in the Viam app, you can test your added resource using the [**Control** tab](/fleet/#remote-control) and program it using [standardized APIs](/build/program/apis/).

`viam-server` manages the [dependencies](/internals/rdk/#dependency-management), [start-up](/internals/rdk/#start-up), [reconfiguration](/fleet/#reconfiguration), [data management](/data/capture/#configure-data-capture-for-individual-components), and [shutdown](/internals/rdk/#shutdown) behavior of your modular resource.

### Tutorials using modules

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" %}}
{{< /cards >}}

## Create your own modules

If none of the existing modular resources in the Viam registry support your use case, you can create your own modules with your own modular resources:

- **Implement a custom component**: Write a driver for an unsupported {{< glossary_tooltip term_id="component" text="component" >}} by implementing the corresponding component API.

- **Implement a custom service**: Implement your own algorithm or {{< glossary_tooltip term_id="model" text="model" >}} against a corresponding service API or use custom algorithms or data models when working with services such as {{< glossary_tooltip term_id="slam" text="SLAM" >}}, vision, or motion planning.

You can write modules in a variety of programming languages, such as, Go, Python, C++, Rust, while implementing the same [APIs](/build/program/apis/).
To create a new module:

1. [Create a module](/registry/create/) with one or more modular resources by implementing all methods for the component's or service's standardized API.
1. [Upload the module to the Viam registry](/registry/upload/) to make it available for deployment to machines or add it as a [local module](/registry/configure/#local-modules).
   You can upload _private_ modules for your {{< glossary_tooltip term_id="organization" text="organization" >}} or _public_ modules.
1. Once you have uploaded your module to the registry, [deploy and configure the module](/registry/configure/) from the Viam app.
   Then, you can test your added resource using the [**Control** tab](/fleet/#remote-control) and [program](/build/program/) it with Viam's Go or Python SDKs.

## Naming your model: namespace:repo-name:name

If you are [creating a custom module](/registry/create/) and want to [upload that module](/registry/upload/) to the Viam registry, ensure your model name meets the following requirements:

- The namespace of your model **must** match the [namespace of your organization](/fleet/organizations/#create-a-namespace-for-your-organization).
  For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:repo-name:mybase`.
- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

For the middle segment of your model triplet `repo-name`, use the name of the Git repository where you store your module's code.
Ideally, your `repo-name` should describe the common functionality provided across the model or models of that module.

For example:

- The `rand:yahboom:arm` model and the `rand:yahboom:gripper` model use the repository name [yahboom](https://github.com/viam-labs/yahboom).
  The models implement the `rdk:component:arm` and the `rdk:component:gripper` API to support the Yahboom DOFBOT arm and gripper, respectively:

  ```json
  {
      "api": "rdk:component:arm",
      "model": "rand:yahboom:arm"
  },
  {
      "api": "rdk:component:gripper",
      "model": "rand:yahboom:gripper"
  }
  ```

- The `viam-labs:audioout:pygame` model uses the repository name [audioout](https://github.com/viam-labs/audioout).
  It implements the custom API `viam-labs:service:audioout`:

  ```json
  {
    "api": "viam-labs:service:audioout",
    "model": "viam-labs:audioout:pygame"
  }
  ```

The `viam` namespace is reserved for models provided by Viam.

### Valid APIs to implement in your model

When implementing a custom {{< glossary_tooltip term_id="model" text="model" >}} of an existing {{< glossary_tooltip term_id="component" text="component" >}}, valid [APIs](/build/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component), for example `motor`

When implementing a custom {{< glossary_tooltip term_id="model" text="model" >}} of an existing [service](/services/), valid [APIs](/build/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service), for example `navigation`

### Tutorials creating modules

{{< cards >}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{% card link="/registry/examples/custom-arm/" %}}
{{< /cards >}}
