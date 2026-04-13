---
title: Model
id: model
full_link:
short_description: A particular implementation of a resource. For example, UR5e is a model of the arm component API.
aliases:
  - /dev/reference/glossary/model/
---

A particular implementation of a {{< glossary_tooltip term_id="resource" text="resource" >}} [API](/reference/apis/).

Models allow you to control hardware or software of a similar category, such as motors, with a consistent set of methods as an interface, even if the underlying implementation differs.

For example, some _models_ of DC motors communicate using [GPIO](/reference/components/board/), while other DC motors use serial protocols like the SPI bus.
Regardless, you can power any motor model that implements the `rdk:component:motor` API with the `SetPower()` method.

Models are either included with [`viam-server`](/reference/viam-server/) or provided through {{< glossary_tooltip term_id="module" text="modules" >}}.
All models are uniquely namespaced as colon-delimited-triplets.
Built-in model names have the form `rdk:builtin:name`.
Modular resource model names have the form `namespace:module-name:model-name`.
See [Write your module](/operate/modules/write-a-driver-module/#2-implement-the-resource-api) for more information.
