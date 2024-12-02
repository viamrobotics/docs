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

#### Maintenance window

There are a few updates that may make your machine temporarily unavailable:

- `viam-agent` updating `viam-server`
- configuration updates

To avoid performing these updates until your machine is ready for maintenance, you can define a maintenance window.
A maintenance window consists of one or multiple conditions that determine if maintenance is currently allowed.
To configure a maintenance window, you need to create a sensor that returns true when your maintenance conditions are met and false otherwise.

Then, add the following configuration to your machine's JSON configuration:

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

Log messages appear under the [**LOGS** tab](/cloud/machines/#logs) for a machine.

The default log level for `viam-server` and any running resources is `"Info"`.

You can set log levels for individual components or other resources by adding the `log_configuration` option to the resources' JSON configuration:

```json
"log_configuration": {
    "level": "Debug"
},
"attributes": { ... }
```

Alternatively, you can configure logs for all machine resources, inside your machine config.
To specify the log level for a specific resource, add the `log` field to your machine config:

For example:

```json
"log": [
     {
       "pattern": "rdk.resource_manager",
       "level": "info",
     },{
       "pattern": "rdk.resource_manager.*",
       "level": "debug",
     }
  ]
```

<!-- prettier-ignore -->
| Attribute | Description |
| --------- | ----------- |
| `pattern` | A regular expression (regex) pattern matching one or more resources. |
| `level` | The log level: `"debug"`, `"info"`, `"warn"`, or `"error"`. |

Patterns are processed from top to bottom.
If multiple patterns apply, the last pattern to be processed will apply.
If log configurations are applied at a resource level using the `log_configuration` field, these take precedence over log levels applied in the `log` field of the machine configuration.

#### Debugging

You can enable debug level logs in two ways:

- Start `viam-server` with the `-debug` option.
- Add `"debug": true` to the machine's configuration:

  ```json
  {
    "debug": true,
    "components": [{ ... }]
  }
  ```

Enabling debug level logs will take precedence over all logging configuration set using the `log` field on a machine or the `log_configuration` field on a resource.

### Shutdown

During machine shutdown, `viam-server` handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

## Next steps

{{< cards >}}
{{% card link="/appendix/apis/" %}}
{{% card link="/registry/" customTitle="Viam Registry" %}}
{{% card link="/installation/viam-server-setup/" canonical="/installation/viam-micro-server-setup/#install-viam-micro-server" %}}
{{< /cards >}}
