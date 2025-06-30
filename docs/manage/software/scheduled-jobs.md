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

{{% alert title="Preview Feature" color="note" %}}
Machine job scheduling is a preview feature. The configuration and functionality described here may change as the feature is developed.
{{% /alert %}}

Viam's machine job scheduler allows you to configure automated jobs that run on your machines at specified intervals. This enables you to automate routine tasks such as data collection, sensor readings, maintenance operations, and system checks without manual intervention.

## How job scheduling works

The job scheduler is built into `viam-server` and executes configured jobs according to their specified schedules. Each job targets a specific resource on your machine and calls a designated method at the scheduled intervals.

Key features:

- **Flexible scheduling**: Support for both unix-cron expressions and Golang duration strings
- **Resource targeting**: Jobs can target any configured component or service on your machine
- **Method specification**: Call any gRPC method available on the target resource
- **Command parameters**: Pass custom parameters to `DoCommand` operations
- **Automatic execution**: Jobs run automatically according to their schedule without external triggers

## Job configuration

Jobs are configured as part of your machine's configuration. Each job requires the following parameters:

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `name` | string | **Required** | Unique identifier for the job within the machine |
| `schedule` | string | **Required** | Schedule specification using unix-cron format or Golang duration |
| `resource` | string | **Required** | Name of the target resource (component or service) |
| `method` | string | **Required** | gRPC method to call on the target resource |
| `command` | object | Optional | Command parameters for `DoCommand` operations |

### Schedule formats

The `schedule` parameter accepts two formats:

**Unix-cron expressions** for time-based scheduling:
- `"0 */6 * * *"` - Every 6 hours
- `"0 0 * * 0"` - Every Sunday at midnight
- `"*/15 * * * *"` - Every 15 minutes
- `"0 9 * * 1-5"` - Every weekday at 9 AM

**Golang duration strings** for interval-based scheduling:
- `"5m"` - Every 5 minutes
- `"1h"` - Every hour
- `"30s"` - Every 30 seconds
- `"24h"` - Every 24 hours

### Example configuration

Here's an example machine configuration with scheduled jobs:

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

## Common use cases

### Automated data collection

Schedule regular sensor readings or camera captures:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "environmental-monitoring",
  "schedule": "*/10 * * * *",
  "resource": "environment-sensor",
  "method": "GetReadings"
}
```

### Periodic maintenance

Run maintenance operations on a schedule:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "weekly-calibration",
  "schedule": "0 3 * * 0",
  "resource": "imu-sensor",
  "method": "DoCommand",
  "command": {
    "action": "calibrate"
  }
}
```

### Data synchronization

Ensure regular data uploads to the cloud:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "sync-data",
  "schedule": "30m",
  "resource": "data_manager",
  "method": "Sync"
}
```

### System health checks

Monitor system status at regular intervals:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "health-check",
  "schedule": "0 */4 * * *",
  "resource": "system-monitor",
  "method": "DoCommand",
  "command": {
    "action": "health_check",
    "include_logs": true
  }
}
```

## Best practices

### Naming conventions

Use descriptive names that indicate the job's purpose and frequency:
- `hourly-sensor-reading`
- `daily-backup`
- `weekly-maintenance`
- `periodic-sync`

### Schedule planning

Consider the following when planning job schedules:

- **Resource usage**: Avoid scheduling resource-intensive jobs simultaneously
- **Network bandwidth**: Stagger data upload jobs to prevent bandwidth saturation
- **Power consumption**: For battery-powered devices, balance functionality with power usage
- **Maintenance windows**: Schedule maintenance tasks during low-activity periods

### Error handling

Jobs should be designed to handle failures gracefully:
- Ensure target resources are properly configured and available
- Use appropriate timeouts for long-running operations
- Consider the impact of failed jobs on subsequent executions

### Testing schedules

Test your job schedules thoroughly:
- Use short intervals during development and testing
- Verify that jobs execute at expected times
- Monitor resource usage and system performance
- Check logs for execution status and errors

## Monitoring and troubleshooting

### Job execution logs

Monitor job execution through `viam-server` logs. Look for:
- Job start and completion messages
- Error messages for failed executions
- Resource availability issues
- Schedule parsing errors

### Common issues

**Job not executing**:
- Verify the schedule format is correct
- Check that the target resource exists and is configured
- Ensure the specified method is available on the resource

**Resource not found**:
- Confirm the resource name matches your configuration exactly
- Verify the resource is properly configured and operational

**Method not supported**:
- Check that the specified method is available on the target resource type
- Refer to the API documentation for supported methods

**Schedule parsing errors**:
- Validate cron expressions using online cron validators
- Ensure Golang duration strings follow the correct format

## Limitations

- Jobs run locally on each machine and are not coordinated across multiple machines
- Job execution depends on `viam-server` being running and connected
- Failed jobs do not automatically retry; design your jobs to be idempotent
- Job schedules are evaluated in the machine's local timezone

## Next steps

- Learn about [deploying control logic](/manage/software/control-logic/) for more complex automation
- Explore [data capture and sync](/data-ai/capture-data/) for automated data collection
- Review [component APIs](/dev/reference/apis/components/) to understand available methods for job targeting