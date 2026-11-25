---
title: Composite
capabilities: ["glossary", "docs"]
id: composite
full_link: /build-modules/composite-models/
short_description: A model that serves more than one resource API from one instance, such as a camera that is also a movement sensor.
---

A {{< glossary_tooltip term_id="model" text="model" >}} that serves more than one resource API from a single instance.

A user adds a composite to a machine with one config entry, under any one of its APIs.
The machine advertises it under each API with the same name, and clients reach it through each API's usual methods.
For example, one device can serve both `rdk:component:camera` and `rdk:component:movement_sensor`.

See [Composite models](/build-modules/composite-models/).
