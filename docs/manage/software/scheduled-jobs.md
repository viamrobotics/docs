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

Viam's machine job scheduler allows you to configure automated jobs that run on your machines at specified intervals.
This enables you to automate routine tasks such as data collection, sensor readings, maintenance operations, and system checks.

The job scheduler is built into `viam-server` and executes configured jobs according to their specified schedules.
Each job targets a specific resource on your machine and calls a designated component or service API method at the scheduled intervals.

## Configure a job

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Job**.

1. Enter a name and click **Create**.

1. For the **Schedule**, select **Interval** or **Cron** and specify the interval the job should be run in.

1. For **Job**, select a **Resource**, and a component or service API **method**.
   For the `DoCommand` method also specify the command parameters.

{{% /tab %}}
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
| Parameter  | Type   | Required     | Description |
| ---------- | ------ | ------------ | ----------- |
| `name`     | string | **Required** | Unique identifier for the job within the machine.                |
| `schedule` | string | **Required** | Schedule specification using unix-cron format or Golang duration. Accepts <ul><li>Unix-cron expressions for time-based scheduling:<ul><li>`"*/5 * * * * *"`: Runs at 5 seconds past the minute</li><li>`"0 */6 * * *"`: Every 6 hours</li><li>`"0 0 * * 0"`: Every Sunday at midnight</li><li>`"*/15 * * * *"`: Every 15 minutes</li><li>`"0 9 * * 1-5"`: Every weekday at 9 AM</li></ul></li><li>Golang duration strings for interval-based scheduling:<ul><li>`"10ms"`: Every 30 milliseconds</li><li>`"30s"`: Every 30 seconds</li><li>`"5m"`: Every 5 minutes</li><li>`"1h"`: Every hour</li><li>`"24h"`: Every 24 hours</li></ul></li></ul>Job schedules are evaluated in the machine's local timezone. |
| `resource` | string | **Required** | Name of the target resource (component or service).               |
| `method`   | string | **Required** | Component or service API method to call on the target resource.   |
| `command`  | object | Optional     | Command parameters for `DoCommand` operations.                    |

## Monitoring and troubleshooting

Monitor job execution through `viam-server` logs. Look for `rdk.job_manager`:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
8/19/2025, 7:38:59 PM info rdk.job_manager.periodic-job   jobmanager/jobmanager.go:160   Job succeeded   response map[action:true]
8/19/2025, 7:38:59 PM info rdk.job_manager.periodic-job   jobmanager/jobmanager.go:155   Job triggered
8/19/2025, 7:51:33 PM warn rdk.job_manager.periodic-job   jobmanager/jobmanager.go:151   Could not get resource   error could not find the resource for name generic-2
```

## Limitations

- There is no timeout on job's invocations of gRPC requests.
- Jobs only run when `viam-server` is running.
- If a unix-cron job is scheduled to start but a previous invocation is still running, the job will be skipped. The job will next run once the previous invocation has finished running and the next scheduled time is reached.
- If a Golang duration job is scheduled to run but a previous invocation is still running, the next invocation will not run until the previous invocation finishes, at which point it will run immediately.
- `DoCommand` is currently the only supported component and service API method which you can invoke with arguments.
  Aside from `DoCommand`, Jobs currently only support component and service API methods that do not require arguments.
  To avoid this limitation, create a module and encapsulate API calls in a DoCommand API call.
- Jobs run locally on each machine and are not coordinated across multiple machines.
- Job execution depends on `viam-server` running.
- Failed jobs do not retry.
