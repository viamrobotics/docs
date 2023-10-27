---
title: Model Namespace Triplet
id: model-namespace-triplet
full_link: /modular-resources/key-concepts/#naming-your-model-namespacerepo-namename
short_description: namespace:repo-name:name or rdk:builtin:name
aka:
---

{{< glossary_tooltip term_id="model" text="Models" >}} are uniquely namespaced as colon-delimited-triplets in the form of `namespace:repo-name:name` for modular resources and `rdk:builtin:name` for built-in models.

For more information see [Naming your model](/modular-resources/key-concepts/#naming-your-model-namespacerepo-namename).

Built-in {{< glossary_tooltip term_id="rdk" text="rdk" >}} models use the triplet `rdk:builtin:name`.
For example:

- The `rdk:builtin:gpio` model.
  It implements the `rdk:component:motor` API to support [GPIO-controlled DC motors](/components/motor/gpio/).
