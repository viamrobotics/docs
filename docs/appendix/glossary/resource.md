---
title: Resource
id: resource
full_link:
short_description: Resources are individual, addressable elements of a robot such as components or services.
aka:
---

Resources are individual, addressable elements of a robot.

{{< glossary_tooltip term_id="part" text="Parts" >}} can operate multiple types of resources:

- physical {{< glossary_tooltip term_id="component" text="components" >}}
- software {{< glossary_tooltip term_id="service" text="services" >}}
- {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} provided by {{< glossary_tooltip term_id="module" text="modules" >}}
- {{< glossary_tooltip term_id="process" text="processes" >}}

Each part has local resources and can also have resources from another {{< glossary_tooltip term_id="remote" text="remote">}} robot part.
The capabilities of each resource are exposed through the part’s API.

Each resource on your robot implements either one of the [existing Viam APIs](/modular-resources/create/#valid-apis-to-implement-in-your-model), or a [custom interface](/modular-resources/advanced/#new-api-subtypes).
