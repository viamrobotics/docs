---
title: API Namespace Triplet
id: api-namespace-triplet
full_link:
short_description: namespace:type:subtype
aka:
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} type exposes an [application programming interface (API)](https://en.wikipedia.org/wiki/API) to describe how you can interact with that resource.

Each Viam resource's API is uniquely namespaced as a colon-delimited-triplet in the form of `namespace:type:subtype`.

For example:

- The API of the built-in component [camera](/components/camera/) is `rdk:component:camera`, which exposes methods such as `GetImage()`.
- The API of the built-in service [vision](/services/vision/) is `rdk:service:vision`, which exposes methods such as `GetDetectionsFromCamera()`.
