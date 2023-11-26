---
title: Subtype
id: subtype
full_link:
short_description: A group of component or service models that share the same API. For example, arm is a subtype of component.
aka:
---

A category within a {{< glossary_tooltip term_id="type" text="type" >}} of {{< glossary_tooltip term_id="resource" text="resource" >}}.
Resource models belonging to a subtype share the same API.
{{< glossary_tooltip term_id="model" text="Models" >}} implement that subtype's API protocol with different drivers.

For example, an arm is a subtype of the {{< glossary_tooltip term_id="component" text="component" >}} resource type, while the `ur5e` is a {{< glossary_tooltip term_id="model" text="model" >}} of the arm subtype's API.

The [Vision Service](/ml/vision/) is a subtype of the {{< glossary_tooltip term_id="service" text="service" >}} resource type.

A subtype is designated by its {{< glossary_tooltip term_id="api-namespace-triplet" text="api-namespace-triplet" >}}.
