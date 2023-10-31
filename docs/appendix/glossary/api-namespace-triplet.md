---
title: API Namespace Triplet
id: api-namespace-triplet
full_link:
short_description: namespace:type:subtype
aka:
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="subtype" text="subtype" >}} exposes an [application programming interface (API)](https://en.wikipedia.org/wiki/API) to describe how you can interact with that resource.

These APIs are organized by colon-delimited-triplet identifiers, in the form of `namespace:type:subtype`.

The `namespace` for built-in Viam resources is `rdk`, while the `type` is `component` or `service`.
`subtype` refers to a specific component or service, like a `camera` or `vision`.

One subtype can have various {{< glossary_tooltip term_id="model" text="models" >}}, custom or built-in, but they all must conform to the subtype's API definition.
This requirement ensures that when a resource of that model is deployed, you can [interface with it](/program/) using the same [client API methods](/program/apis/) you would when programming resources of the same subtype with a different model.

For example:

- The API of the built-in component [camera](/components/camera/) is `rdk:component:camera`, which exposes methods such as `GetImage()`.
- The API of the built-in service [vision](/services/vision/) is `rdk:service:vision`, which exposes methods such as `GetDetectionsFromCamera()`.
