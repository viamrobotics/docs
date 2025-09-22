---
title: "Lifecycle of a module"
linkTitle: "Lifecycle of a module"
weight: 50
layout: "docs"
type: "docs"
description: "Learn about the lifecycle of a module: How and when it starts, shuts down, and reconfigures."
---

Modules run on your machine, alongside `viam-server` as separate processes, communicating with `viam-server` over UNIX sockets.

[`viam-server` manages](/operate/reference/viam-server/) the dependencies, start-up, reconfiguration, [data management](/data-ai/capture-data/capture-sync/), and shutdown behavior of your modular resource.

The lifecycle of a module and the resources it provides is as follows:

1. `viam-server` starts, and if it is connected to the internet, it checks for configuration updates.

1. `viam-server` starts any configured modules.

1. When a module initializes, it registers its model or models and associated [APIs](/dev/reference/apis/) with `viam-server`, making the models available for use.

1. For each modular resource configured on the machine, `viam-server` uses the resource's `validate` function and the `depends_on` field in the resource configuration to determine the [dependencies](/operate/modules/other-hardware/create-module/dependencies/) of the resource.

1. If a required dependency is not already running, `viam-server` starts it before starting the resource.
   If a required dependency is not found or fails to start, `viam-server` will not start the resource that depends on it.

1. `viam-server` calls the resource's constructor to build the resource based on its configuration.
   Typically, the constructor calls the reconfigure function.

1. If construction or reconfiguration fails due to a validation failure or an exception thrown by the modular resource's constructor or its reconfigure method, `viam-server` attempts to construct or reconfigure the resource every 5 seconds.
   If the module exceeds the [configured timeout limits](/operate/modules/other-hardware/module-configuration/#environment-variables) (default 5 minutes to start up and 1 minute to reconfigure), `viam-server` logs an [error](/dev/tools/common-errors/#timed-out-waiting-for-module).

1. Once the modular resource has started up and configured, it is available for use.

1. If at any point the user changes the configuration of the machine, `viam-server` reconfigures the affected resources within 15 seconds.

1. If `viam-server` attempts to shut down an individual module (for example due to a user disabling a module) and the module does not shut down within 30 seconds, `viam-server` kills the module.

1. When `viam-server` shuts down, it first attempts to shut down each module sequentially in no particular order.
   If a given module does not shut down within 30 seconds, it is killed with a `SIGKILL`.
   If any modules are still running after 90 seconds, `viam-server` kills them as well.
   This means that if four modules are running and the first three each fail to shut down within 30 seconds each, the fourth is killed immediately at the 90 second mark.

Microcontroller modules function differently and are embedded in the firmware you flash onto your device.
For more information see [Modules for ESP32](/operate/modules/other-hardware/micro-module/).
