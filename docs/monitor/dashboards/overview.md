---
linkTitle: "Overview"
title: "Data dashboards"
weight: 10
layout: "docs"
type: "docs"
description: "Understand dashboard widget types, the windowing and aggregation query model, and how dashboards differ from teleop workspaces."
---

Dashboards and teleop workspaces both use widgets to display data from your machines. This page explains what each widget type does, how the query model behind them works, and where dashboards and teleop workspaces differ.

For step-by-step instructions, see [Create dashboards](/monitor/dashboards/create-dashboards/). For custom MQL queries, see [Custom queries](/monitor/dashboards/custom-queries/).

## Widget types

Widgets are the building blocks of dashboards and teleop workspaces. Each widget type displays data in a different way.

### GPS

Displays a machine's location on a map using position data from a movement sensor. You select a movement sensor and a refresh rate. The map updates at the interval you specify.

Use GPS widgets to track machine locations across a fleet, or to monitor a single machine's position over time.

### Stat

Displays a single value from a sensor, such as the current temperature or battery level.

In **dashboards**, stat widgets support the full query model: you can apply windowing and aggregation to show computed values like the average temperature across all machines over the last hour. In **teleop workspaces**, stat widgets show only the most recent reading from the selected sensor.

### Time series

Displays a graph of sensor data over time. You can add multiple lines to the same graph to compare readings from different sensors or fields.

Time series widgets support the full query model (windowing and aggregation) in both dashboards and teleop workspaces. You can graph raw data points or aggregate them into time windows to smooth out noise and reveal trends.

### Table

Displays sensor data in rows and columns. Each row represents a reading and each column represents a field.

In **dashboards**, tables support two display methods:

- **Columns**: configure each column independently with its own data source and aggregation. No MQL required.
- **Custom query**: write an MQL aggregation pipeline to transform data into any column structure you need.

In **teleop workspaces**, tables support custom queries only.

### Actuation

Displays controls for actuating components: motors, servos, bases, arms, grippers, and other components that accept commands.

Available in **teleop workspaces only**. Dashboards are read-only and do not include actuation widgets.

### Camera

Displays a live camera feed.

Available in **teleop workspaces only**. Dashboards do not include camera streams.

## The query model

Time series, stat, and table widgets do not just display raw sensor readings. They can transform data through two layers of processing: **windowing** and **aggregation**. Understanding these two layers is the key to building useful dashboards.

### Windowing: group readings into time buckets

Windowing divides your data into time buckets of a specified duration and computes a summary value for each bucket. For example, with a 1-hour window and the Average method, you get one averaged data point per hour instead of hundreds of raw readings.

Available window methods:

| Method       | What it computes                                      | Example use                                                       |
| ------------ | ----------------------------------------------------- | ----------------------------------------------------------------- |
| None         | No windowing. Returns raw data points sorted by time. | Viewing individual sensor readings.                               |
| Count        | Number of readings in each time bucket.               | Checking whether a sensor is reporting at the expected frequency. |
| Average      | Mean value in each bucket.                            | Smoothing noisy temperature data into hourly averages.            |
| Min          | Lowest value in each bucket.                          | Finding the coldest temperature each hour.                        |
| Max          | Highest value in each bucket.                         | Tracking peak CPU usage per hour.                                 |
| Sum          | Total of all values in each bucket.                   | Counting total events per time window.                            |
| Custom query | An MQL aggregation pipeline you define.               | Computing derived metrics like rate of change or percentiles.     |

### Aggregation: combine across machines

After windowing groups data into time buckets, aggregation combines data from multiple machines into a single result. This is how you answer questions like "what is the average temperature across all machines in the warehouse?"

Available aggregation methods: Average, Count, Min, Max, Sum, and Custom query. These work the same way as the corresponding window methods but operate across machines instead of across time.

Aggregation is optional. If you skip it, each machine's data appears as a separate line or value.

### How the two layers work together

Consider a fleet of 10 machines, each reporting temperature every 10 seconds:

1. **Raw data**: 6 readings per minute per machine, so 60 readings per minute across the fleet.
2. **After windowing** (Average, 1-hour window): 1 data point per hour per machine, so 10 data points per hour.
3. **After aggregation** (Average): 1 data point per hour for the entire fleet.

The same two-layer model applies to stat widgets (showing a single computed value) and table widgets using the columns display method.

### When you need custom queries

The built-in window and aggregation methods cover common cases. Use a custom query when you need to:

- Compute derived values like rate of change, standard deviation, or percentiles
- Filter or reshape data beyond what the built-in methods support
- Join data from multiple fields into a single visualization
- Apply conditional logic to your aggregation

Custom queries use MongoDB's MQL aggregation pipeline syntax. For details on writing custom queries, see [Custom queries](/monitor/dashboards/custom-queries/).

## Dashboards and teleop workspaces

Dashboards and teleop workspaces serve different purposes and have different capabilities.

|                 | Dashboard                                                                       | Teleop workspace                                         |
| --------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Purpose         | Monitor data trends across machines                                             | Control and monitor a specific machine                   |
| Scope           | Organization-level, with filters for location, machine, fragment, and timeframe | Requires selecting a specific machine                    |
| Widget types    | GPS, stat, time series, table                                                   | GPS, stat, time series, table, plus actuation and camera |
| Control         | Read-only                                                                       | Can send commands to components                          |
| Stat widget     | Supports windowing and aggregation                                              | Most recent reading only                                 |
| Table widget    | Columns or custom query                                                         | Custom query only                                        |
| Time series Sum | Supported                                                                       | Not available                                            |

Use **dashboards** when you want to watch data from multiple machines or analyze trends over time. Use **teleop workspaces** when you need to interact with a specific machine or view its live camera feeds.

To create a dashboard, see [Create dashboards](/monitor/dashboards/create-dashboards/). To create a teleop workspace, see [Teleop workspaces](/monitor/teleop-workspaces/).
