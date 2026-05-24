---
title: "Board Component"
linkTitle: "Board"
childTitleEndOverwrite: "Board Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in board models."
no_list: true
tags: ["board", "components"]
icon: true
images: ["/icons/components/board.svg"]
aliases:
  - "/components/board/"
---

This section documents the configuration attributes for each built-in board model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a board component on your machine, see [Board](/hardware/common-components/add-a-board/).
- For the methods you call on a board in code, see the [Board API reference](/reference/apis/components/board/).
- For board models outside the built-in set, search for `board` in the [Viam registry](https://app.viam.com/registry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following board models ship with `viam-server`:

| Model           | Description                                          |
| --------------- | ---------------------------------------------------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |

## Micro-RDK models

The following board models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                       | Description |
| --------------------------- | ----------- |
| [`esp32`](micro-rdk/esp32/) | —           |
