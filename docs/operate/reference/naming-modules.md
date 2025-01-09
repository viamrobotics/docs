---
title: "Valid Module Identifiers"
linkTitle: "Module Naming"
type: "docs"
weight: 25
images: ["/registry/module-puzzle-piece.svg"]
tags: ["modular resources", "components", "services", "registry"]
description: "Add support for a new component or service model by writing a module in C++."
languages: ["c++"]
viamresources: []
platformarea: ["registry"]
toc_hide: true
---

Each modular resource has two associated triplets: an API namespace triplet to indicate which [API](/dev/reference/apis/) it implements, and a model namespace triplet to uniquely identify the modular resource {{< glossary_tooltip term_id="model" text="model" >}}.

## Valid API identifiers

Each existing component or service API has a unique identifier in the form of a colon-delimited triplet.
You will use this {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet" >}} when creating your new model, to indicate which API it uses.

The API namespace triplet is the same for all built-in and modular models that implement a given API.
For example, every model of motor built into Viam, as well as every custom model of motor provided by a module, all use the same API namespace triplet `rdk:component:motor` to indicate that they implement the [motor API](/operate/reference/components/motor/#api).

The three pieces of the API namespace triplet are as follows:

{{< tabs >}}
{{% tab name="Component" %}}

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component), for example `motor` if you are creating a new model of motor

{{% /tab %}}
{{% tab name="Service" %}}

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service), for example `vision` if you are creating a new model of vision service

{{% /tab %}}
{{< /tabs >}}

## Valid model identifiers

In addition to determining which existing API namespace triplet to use when creating your module, you need to decide on a separate triplet unique to your model.

{{< expand "API namespace triplet and model namespace triplet examples" >}}

- The `rand:yahboom:arm` model and the `rand:yahboom:gripper` model use the module name (and matching repo name) [yahboom](https://github.com/viam-labs/yahboom).
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

{{< /expand >}}

The `viam` namespace is reserved for models provided by Viam.

A resource model is identified by a unique name, called the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, using the format: `namespace:module-name:model-name`, where:

- `namespace` is the namespace of your organization, which you can find or [create](#create-a-namespace-for-your-organization) in your organization settings page in the [Viam app](https://app.viam.com).
  - For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:module-name:mybase`.
    If you do not intend to [upload your module](/operate/get-started/other-hardware/#upload-your-module) to the [Viam Registry](https://app.viam.com/registry), you do not need to use your organization's namespace as your model's namespace.
  - The `viam` namespace is reserved for models provided by Viam.
- `module-name` is the name of your module.
  Your `module-name` should describe the common functionality provided across the model or models provided by that module.
  - Many people also choose to use the module name as the name of the code repository (GitHub repo) that houses the module code.
- `model-name` is the name of the new resource model that your module will provide.

For example, if your organization namespace is `acme`, and you have written a new base implementation named `mybase` which you have supported with a module named `my-custom-base-module`, you would use the namespace `acme:my-custom-base-module:mybase` for your model.

More requirements:

- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

Determine the model name you want to use based on these requirements, then proceed to the next section.

## Create a namespace for your organization

When uploading modules to the Viam Registry, you must set a unique namespace for your organization to associate your module with.

To create a new namespace for your organization, click on the org's **Settings** in the top right of the navigation bar, then click the **Set a public namespace** button.
Enter a name or use the suggested name for your namespace, and then click **Set namespace**.
A namespace may only contain letters, numbers, and the dash (`-`) character.
