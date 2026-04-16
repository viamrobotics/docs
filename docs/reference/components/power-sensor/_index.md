---
title: "Power Sensor Component"
linkTitle: "Power sensor"
childTitleEndOverwrite: "Power Sensor Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in power sensor models."
no_list: true
tags: ["power-sensor", "components"]
icon: true
images: ["/icons/components/power-sensor.svg"]
aliases:
  - "/components/power-sensor/"
---

This section documents the configuration attributes for each built-in power sensor model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a power sensor component on your machine, see [Power sensor](/hardware/common-components/add-a-power-sensor/).
- For the methods you call on a power sensor in code, see the [Power sensor API reference](/reference/apis/components/power-sensor/).
- For power sensor models outside the built-in set, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=power_sensor). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following power sensor models ship with `viam-server`:

| Model | Description |
| ----- | ----------- |
| [`fake`](fake/) | A model for testing, with no physical hardware. |
