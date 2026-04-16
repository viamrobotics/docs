---
title: "Generic Component"
linkTitle: "Generic"
childTitleEndOverwrite: "Generic Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in generic models."
no_list: true
tags: ["generic", "components"]
icon: true
images: ["/icons/components/generic.svg"]
aliases:
  - "/components/generic/"
---

This section documents the configuration attributes for each built-in generic model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a generic component on your machine, see [Generic](/hardware/common-components/add-a-generic/).
- For the methods you call on a generic in code, see the [Generic API reference](/reference/apis/components/generic/).
- For generic models outside the built-in set, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=generic). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following generic models ship with `viam-server`:

| Model | Description |
| ----- | ----------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
