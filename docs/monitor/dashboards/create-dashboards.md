---
linkTitle: "Create dashboards"
title: "Create dashboards"
weight: 20
layout: "docs"
type: "docs"
description: "Create a dashboard to visualize sensor data from machines across your organization."
---

Create a dashboard to visualize sensor data from machines across your organization. Dashboards display data through widgets that you configure to pull from specific sensors.

Before you start, you need at least one machine with a sensor configured for [data capture](/data/capture-sync/capture-and-sync-data/) so there is data to visualize.

## Create a dashboard

1. Navigate to the [**FLEET** page](https://app.viam.com) and click the **dashboard** tab.
1. Click **Create dashboard**.
1. Enter a name for your dashboard, replacing the placeholder text.

Only organization owners can create dashboards.

## Add widgets

Click **Add widget** and select a widget type.
The widget appears in your dashboard layout.
Click the pencil icon in the top right of the widget to configure it.

To rearrange widgets, click and drag the grid icon in the top left of a widget.
Drag the divider between widgets to resize them.

For an explanation of each widget type and the query model behind them, see [Data dashboards overview](/monitor/dashboards/overview/).

### GPS

Displays the current location reported by a movement sensor on a map.

1. Choose a movement sensor from the **Movement sensor name** dropdown.
1. Set the **Refresh rate** in seconds.
1. Click **Save**.

### Stat

Displays a computed value from a sensor. By default, this is the most recent reading, but you can apply windowing and aggregation to show values like the average temperature across your fleet over the last hour.

1. Choose a sensor from the **Sensor name** dropdown.
1. Select the reading to display from the **Path** dropdown.
1. Set a title, unit suffix, and refresh rate.
1. To aggregate data, configure a **Window method** and **Aggregation method**. See [The query model](/monitor/dashboards/overview/#the-query-model) for details on these options.
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
   - **Min**: lowest value in each window
   - **Max**: highest value in each window
   - **Sum**: total of all values in each window
   - **Custom query**: a custom MQL aggregation pipeline (see [Custom queries](/monitor/dashboards/custom-queries/))
1. Optionally select an **Aggregation method** to combine data across machines. The same methods are available: Average, Count, Min, Max, Sum, and Custom query. See [The query model](/monitor/dashboards/overview/#the-query-model) for details.
1. Click **Save**.

### Table

Displays a grid of sensor readings.
Each row is a reading and each column is a field.

Tables support two display methods:

**Columns** (no MQL required):

1. Choose a sensor from the **Resource name** dropdown.
1. Choose a capture method.
1. Configure each column with its own data source and aggregation method.
1. Click **Save**.

**Custom query** (MQL):

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

   Tables display a maximum of 10,000 rows.

   For more on MQL aggregation, see the [MongoDB documentation](https://www.mongodb.com/docs/manual/reference/mql/aggregation-stages/).

1. Click **Save**.

## Filter dashboard data

Use the filter bar at the top of a dashboard to scope which data the widgets display:

- **Location**: show data from machines in a specific location.
- **Machine**: show data from a specific machine.
- **Fragment**: show data from machines that use a specific fragment.
- **Timeframe**: set the time range for historical data. The default is the last hour. You can use relative times like `now-1h` or `now-30m`, or set absolute start and end times.

Filters apply to all widgets in the dashboard.

## Manage dashboards

- **Rename**: click the dashboard name at the top of the page and edit it inline.
- **Duplicate**: create a copy of the dashboard from the actions menu.
- **Delete**: remove the dashboard from the actions menu. This cannot be undone.
