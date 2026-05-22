---
title: "Arm Component"
linkTitle: "Arm"
childTitleEndOverwrite: "Arm Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in arm models."
no_list: true
tags: ["arm", "components"]
icon: true
images: ["/icons/components/arm.svg"]
aliases:
  - "/components/arm/"
---

This section documents the configuration attributes for each built-in arm model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a arm component on your machine, see [Arm](/hardware/common-components/add-an-arm/).
- For the methods you call on a arm in code, see the [Arm API reference](/reference/apis/components/arm/).
- For arm models outside the built-in set, search for `arm` in the [Viam registry](https://app.viam.com/registry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following arm models ship with `viam-server`:

| Model           | Description                                          |
| --------------- | ---------------------------------------------------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
