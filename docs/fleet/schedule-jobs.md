---
linkTitle: "Schedule jobs"
title: "Schedule automated jobs"
weight: 40
layout: "docs"
type: "docs"
description: "Configure automated jobs that call component and service methods on a schedule."
---

Schedule automated jobs that call methods on your machine's components and services at specified intervals. Use jobs to automate routine tasks like reading sensors, capturing images, running calibration routines, or syncing data.

## When to use jobs

Jobs are a good fit when you need to:

- Call a component or service method at regular intervals (every 30 seconds, hourly, daily)
- Run a `DoCommand` routine with specific parameters on a schedule
- Automate operations that don't require complex logic between calls

If you need conditional logic, coordination between multiple resources, or responses to events, write a [logic module](/build-modules/write-a-logic-module/) instead.

## Add a job

1. Navigate to your machine's **CONFIGURE** tab (or edit a fragment that the machine uses).
1. Click **+** and select **Job**.
1. Enter a name for the job and click **Create**.

## Configure the schedule

The job card has a **Schedule** section with three options:

**Interval**: run the job every N units of time. Select a number and a unit (milliseconds, seconds, minutes, hours, or days). For example, "every 5 minutes."

**Cron**: run the job on a cron schedule. Enter a 5-field or 6-field cron expression. The UI shows a human-readable description of the schedule. Examples:

- `0 * * * *` — every hour at the top of the hour
- `0 9 * * 1-5` — every weekday at 9 AM
- `*/5 * * * * *` — every 5 seconds (6-field cron with seconds)

Cron schedules are evaluated in UTC.

**Continuous**: run the job in an infinite loop. Each invocation starts immediately after the previous one completes. Use this for tasks that should always be running.

## Configure the action

In the **Job** section:

1. Select a **Resource** from the dropdown. This lists all components and services on the machine.
1. Enter the **Method** to call on that resource. For custom actions, use `DoCommand`.
1. If the method is `DoCommand`, a **Command** editor appears. Enter the JSON command to send:

```json
{
  "action": "calibrate",
  "mode": "full"
}
```

## Configure logging

In the **Log threshold** section, set the minimum log level for this job's output:

- **Error**: only errors
- **Warn**: errors and warnings
- **Info**: errors, warnings, and info (default)
- **Debug**: all messages, including debug output from job execution

Job execution logs appear under `rdk.job_manager.{job-name}` in the machine's logs. At the default Info level, "Job triggered" and "Job succeeded" messages are at debug level and will not appear. Set the log threshold to Debug to see them.

## JSON configuration reference

In JSON mode, jobs are defined in the `jobs` array at the top level of the machine configuration:

```json
{
  "jobs": [
    {
      "name": "hourly-reading",
      "schedule": "0 * * * *",
      "resource": "my-sensor",
      "method": "GetReadings"
    },
    {
      "name": "calibration",
      "schedule": "0 2 * * 0",
      "resource": "my-sensor",
      "method": "DoCommand",
      "command": {
        "action": "calibrate"
      },
      "log_configuration": {
        "level": "debug"
      }
    }
  ]
}
```

| Field               | Type   | Required | Description                                                                                                    |
| ------------------- | ------ | -------- | -------------------------------------------------------------------------------------------------------------- |
| `name`              | string | Yes      | Unique name for the job.                                                                                       |
| `schedule`          | string | Yes      | Cron expression (5 or 6 fields), Go duration string (for example, `"30s"`, `"5m"`, `"1h"`), or `"continuous"`. |
| `resource`          | string | Yes      | Name of the component or service to call.                                                                      |
| `method`            | string | Yes      | The API method to invoke on the resource.                                                                      |
| `command`           | object | No       | Arguments for `DoCommand`. Ignored for other methods.                                                          |
| `log_configuration` | object | No       | Set `"level"` to `"debug"`, `"info"`, `"warn"`, or `"error"`.                                                  |

## Verify a job is running

Check the machine's **LOGS** tab and filter for `job_manager`. Successful execution produces:

```sh {class="command-line" data-prompt="$" data-output="1-2"}
debug rdk.job_manager.hourly-reading  Job triggered
debug rdk.job_manager.hourly-reading  Job succeeded  response map[...]
```

If the resource is not found:

```sh {class="command-line" data-prompt="$" data-output="1"}
warn rdk.job_manager.hourly-reading  Could not get resource  error could not find the resource for name my-sensor
```

## Scheduling behavior

**Interval and cron jobs** are singleton: only one instance runs at a time.

- **Cron**: if a job is still running when the next cron trigger fires, the next run is skipped entirely. It runs again at the following scheduled time.
- **Interval**: if a job is still running when the next interval elapses, the next run queues and starts immediately after the current run finishes.

**Continuous jobs** restart immediately after each invocation. If the job function exits unexpectedly, it restarts after a 5-second delay.

## Limitations

- Jobs only run when `viam-server` is running. They do not persist across restarts (missed runs are not retried).
- `DoCommand` is the only method that supports arguments. All other methods are called without arguments (only the resource name is passed).
- There is no timeout on individual job invocations. A stuck job blocks that job's schedule indefinitely.
- Jobs run locally on each machine. There is no cross-machine job coordination.
- Failed jobs do not retry automatically. The failure is logged and the job runs again at the next scheduled time.
- Duplicate job names in the same configuration produce undefined behavior.

## Related pages

- [Reuse configuration](/fleet/reuse-configuration/) for deploying job configurations across a fleet through fragments
- [Write a logic module](/build-modules/write-a-logic-module/) for more complex automation that goes beyond scheduled method calls
