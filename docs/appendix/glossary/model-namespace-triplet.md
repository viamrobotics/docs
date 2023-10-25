---
title: Model Namespace Triplet
id: model-namespace-triplet
full_link:
short_description: namespace:repo-name:name or rdk:builtin:name
aka:
---

{{< glossary_tooltip term_id="model" text="Models" >}} are uniquely namespaced as colon-delimited-triplets in the form of `namespace:repo-name:name` for modular resources and `rdk:builtin:name` for built-in models.

The `repo-name` segment generally matches the name of the git repository of your modular resource, but you can also use it to identify a family of models.
For example:

- The `viam:camera:csi` model implements the `rdk:component:camera` API to support CSI cameras.
- The `rdk:builtin:gpio` model implements the `rdk:component:motor` API to support [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model implements the `rdk:component:motor` API to support [DMC4000](/components/motor/dmc4000/) motor controllers.
