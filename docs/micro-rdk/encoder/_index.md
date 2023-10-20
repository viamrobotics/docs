---
title: "Micro-RDK Encoder Models"
linkTitle: "Encoder"
weight: 30
type: "docs"
description: "Encoder support in the micro-rdk."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
---

## Supported Models

The micro-RDK currently supports the following models of Encoder:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`incremental`](incremental/) | A two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point |
| [`single`](single/) | A single pin "pulse output" encoder which returns its relative position but no direction |

Click on the model names above for configuration information.

## API

The [Encoder API](/components/encoder/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`ResetPosition()`](/components/encoder/#resetposition)
- [`GetPosition()`](/components/encoder/#getposition)
- [`GetProperties()`](/components/encoder/#getproperties)
