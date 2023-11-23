---
title: "Robot Development Kit"
linkTitle: "Robot Development Kit"
weight: 1
type: "docs"
description: "The RDK is the open-source, on-robot portion of the Viam platform, that provides viam-server and the Go SDK."
tags: ["server", "rdk"]
aliases:
  - "/product-overviews/rdk"
  - "/program/rdk"
  - "/internals/rdk"
---

{{< alert title="Tip" color="tip" >}}
For an overview of the Viam platform, see [Viam in 3 minutes](/viam/).
{{< /alert >}}

Viam’s Robot Development Kit (RDK) is the [open-source](https://github.com/viamrobotics/rdk), on-robot portion of the Viam platform, that provides `viam-server` and the Go SDK.

## `viam-server`

_viam-server_ manages the following:

### Communication

`viam-server` handles all {{< glossary_tooltip term_id="grpc" text="gRPC" >}} and {{< glossary_tooltip term_id="webrtc" >}} communication for connecting robots to the cloud or for connecting to other parts of your machine.

### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

### Start-up

`viam-server` ensures that any configured {{< glossary_tooltip term_id="module" text="modules" >}}, {{< glossary_tooltip term_id="resource" text="built-in resources" >}} and {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, and processes are loaded on startup.

After start-up, `viam-server` manages:

- the configured processes,
- the connections to hardware,
- the running services, and
- the {{< glossary_tooltip term_id="module" text="modules" >}} that provide the {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}.

### Reconfiguration

When you or your collaborators change the configuration of a machine in the Viam app, `viam-server` automatically synchronizes the configuration to your machine and updates the running resources within 15 seconds.
This means you can add, modify, and remove a modular resource instance from a running robot.

You can see configuration changes made by yourself or by your collaborators on the [History tab](/manage/fleet/robots/#history).
You can also revert to an earlier configuration from the History tab.

### Logging

Log messages written appear under the [**Logs** tab](/manage/fleet/robots/#logs) for the machine running the module.

### Data management

Data capture for individual components is supported on [certain component subtypes](/services/data/configure-data-capture/#configure-data-capture-for-individual-components).

### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

## Next Steps

{{< cards >}}
{{% card link="/program/apis/" %}}
{{% card link="/registry/" %}}
{{% card link="/micro-rdk/" %}}
{{< /cards >}}
