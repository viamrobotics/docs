---
title: API Namespace Triplet
id: api-namespace-triplet
full_link:
short_description: namespace:type:subtype, for example `rdk:component:sensor`
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} implements an [application programming interface (API)](https://en.wikipedia.org/wiki/API) that describes how you can interact with that resource.

These APIs are organized by colon-delimited-triplet identifiers, in the form of `namespace:type:subtype`.

The `namespace` for built-in Viam resources is `rdk`, while the `type` is `component` or `service`.
`subtype` refers to a specific component or service, like a `camera` or `vision`.

One API can have various {{< glossary_tooltip term_id="model" text="models" >}}, custom or built-in, but they all must conform to the same API definition.
This requirement ensures that when a resource of that model is deployed, you can [interface with it](/dev/reference/sdks/) using the same [client API methods](/dev/reference/apis/) you would when programming resources of the same API with a different model.

Each resource implements one and only one API.

For example:

- The API of the built-in component [camera](/operate/reference/components/camera/) is `rdk:component:camera`, which exposes methods such as `GetImages()`.
- The API of the built-in service [vision](/operate/reference/services/vision/) is `rdk:service:vision`, which exposes methods such as `GetDetectionsFromCamera()`.
