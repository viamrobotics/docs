---
title: "Micro-RDK Encoder Models"
linkTitle: "Encoder"
weight: 30
type: "docs"
description: "Support in the micro-RDK for encoders, a special type of sensor that measures rotation of a motor or joint."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components", "micro-rdk"]
no_list: true
aliases:
  - /micro-rdk/encoder/
# SMEs: Nick M., Gautham V.
---

An encoder is a special type of sensor that measures rotation of a motor or joint.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Encoder Component](/components/encoder/).

## Supported Models

For configuration information, click on one of the supported encoder model names:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`incremental`](incremental/) | A two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point |
| [`single`](single/) | A single pin "pulse output" encoder which returns its relative position but no direction |

Click on the model names above for configuration information.

## API

The micro-RDK [encoder API](/components/encoder/#api) supports only the following supported client SDK API methods, which operate the same ways as those in the full-featured RDK:

- [`ResetPosition()`](/components/encoder/#resetposition)
- [`GetPosition()`](/components/encoder/#getposition)
- [`GetProperties()`](/components/encoder/#getproperties)
