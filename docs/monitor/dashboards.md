---
linkTitle: "Data dashboards"
title: "Data dashboards"
weight: 15
layout: "docs"
type: "docs"
description: "Create dashboards to visualize sensor data and monitor trends across machines in your organization."
---

Dashboards let you visualize sensor data from machines across your organization.
You build a dashboard by adding widgets (GPS maps, stat displays, time series graphs, and data tables) and configuring each widget to pull data from a specific sensor and capture method.

Dashboards are for monitoring and analysis.
If you need to control a machine remotely (send commands to motors, view live camera feeds, actuate grippers), use a [teleop workspace](/monitor/custom-interface/) instead.

## Create a dashboard

1. Navigate to the [**FLEET** page](https://app.viam.com) and click the **dashboard** tab.
1. Click **Create dashboard**.
1. Enter a name for your dashboard, replacing the placeholder text.

## Add widgets

Click **Add widget** and select a widget type.
The widget appears in your dashboard layout.
Click the pencil icon in the top right of the widget to configure it.

To rearrange widgets, click and drag the grid icon in the top left of a widget.
Drag the divider between widgets to resize them.

### GPS

Displays the current location reported by a movement sensor on a map.

To configure:

1. Choose a movement sensor from the **Movement sensor name** dropdown.
1. Set the **Refresh rate** in seconds.
1. Click **Save**.

### Stat

Displays the most recent reading from a sensor as a single value.

To configure:

1. Choose a sensor from the **Sensor name** dropdown.
1. Select the reading to display from the **Path** dropdown.
1. Set a title, unit suffix, and refresh rate.
1. Click **Save**.

### Time series

Displays a graph of sensor readings over time.
You can add multiple lines to compare readings from different sensors or fields on the same graph.

To configure each line:

1. Choose a sensor from the **Resource name** dropdown.
1. Choose a capture method (for example, **Readings**).
1. Enter a title for the line.
1. Select the data field from the **Path** dropdown.
1. Set the unit, duration, and other display options.
1. Select a **Window method** to aggregate readings over time intervals:
   - **None**: raw data points
   - **Count**: number of readings in each window
   - **Average**: mean value in each window
   - **Minimum**: lowest value in each window
   - **Maximum**: highest value in each window
   - **Custom query**: a custom MQL aggregation pipeline
1. Click **Save**.

### Table

Displays a grid of sensor readings.
Each row is a reading; each column is a field.

To configure:

1. Choose a sensor from the **Resource name** dropdown.
1. Choose a capture method.
1. Set the refetch rate and time range in seconds.
1. Write a custom MQL aggregation pipeline to transform your data into columns.

   For example, given sensor data with nested readings:

   ```json
   {
     "data": {
       "readings": {
         "temperature": 22.96,
         "humidity": 48.318
       }
     }
   }
   ```

   Use a `$project` stage to select and rename columns:

   ```json
   {
     "$project": {
       "Temperature": "$data.readings.temperature",
       "Humidity": "$data.readings.humidity"
     }
   }
   ```

   For more on MQL aggregation, see the [MongoDB documentation](https://www.mongodb.com/docs/manual/reference/mql/aggregation-stages/).

1. Click **Save**.

## Filter dashboard data

Use the filter bar at the top of a dashboard to scope which data the widgets display:

- **Location**: show data from machines in a specific location.
- **Machine**: show data from a specific machine.
- **Fragment**: show data from machines using a specific fragment.
- **Timeframe**: set the time range for historical data.

Filters apply to all widgets in the dashboard.

## Manage dashboards

- **Rename**: click the dashboard name at the top of the page and edit it inline.
- **Duplicate**: create a copy of the dashboard from the actions menu.
- **Delete**: remove the dashboard from the actions menu. This cannot be undone.

## Dashboards and teleop workspaces

Dashboards and [teleop workspaces](/monitor/custom-interface/) are separate features that appear as separate tabs under **FLEET**.

|              | Dashboard                           | Teleop workspace                                         |
| ------------ | ----------------------------------- | -------------------------------------------------------- |
| Purpose      | Monitor data trends across machines | Control and monitor a specific machine in real time      |
| Widget types | GPS, stat, time series, table       | GPS, stat, time series, table, plus actuation and camera |
| Scope        | Organization-level with filters     | Requires selecting a specific machine                    |
| Control      | Read-only                           | Can send commands to components                          |

Use dashboards when you want to watch data from multiple machines or analyze trends over time.
Use teleop workspaces when you need to interact with a specific machine.
