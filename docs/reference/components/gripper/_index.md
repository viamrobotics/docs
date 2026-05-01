---
title: "Gripper Component"
linkTitle: "Gripper"
childTitleEndOverwrite: "Gripper Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in gripper models."
no_list: true
tags: ["gripper", "components"]
icon: true
images: ["/icons/components/gripper.svg"]
aliases:
  - "/components/gripper/"
---

This section documents the configuration attributes for each built-in gripper model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a gripper component on your machine, see [Gripper](/hardware/common-components/add-a-gripper/).
- For the methods you call on a gripper in code, see the [Gripper API reference](/reference/apis/components/gripper/).
- For gripper models outside the built-in set, search for `gripper` in the [Viam registry](https://app.viam.com/registry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following gripper models ship with `viam-server`:

| Model           | Description                                          |
| --------------- | ---------------------------------------------------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
