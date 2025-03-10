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
  - /architecture/viam-server/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The `viam-server` executable runs on a computer and manages hardware, software, and data for a machine.
`viam-server` is built from the open-source [Robot Development Kit (RDK)](https://github.com/viamrobotics/rdk).
If you are working with microcontrollers, [`viam-micro-server`](/operate/reference/viam-micro-server/) is a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured `viam-server`.

To use Viam with a machine, you create a configuration specifying which hardware and software the machine consists of.
`viam-server` then manages and runs the drivers for the configured {{< glossary_tooltip term_id="resource" text="resources" >}}.

Overall, `viam-server` manages:

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

Reconfiguration of individual resources happens concurrently if there are no configured dependencies for any resources.
If there are configured dependencies, resources are reconfigured in groups.

You can see configuration changes made by yourself or by your collaborators by selecting **History** on the right side of your machine part's card on the **CONFIGURE** tab.
You can also revert to an earlier configuration from the History tab.

#### Maintenance window

There are a few updates that may make your machine temporarily unavailable:

- `viam-agent` updating `viam-server`
- configuration updates

To avoid performing these updates until your machine is ready for maintenance, you can define a maintenance window.
A maintenance window consists of one or multiple conditions that determine if maintenance is currently allowed.
To configure a maintenance window, you need to create a sensor that returns true when your maintenance conditions are met and false otherwise.

{{< tabs >}}
{{% tab name="Builder UI" %}}

To configure a maintenance window, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Maintenance window**.

In the new panel, specify the name of the sensor and the key for the value to be used to determine when maintenance is allowed.

{{% /tab %}}
{{% tab name="JSON" %}}

To configure a maintenance window, add the following configuration to your machine's JSON configuration:

```json
// components: [ ... ],
// services: [ ... ],
maintenance : {
   "sensor_name" : string,
   "maintenance_allowed_key" : string
}
```

{{% /tab %}}
{{< /tabs >}}

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `sensor_name` | string | **Required** | The full name of the sensor that provides the information if it is safe to update a machine's configuration. For example `rdk:component:sensor/sensor1`. |
| `maintenance_allowed_key` | string | **Required** | The key of the key value pair for the reading returned by the sensor. |

### Logging

Log messages appear under the [**LOGS** tab](/manage/troubleshoot/troubleshoot/#check-logs) for a machine.

The default log level for `viam-server` and any running resources is `"Info"`.
Logs are stored for 30 days before they are deleted.

If you need more logs for individual resource, click **Enable debug logs** in the **...** menu on the resource.
To set other log levels for individual resources, add the `log_configuration` option to the resource's JSON configuration:

```json
"log_configuration": {
    "level": "Debug"
},
"attributes": { ... }
```

For modular resources, you must instead set the `log_level` attribute on the module itself:

```json {class="line-numbers linkable-line-numbers" data-line="3"}
"module_id": "viam:raspberry-pi",
"version": "1.9.0"
"log_level":  "debug"
```

Alternatively, you can configure logs for all machine resources, inside your machine config.
To specify the log level for a specific resource, add the `log` field to your machine config:

For example:

```json
"components": [ ... ]
"log": [
    {
    "pattern": "rdk.components.arm",
    "level": "debug",
    }, {
    "pattern": "rdk.services.*",
    "level": "debug",
    }, {
    "pattern": "<module-name>",
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

{{% expand "Click to view full configuration example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="10-18"}
{
  "components": [
    {
      "name": "camera1",
      "api": "rdk:component:camera",
      "model": "fake"
    }
  ],
  "services": [],
  "log": [
    {
      "pattern": "rdk.resource_manager",
      "level": "info"
    },
    {
      "pattern": "rdk.resource_manager.*",
      "level": "debug"
    }
  ]
}
```

{{% /expand%}}

#### Disable log deduplication

By default, `viam-server` deduplicates log messages that are deemed noisy.
A log is deemed noisy if it has been output 3 times in the past 10 seconds.

To disable log deduplication, set `disable_log_deduplication` in your machine's configuration:

```json
"disable_log_deduplication": true
```

{{% expand "Click to view full configuration example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="10"}
{
  "components": [
    {
      "name": "camera1",
      "api": "rdk:component:camera",
      "model": "fake"
    }
  ],
  "services": [],
  "disable_log_deduplication": true
}
```

{{% /expand%}}

#### Delete machine logs

You cannot delete machine logs.
If your machine has generated a large amount of logs and you are concerned about the cost, you can:

1. Copy the machine's configuration to a new machine.
2. Delete the old machine.

If you delete a machine you will not be charged for the remainder of the 30 days until logs from that machine are deleted.

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
{{% card link="/dev/reference/apis/" %}}
{{% card link="/operate/get-started/supported-hardware/" %}}
{{% card link="/operate/get-started/setup/" %}}
{{< /cards >}}
