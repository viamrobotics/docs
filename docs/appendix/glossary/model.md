---
title: Model
id: model
full_link:
short_description: A particular implementation of a resource. For example, UR5e is a model of the arm component subtype.
aka:
---

A particular implementation of a {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="subtype" text="subtype" >}}.

For example: `ur5e` is a _model_ of arm, implementing the [resource API](/program/apis/) of the [arm](/components/arm/) subtype of {{< glossary_tooltip term_id="component" text="component" >}}, which, in turn, is a {{< glossary_tooltip term_id="type" text="type" >}} of resource.

## Models

A _model_ describes a specific implementation of a {{< glossary_tooltip term_id="resource" text="resource" >}} that implements (speaks) its [API](/program/apis/).
Models allow you to control hardware or software of a similar category, such as motors, with a consistent set of methods as an interface, even if the underlying implementation differs.

For example, some DC motors communicate using [GPIO](/components/board/), while other DC motors use serial protocols like the [SPI bus](/components/board/#spis).
Regardless, you can power any motor model that implements the `rdk:component:motor` API with the `SetPower()` method.

Models are uniquely namespaced as colon-delimited-triplets.
Modular resource model names have the form `namespace:repo-name:name`.
Built-in model names have the form `rdk:builtin:name`.
See [Naming your model](#naming-your-model-namespacerepo-namename) for more information.

Models are either:

- Built into the RDK, and included when you [install `viam-server`](/installation/) or when you use one of the [Viam SDKs](/program/apis/).
- Provided in {{< glossary_tooltip term_id="module" text="custom modules" >}} available for download from the [Viam registry](https://app.viam.com/registry), and are written by either Viam or community users.
  Custom modules can also be [local](/registry/configure/#local-modules).

### Built-in models

Viam provides many built-in models that implement API capabilities, each using `rdk` as the `namespace`, and `builtin` as the `family`.
These models run within `viam-server`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

### Custom models

The [Viam registry](https://app.viam.com/registry) makes available both Viam-provided and community-written modules for download and use on your robot.
You can also run modules [locally](/registry/configure/#local-modules).
These models run outside `viam-server` as a separate process.

#### Naming your model: namespace:repo-name:name

If you are [creating a custom module](/registry/create/) and [uploading that module](/registry/upload/) to the Viam registry, ensure your model name meets the following requirements:

- The namespace of your model **must** match the [namespace of your organization](/manage/fleet/organizations/#create-a-namespace-for-your-organization).
  For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:demo:mybase`.
- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

For the middle segment of your model triplet `repo-name`, use the name of the git repository where you store your module's code.
The `repo-name` should describe the common functionality provided across the model or models of that module.

For example:

- The `rand:yahboom:arm` model and the `rand:yahboom:gripper` model uses the repository name [yahboom](https://github.com/viam-labs/yahboom).
  The models implement the `rdk:component:arm` and the `rdk:component:gripper` API to support the Yahboom DOFBOT arm and gripper, respectively.
- The `viam-labs:audioout:pygame` model uses the repository name [audioout](https://github.com/viam-labs/audioout)
  It implements the custom API `viam-labs:service:audioout`.

The `viam` namespace is reserved for models provided by Viam.
