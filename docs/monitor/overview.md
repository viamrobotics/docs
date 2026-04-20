---
linkTitle: "Overview"
title: "Monitor and operate"
weight: 1
layout: "docs"
type: "docs"
description: "Monitor machine status, visualize data, set up alerts, teleoperate machines, and troubleshoot problems."
---

Your machines are running. Now you need to know what they're doing, get alerted when something needs attention, operate them remotely, and fix problems when they arise. This section covers the observability and operations tools that Viam provides for deployed machines.

## Check machine status

The fleet dashboard shows every machine in your organization with its current status: online, offline, or awaiting setup. You can see when each machine was last online, drill into individual machines to inspect part status and configuration, and check resource health.

From the command line, `viam machines status` and `viam machines part status` provide the same information.

See [Monitor machine status](/monitor/monitor/).

## Visualize data with dashboards

Dashboards let you visualize sensor data from machines across your organization. You add widgets (GPS maps, stat displays, time series graphs, and tables) and configure each one to pull data from a specific sensor and capture method. Filters scope the data by location, machine, fragment, or time range.

Widgets support aggregation: you can compute averages, minimums, maximums, and counts over time windows, or write custom MongoDB aggregation queries for advanced transformations. A separate overview explains the query model and widget types in detail.

See [Data dashboards](/monitor/dashboards/overview/).

## Set up alerts

Triggers send email or webhook notifications when specific events occur on your machines:

- **Telemetry thresholds**: alert when a sensor reading (CPU usage, temperature, battery level) crosses a threshold.
- **Machine status**: alert when a machine part comes online or goes offline.
- **Log levels**: alert when error, warning, or info logs appear on a machine.

You configure the alert frequency to control how often alerts fire, which helps prevent alert fatigue as your fleet grows. Notifications can go to specific email addresses, all machine owners, or a webhook endpoint that integrates with services like PagerDuty, Twilio, or Zapier.

For alerts based on data sync events, see [Trigger on data events](/data/trigger-on-data/). For alerts based on ML model detections, see [Alert on detections](/vision/object-detection/alert-on-detections/).

See [Set up alerts](/monitor/alert/).

## Teleoperate machines

You can remotely control and test any configured machine without writing code.

The **default control interface** is the CONTROL tab on your machine's page in the Viam app. It provides a control card for every configured component and service: move bases, actuate arms and grippers, read sensors, view camera feeds, and test vision services. The Viam mobile app provides similar access from your phone.

**Teleop workspaces** let you build custom operator interfaces with only the widgets you need for a specific task. You choose the widgets (camera feeds, sensor readouts, actuation controls, GPS maps) and arrange them into a focused view. This is useful when the full CONTROL tab shows more than the operator needs.

See [Default control interface](/monitor/default-interface/) and [Teleop workspaces](/monitor/teleop-workspaces/).

## Troubleshoot problems

When something goes wrong, Viam provides a set of debugging tools you can use without physical access to the machine:

- **Logs**: the LOGS tab shows machine logs filterable by level, keyword, time range, and resource. You can enable debug logging for individual resources or log name patterns without restarting.
- **Remote shell**: access a terminal on the machine through the CLI (`viam machines part shell`) without setting up SSH tunnels.
- **Debug endpoints**: enable pprof profiling and resource graph visualization for performance issues.
- **Configuration history**: view and revert to previous configurations if a config change caused the problem.
- **Diagnostics**: download FTDC (full-time diagnostic capture) data and OpenTelemetry traces for detailed analysis.

See [Troubleshoot problems](/monitor/troubleshoot/).

## What this section covers and what it does not

This section covers tools for monitoring, operating, and debugging machines that are already configured and running.

| If you need to...                              | See                                     |
| ---------------------------------------------- | --------------------------------------- |
| Set up a machine for the first time            | [Get started](/set-up-a-machine/)       |
| Configure components and services              | [Configure hardware](/hardware/)        |
| Capture and sync data from sensors             | [Manage data](/data/)                   |
| Train and deploy ML models                     | [Train ML models](/train/)              |
| Build a custom web or mobile app with the SDKs | [Build apps](/build-apps/overview/) |
| Manage fleet deployment and provisioning       | [Fleet deployment](/fleet/)             |
