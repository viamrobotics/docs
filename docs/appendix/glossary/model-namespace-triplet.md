---
title: Model Namespace Triplet
id: model-namespace-triplet
full_link:
short_description: namespace:repo-name:name or rdk:builtin:name
aka:
---

{{< glossary_tooltip term_id="model" text="Models" >}} are uniquely namespaced as colon-delimited-triplets in the form of `namespace:repo-name:name` for modular resources and `rdk:builtin:name` for built-in models.

We recommend to use the name of the git repository of your modular resource as the middle segment.
The `repo-name` should describe the common functionality provided across the model or models of that module.

For example:

- The `rand:yahboom:arm` model uses the repository name [yahboom](https://github.com/viam-labs/yahboom).
  It implements the `rdk:component:arm` API to support the yahboom dofbot arm.
- The `viam-labs:audioout:pygame` model uses the repository name [audioout](https://github.com/viam-labs/audioout)
  It implements the custom API `viam-labs:service:audioout`.

Built-in {{< glossary_tooltip term_id="rdk" text="rdk" >}} models use the triplet `rdk:builtin:name`.
For example:

- The `rdk:builtin:gpio` model.
  It implements the `rdk:component:motor` API to support [GPIO-controlled DC motors](/components/motor/gpio/).
