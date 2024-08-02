---
title: Model
id: model
full_link:
short_description: A particular implementation of a resource. For example, UR5e is a model of the arm component subtype.
---

A particular implementation of a {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="subtype" text="subtype" >}} that implements its [API](/appendix/apis/).

Models allow you to control hardware or software of a similar category, such as motors, with a consistent set of methods as an interface, even if the underlying implementation differs.

For example, some _models_ of DC motors communicate using [GPIO](/components/board/), while other DC motors use serial protocols like the SPI bus.
Regardless, you can power any motor model that implements the `rdk:component:motor` API with the `SetPower()` method.

Models are either included with [`viam-server`](/installation/), provided in {{< glossary_tooltip term_id="module" text="custom modules" >}} available for download from the [Viam registry](https://app.viam.com/registry), or installed as [local modules](/registry/configure/#local-modules).
All models are uniquely namespaced as colon-delimited-triplets.
Built-in model names have the form `rdk:builtin:name`.
Modular resource model names have the form `namespace:repo-name:name`.
See [Name your new resource model](/use-cases/create-module/#name-your-new-resource-model) for more information.
