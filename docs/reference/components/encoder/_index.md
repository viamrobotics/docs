---
title: "Encoder Component"
linkTitle: "Encoder"
childTitleEndOverwrite: "Encoder Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in encoder models."
no_list: true
tags: ["encoder", "components"]
icon: true
images: ["/icons/components/encoder.svg"]
aliases:
  - "/components/encoder/"
---

This section documents the configuration attributes for each built-in encoder model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a encoder component on your machine, see [Encoder](/hardware/common-components/add-an-encoder/).
- For the methods you call on a encoder in code, see the [Encoder API reference](/reference/apis/components/encoder/).
- For encoder models outside the built-in set, browse the [Viam registry](https://app.viam.com/registry?type=component&subtype=encoder). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following encoder models ship with `viam-server`:

| Model                         | Description                                                                                                                 |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [`arduino`](arduino/)         | —                                                                                                                           |
| [`fake`](fake/)               | An encoder model for testing.                                                                                               |
| [`incremental`](incremental/) | Supports a two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point. |
| [`single`](single/)           | A single pin 'pulse output' encoder which returns its relative position but no direction.                                   |

## Micro-RDK models

The following encoder models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                                   | Description |
| --------------------------------------- | ----------- |
| [`incremental`](micro-rdk/incremental/) | —           |
| [`single`](micro-rdk/single/)           | —           |
