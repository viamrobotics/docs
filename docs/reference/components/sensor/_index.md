---
title: "Sensor Component"
linkTitle: "Sensor"
childTitleEndOverwrite: "Sensor Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in sensor models."
no_list: true
tags: ["sensor", "components"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/sensor/"
---

This section documents the configuration attributes for each built-in sensor model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a sensor component on your machine, see [Sensor](/hardware/common-components/add-a-sensor/).
- For the methods you call on a sensor in code, see the [Sensor API reference](/reference/apis/components/sensor/).
- For sensor models outside the built-in set, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=sensor). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following sensor models ship with `viam-server`:

| Model           | Description                                          |
| --------------- | ---------------------------------------------------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |

## Micro-RDK models

The following sensor models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                                 | Description |
| ------------------------------------- | ----------- |
| [`ultrasonic`](micro-rdk/ultrasonic/) | —           |
