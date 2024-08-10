---
title: "How to create a sensor module with Python"
linkTitle: "Create a sensor module"
type: "docs"
weight: 26
images: ["/icons/components/sensor.svg"]
tags: ["modular resources", "components", "services", "registry"]
description: "Add a custom resource by creating and deploying a module to your machine."
---

A sensor is anything that collects data.

A sensor could be something we typically think of as a sensor, like a temperature and humidity sensor, or it could be a "virtual," non-hardware sensor like a service that gets stock market data.

Since a sensor can be so many different things, there's a good likelihood you're on this page because though there are various [built-in and modular sensor models available in Viam](/components/sensor/#available-models), you have a different, unsupported sort of sensor you'd like to use.

Making a module to support your sensor will allow you to use it with Viam's data capture and sync tools, as well as using the sensor API (using any of the different programming language [SDKs](/sdks/)) to get readings from it.

## Get something working

Start by getting a test script working so you can check that the code itself works before packaging it into a module.

Since this how-to uses Python, you need a Python test script so that you can more easily wrap it in a Python-based module.
You'll still be able to use any of Viam's SDKs with the module.

This step depends completely on your sensor hardware (or software)--just write some script that gets readings from the sensor.

An example for an air quality sensor:

```python
import

```

<details>
  <summary>Another example (this is for a base, not a sensor)</summary>

An example from the [custom robot dog base tutorial](/tutorials/custom/custom-base-dog/):

```python
# dog_test.py is for testing the connection
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("PASTE DOG IP ADDRESS HERE", 5001))

cmd = "CMD_MOVE_FORWARD#15"
s.send(cmd.encode("utf-8"))
time.sleep(7)
cmd = "CMD_MOVE_STOP"
s.send(cmd.encode("utf-8"))
cmd = "CMD_RELAX"
s.send(cmd.encode("utf-8"))
```

</details>

## Understand the sensor API

{{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet" >}}: `rdk:component:sensor`

You need to implement `GetReadings()`.
