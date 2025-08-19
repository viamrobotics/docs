---
linkTitle: "Schedule automated jobs"
title: "Schedule automated jobs on machines"
weight: 40
layout: "docs"
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
description: "Configure automated jobs that run on machines at specified intervals."
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Intermediate"
date: "2025-06-17"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

Viam's machine job scheduler allows you to configure automated jobs that run on your machines at specified intervals. This enables you to automate routine tasks such as data collection, sensor readings, maintenance operations, and system checks.

The job scheduler is built into `viam-server` and executes configured jobs according to their specified schedules. Each job targets a specific resource on your machine and calls a designated method at the scheduled intervals.

## Configure a job

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [ ... ],
  "services": [ ... ],
  "jobs": [
    {
      "name": "hourly-job",
      "schedule": "0 * * * *",
      "resource": "<resource-name>",
      "method": "<method-name>"
    },
    {
      "name": "daily-job",
      "schedule": "0 8 * * *",
      "resource": "<resource-name>",
      "method": "<method-name>"
    },
    {
      "name": "periodic-job",
      "schedule": "15m",
      "resource": "<resource-name>",
      "method": "<method-name>"
    },
    {
      "name": "do-command-job",
      "schedule": "0 2 * * 0",
      "resource": "<resource-name>",
      "method": "DoCommand",
      "command": {
        "key": "calibrate",
        "mode": "full"
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "temp-sensor",
      "model": "fake",
      "type": "sensor"
    },
    {
      "name": "camera1",
      "model": "webcam",
      "type": "camera"
    }
  ],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager"
    }
  ],
  "jobs": [
    {
      "name": "hourly-sensor-reading",
      "schedule": "0 * * * *",
      "resource": "temp-sensor",
      "method": "GetReadings"
    },
    {
      "name": "daily-camera-capture",
      "schedule": "0 8 * * *",
      "resource": "camera1",
      "method": "GetImage"
    },
    {
      "name": "periodic-sync",
      "schedule": "15m",
      "resource": "data_manager",
      "method": "Sync"
    },
    {
      "name": "custom-maintenance",
      "schedule": "0 2 * * 0",
      "resource": "temp-sensor",
      "method": "DoCommand",
      "command": {
        "action": "calibrate",
        "mode": "full"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Job configuration

Jobs are configured as part of your machine's configuration. Each job requires the following parameters:

<!-- prettier-ignore -->
| Parameter  | Type   | Required     | Description                                                      |
| ---------- | ------ | ------------ | ---------------------------------------------------------------- |
| `name`     | string | **Required** | Unique identifier for the job within the machine.                |
| `schedule` | string | **Required** | Schedule specification using unix-cron format or Golang duration. Accepts <ul><li>Unix-cron expressions for time-based scheduling:<ul><li>`"0 */6 * * *"` - Every 6 hours</li><li>`"0 0 * * 0"` - Every Sunday at midnight</li><li>`"*/15 * * * *"` - Every 15 minutes</li><li>`"0 9 * * 1-5"` - Every weekday at 9 AM</li></ul></li><li>Golang duration strings for interval-based scheduling:<ul><li>`"5m"` - Every 5 minutes</li><li>`"1h"` - Every hour</li><li>`"30s"` - Every 30 seconds</li><li>`"24h"` - Every 24 hours</li></ul></li></ul>Job schedules are evaluated in the machine's local timezone. |
| `resource` | string | **Required** | Name of the target resource (component or service).               |
| `method`   | string | **Required** | gRPC method to call on the target resource.                       |
| `command`  | object | Optional     | Command parameters for `DoCommand` operations.                    |

## Monitoring and troubleshooting

Monitor job execution through `viam-server` logs. Look for `rdk.job_manager`:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
8/19/2025, 7:38:59 PM info rdk.job_manager.periodic-job   jobmanager/jobmanager.go:160   Job succeeded   response map[action:true]
8/19/2025, 7:38:59 PM info rdk.job_manager.periodic-job   jobmanager/jobmanager.go:155   Job triggered
8/19/2025, 7:51:33 PM warn rdk.job_manager.periodic-job   jobmanager/jobmanager.go:151   Could not get resource   error could not find the resource for name generic-2
```

## Limitations

- There is no timeout on job's invocations of gRPC requests
- Jobs only run when `viam-server` is running
- If a unix-cron job _should_ run but cannot due to a previous invocation still running, the job will not run until the next scheduled cron occurrence when a previous invocation has finished
- If a Golang duration job _should_ run but cannot due to a previous invocation still running, the next invocation will not run until the previous invocation finishes, at which point it will run immediately
- Jobs run locally on each machine and are not coordinated across multiple machines.
- Job execution depends on `viam-server` running.
- Failed jobs do not retry.
