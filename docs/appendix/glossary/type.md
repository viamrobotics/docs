---
title: Type (Resource Type)
id: type
full_link:
short_description: A group of component or service models that share the same API.
aka:
---

Every {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}} has a type and a {{< glossary_tooltip term_id="model" text="model" >}}.
All {{< glossary_tooltip term_id="resource" text="resources" >}} of a given type have the same API.
Models are subcategories within that type, implementing the common API.

For example, `gpio` and `gpiostepper` are both models of type `motor`, and they are both controlled through the [motor API](/components/motor/#api).
