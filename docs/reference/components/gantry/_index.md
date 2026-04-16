---
title: "Gantry Component"
linkTitle: "Gantry"
childTitleEndOverwrite: "Gantry Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in gantry models."
no_list: true
tags: ["gantry", "components"]
icon: true
images: ["/icons/components/gantry.svg"]
aliases:
  - "/components/gantry/"
---

This section documents the configuration attributes for each built-in gantry model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a gantry component on your machine, see [Gantry](/hardware/common-components/add-a-gantry/).
- For the methods you call on a gantry in code, see the [Gantry API reference](/reference/apis/components/gantry/).
- For gantry models outside the built-in set, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=gantry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following gantry models ship with `viam-server`:

| Model | Description |
| ----- | ----------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
| [`multi-axis`](multi-axis/) | Supports a gantry with multiple linear rails. Composed of multiple single-axis gantries. |
| [`single-axis`](single-axis/) | Supports a gantry with a singular linear rail. |
