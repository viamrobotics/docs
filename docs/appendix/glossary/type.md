---
title: Type
id: type
full_link:
short_description: Component and service are the built-in types of resource API the RDK provides.
aka:
---

In the {{< glossary_tooltip term_id="rdk" text="RDK" >}} architecture's {{< glossary_tooltip term_id="api-namespace-triplet" text="namespace triplet" >}} for resource APIs, _type_ refers to the distinction between {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}}.

However, the meaning of "type" can be context dependent across the Viam platform.

For example, when [configuring a robot](/build/configure/) in the [Viam app](https://app.viam.com), `"type"` is used in the JSON to indicate a particular implementation of a component or service, which is formally designated as the {{< glossary_tooltip term_id="subtype" text="subtype" >}}.
