---
title: "Base Component"
linkTitle: "Base"
childTitleEndOverwrite: "Base Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in base models."
no_list: true
tags: ["base", "components"]
icon: true
images: ["/icons/components/base.svg"]
aliases:
  - "/components/base/"
---

This section documents the configuration attributes for each built-in base model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a base component on your machine, see [Base](/hardware/common-components/add-a-base/).
- For the methods you call on a base in code, see the [Base API reference](/reference/apis/components/base/).
- For base models outside the built-in set, search for `base` in the [Viam registry](https://app.viam.com/registry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following base models ship with `viam-server`:

| Model                                     | Description                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------------ |
| [`fake`](fake/)                           | A model used for testing, with no physical hardware.                                       |
| [`sensor-controlled`](sensor-controlled/) | Wrap other base models and add feedback control using a movement sensor.                   |
| [`wheeled`](wheeled/)                     | Supports mobile wheeled robotic bases with motors on both sides for differential steering. |

## Micro-RDK models

The following base models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                                             | Description |
| ------------------------------------------------- | ----------- |
| [`two_wheeled_base`](micro-rdk/two_wheeled_base/) | —           |
