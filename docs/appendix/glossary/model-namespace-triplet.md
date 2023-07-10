---
title: Model Namespace Triplet
id: model-namespace-triplet
full_link:
short_description: namespace:family:name
aka:
---

A model is a specific implementation of a resource that implements (speaks) its API.
Models allow you to control different versions of resource types with a consistent interface.

Models of a {{< glossary_tooltip term_id="resource" text="resource" >}} are uniquely namespaced as colon-delimited-triplets in the form of `namespace:family:name`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.
