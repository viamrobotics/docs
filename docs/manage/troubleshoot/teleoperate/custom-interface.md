---
title: "Teleoperate with a custom control interface"
linkTitle: "Custom interface"
weight: 25
type: "docs"
description: "Use a teleop workspace to create a custom control interface for operating a machine or visualizing and aggregating its data."
tags: ["teleop", "fleet management", "control", "app"]
languages: []
viamresources: ["sensor", "camera", "movement sensor"]
platformarea: ["viz", "data"]
images: ["/how-tos/teleop/full-workspace.png"]
level: "Intermediate"
date: "2024-11-13"
updated: "2025-09-10"
cost: "0"
---

You can remotely operate any configured machine and visualize and aggregate its data using a custom control interface.

## Prerequisites

{{% expand "A configured machine with teleoperable components" %}}

Make sure your machine has at least one camera, movement sensor, sensor, base, arm, board, gantry, gripper, motor or servo.

See [configure a machine](/operate/modules/configure-modules/) for more information.

{{% /expand%}}

### Create a workspace

1. Navigate to the **FLEET** page's [**TELEOP** tab](https://app.viam.com/teleop).
   Click **+ Create workspace**.

1. Enter a unique name for your workspace in the top left of the page, replacing the placeholder `untitled-workplace` text.

1. Use the **Select location** dropdown to select the location that contains the machine that you would like to visualize data from.

1. Use the **Select machine** dropdown to select the machine that you would like to visualize data from.

## Add a widget

1. Click **Add widget** and select a widget type to create a new widget on your workspace.

   See [widget types](/manage/troubleshoot/teleoperate/custom-interface/#widget-types) for more information about each type.

1. To configure the widget, click the pencil icon in the top right of your widget:

   {{<imgproc src="/services/data/visualize-widget-configure.png" alt="Click the pencil icon to configure your widget." style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

You can mix and match multiple widgets to visualize many kinds of data collected by your machine:

{{<imgproc src="/services/data/visualize-workspace.png" resize="1200x" style="width: 700px" class="fill imgzoom shadow" declaredimensions=true alt="Workspace containing.">}}

To arrange widgets on your workspace, click and drag the grid icon in the top left of your widget:

{{<imgproc src="/services/data/visualize-widget-move.png" alt="Click the grid icon to move a widget." style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

## Widget types

Viam provides the following types of widgets that you can customize to visualize data synced from your machines:

### Actuation

The actuation widget allows you to operate actuating components:

{{<imgproc src="/services/data/visualize-widget-actuation.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="An actuation widget displaying servo controls.">}}

To configure the actuation widget:

1. Choose a type from the **Component type** dropdown.
1. Choose a method from the **Method** dropdown.
1. Choose a component from the **Actuating component name** dropdown.
1. Click **Save**.

### Camera stream

The camera stream widget displays a live feed of the most recent image captured by a camera component:

{{<imgproc src="/services/data/visualize-widget-camera.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A camera widget displaying a live camera feed.">}}

To configure the camera widget:

1. Choose a camera from the **Camera name** dropdown.
1. Select the **Refresh type**.
1. Click **Save**.

### GPS

The GPS widget displays the current GPS location of any sensor that reports a position:

{{<imgproc src="/services/data/visualize-widget-gps.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A GPS widget displaying a live location.">}}

To configure the camera widget:

1. Choose a movement sensor from the **Movement sensor name** dropdown.
1. Specify the **Refresh rate** in seconds.
1. Choose to include Historic positions.
1. Click **Save**.

### Stat

The stat widget displays the most recent reading recorded by any sensor that produces tabular data:

{{<imgproc src="/services/data/visualize-widget-stat.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A stat widget displaying a live sensor reading.">}}

To configure the stat widget:

1. Choose a sensor from the **Sensor name** dropdown.
1. Select the reading you would like to display from the **Path** dropdown.
1. Assign a title, a unit suffix, and a refresh rate.
1. Click **Save**.

### Table

The table widget displays a grid of historic tabular data values. You can display multiple fields simultaneously in a single table.
Each row in the table represents a separate historic reading; each column represents a field.

{{<imgproc src="/services/data/visualize-widget-table.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A table widget displaying a grid of sensor readings.">}}

To configure the table widget, define the following attributes:

1. From the **Resource name** dropdown, choose a sensor you would like to visualize.
1. From the **Capture method** dropdown, choose a method of data capture (for example **Readings**).
1. Specify the **Refetch rate** in seconds.
1. Specify the **Time range** in seconds.

1. Use a custom MQL aggregation pipeline stage (or series of stages) to transform your sensor data into a flat object where each field corresponds to a column for the table.
   Consider the following sensor data, which contains information about air quality in a field named `readings`:

   ```json
   "data" {
     "readings": {
       "gas_resistance": 114978.66606781945,
       "temperature": 22.96,
       "pressure": 1016.18,
       "humidity": 48.318
     }
   }
   ```

   To change the displayed names, use a `$project` stage:

   ```mql
   {
     "$project": {
       "Air Quality": "$data.readings.gas_resistance",
       "Humidity": "$data.readings.humidity",
       "Temperature": "$data.readings.temperature"
     }
   }
   ```

   For more information about MQL aggregation operators, see the [MongoDB documentation](https://www.mongodb.com/docs/manual/reference/operator/aggregation/).

1. Click **Save**.

### Time series

The time series widget creates a graph of tabular data. You can add multiple lines to the time series widget to compare multiple readings over the same time period:

{{<imgproc src="/services/data/visualize-widget-time-series.png" resize="1000x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A time series widget displaying a live graph of sensor data over time.">}}

To configure the time series widget, define the following attributes for each line in the time series:

1. From the **Resource name** dropdown, choose a sensor you would like to visualize.
1. From the **Capture method** dropdown, choose a method of data capture (for example **Readings**).
1. In the **Title** field, enter a name for the line.
1. From the **Path** dropdown, choose the field of data that this line should visualize.

1. Use the other fields to customize the unit, duration, and other aspects of your visualization.

1. The **Window method** allows you to aggregate sensor readings over specified time intervals instead of displaying raw data points.
   Select a window method from the following options:

   - **None**: shows raw data with the path specified with no aggregation
   - **Count**: shows the number of readings within the window
   - **Average**: calculates the average value throughout the window
   - **Minimum**: shows the minimum value within the window
   - **Maximum**: shows the maximum value within the window
   - **Custom query**: shows the result of a custom MQL aggregation pipeline that you define

1. Click **Save**.
