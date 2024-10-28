---
title: "viam-server"
linkTitle: "viam-server"
weight: 80
type: "docs"
description: "viam-server is the open-source, on-machine portion of the Viam platform."
tags: ["server", "rdk"]
aliases:
  - "/product-overviews/rdk"
  - "/build/program/rdk"
  - /internals/rdk/
  - /architecture/rdk/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The `viam-server` executable runs on a computer and manages hardware, software, and data for a machine.
`viam-server` is built from the open-source [Robot Development Kit (RDK)](https://github.com/viamrobotics/rdk).
If you are working with microcontrollers, [`viam-micro-server`](/architecture/viam-micro-server/) is a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured `viam-server`.

To use Viam with a machine, you create a configuration specifying which hardware and software the machine consists of.
`viam-server` then manages and runs the drivers for the configured {{< glossary_tooltip term_id="resource" text="resources" >}}.

Overall, _viam-server_ manages:

- [Communication](#communication)
- [Dependency management](#dependency-management)
- [Start-up](#start-up)
- [Reconfiguration](#reconfiguration)
- [Logging](#logging)
- [Shutdown](#shutdown)

## Communication

`viam-server` handles all {{< glossary_tooltip term_id="grpc" text="gRPC" >}} and {{< glossary_tooltip term_id="webrtc" >}} communication for connecting machines to the cloud or for connecting to other parts of your machine.

## Dependency management

`viam-server` handles dependency management between resources.

## Start-up

`viam-server` ensures that any configured {{< glossary_tooltip term_id="module" text="modules" >}}, {{< glossary_tooltip term_id="resource" text="built-in resources" >}} and {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, and processes are loaded on startup.

After start-up, `viam-server` manages:

- the configured processes,
- the connections to hardware,
- the running services, and
- the {{< glossary_tooltip term_id="module" text="modules" >}} that provide the {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}.

### Reconfiguration

When you or your collaborators change the configuration of a machine in the Viam app, `viam-server` automatically synchronizes the configuration to your machine and updates the running resources within 15 seconds.
This means you can add, modify, and remove a modular resource instance from a running machine.

You can see configuration changes made by yourself or by your collaborators by selecting **History** on the right side of your machine part's card on the **CONFIGURE** tab.
You can also revert to an earlier configuration from the History tab.

#### Conditional reconfiguration

If you only want to apply configuration updates under certain conditions, you can create a sensor with your conditions.
The sensor must return a true value when it is safe to update and a false value otherwise.

Add the following configuration to your machine's JSON configuration:

```json
// components: [ ... ],
// services: [ ... ],
maintenance : {
   "sensor_name" : string,
   "maintenance_allowed_key" : string
}
```

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `sensor_name` | string | **Required** | The full name of the sensor that provides the information if it is safe to update a machine's configuration. For example `rdk:component:sensor/sensor1`. |
| `maintenance_allowed_key` | string | **Required** | The key of the key value pair for the reading returned by the sensor. |

### Logging

Log messages written appear under the [**LOGS** tab](/cloud/machines/#logs) for the machine running the module.

### Shutdown

During machine shutdown, `viam-server` handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

## Next steps

{{< cards >}}
{{% card link="/appendix/apis/" %}}
{{% card link="/registry/" customTitle="Viam Registry" %}}
{{% card link="/installation/viam-server-setup/" canonical="/installation/viam-micro-server-setup/#install-viam-micro-server" %}}
{{< /cards >}}
