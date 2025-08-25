---
linkTitle: "Visualize data"
title: "Visualize data"
weight: 20
layout: "docs"
type: "docs"
images: ["/services/icons/data-visualization.svg"]
icon: true
aliases:
  - /data/visualize/
  - /use-cases/sensor-data-visualize/
  - /how-tos/sensor-data-visualize/
  - /how-tos/configure-teleop-workspace/
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "fleet"]
date: "2024-12-04"
description: "Use teleop or Grafana to visualize sensor data."
---

Once you have used the data management service to [capture data](/data-ai/capture-data/capture-sync/), you can visualize your data on a dashboard on the [TELEOP](https://app.viam.com/teleop) page or a variety of third-party tools, including Grafana, Tableau, Google's Looker Studio, and more.

## Teleop

Create a dashboard visualizing numeric data from components with the **TELEOP** page.

### Prerequisites

{{% expand "A machine with at least one sensor, camera, or other component that captures data" %}}

Make sure your machine is configured with at least one component that can capture data, for example:

- [Sensor](/operate/reference/components/sensor/)
- [Movement sensor](/operate/reference/components/movement-sensor/)
- [Camera](/operate/reference/components/camera/)

{{% /expand%}}

### Create a workspace

1. Navigate to the **FLEET** page's [**TELEOP** tab](https://app.viam.com/teleop).
   Click **+ Create workspace**.
   Enter a unique name for your workspace in the top left of the page, replacing the placeholder `example-workplace` text.

1. Use the **Select location** dropdown to select the location that contains the machine that you would like to visualize data from.

1. Use the **Select machine** dropdown to select the machine that you would like to visualize data from.

### Add a widget

1. Click **Add widget** and select a widget type to create a new widget on your workspace.
   See [widget types](#widget-types) for more information about each type.

1. To configure the widget, click the pencil icon in the top right of your widget:

   {{<imgproc src="/services/data/visualize-widget-configure.png" alt="Click the pencil icon to configure your widget." style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

   {{% alert title="Tip" color="tip" %}}
   Select a location and machine for your workspace to populate the widget configuration dropdowns using sensor names and data from that machine.
   {{% /alert %}}

You can mix and match multiple widgets to visualize many kinds of data collected by your machine:

{{<imgproc src="/services/data/visualize-workspace.png" resize="1000x" style="width: 700px" class="fill imgzoom shadow" declaredimensions=true alt="Workspace containing.">}}

To arrange widgets on your workspace, click and drag the grid icon in the top left of your widget:

{{<imgproc src="/services/data/visualize-widget-move.png" alt="Click the grid icon to move a widget." style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

### Widget types

Viam provides the following types of widgets that you can customize to visualize data synced from your machines:

#### Camera stream

The camera stream widget displays a live feed of the most recent image captured by a camera component:

{{<imgproc src="/services/data/visualize-widget-camera.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A camera widget displaying a live camera feed.">}}

#### GPS

The GPS widget displays the current GPS location of any sensor that reports a position:

{{<imgproc src="/services/data/visualize-widget-gps.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A GPS widget displaying a live location.">}}

#### Stat

The stat widget displays the most recent reading recorded by any sensor that produces tabular data:

{{<imgproc src="/services/data/visualize-widget-stat.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A stat widget displaying a live sensor reading.">}}

To configure the stat widget:

1. Choose a sensor from the **Sensor name** dropdown.
1. Select the reading you would like to display from the **Path** dropdown.
1. Assign a title, a unit suffix, and a refresh rate.

#### Time series

The time series widget creates a graph of tabular data. You can add multiple lines to the time series widget to compare multiple readings over the same time period:

{{<imgproc src="/services/data/visualize-widget-time-series.png" resize="1000x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A time series widget displaying a live graph of sensor data over time.">}}

To configure the time series widget, define the following attributes for each line in the time series:

1. From the **Resource name** dropdown, choose a sensor you would like to visualize.
1. From the **Capture method** dropdown, choose a method of data capture (for example **Readings**).
1. From the **Path** dropdown, choose the field of data that this line should visualize.

Use the other fields to customize the title, unit, duration, and other aspects of your visualization.

The **window method** allows you to aggregate sensor readings over specified time intervals instead of displaying raw data points.
Select a window method from the following options:

- **None**: shows raw data with the path specified with no aggregation
- **Count**: shows the number of readings within the window
- **Average**: calculates the average value throughout the window
- **Minimum**: shows the minimum value within the window
- **Maximum**: shows the maximum value within the window
- **Custom**: shows the result of a custom MQL aggregation pipeline that you define

#### Table

The table widget displays a grid of historic tabular data values. You can display multiple fields simultaneously in a single table.
Each row in the table represents a separate historic reading; each column represents a field.

{{<imgproc src="/services/data/visualize-widget-table.png" resize="800x" style="width: 500px" class="fill imgzoom shadow" declaredimensions=true alt="A table widget displaying a grid of sensor readings.">}}

To configure the table widget, define the following attributes:

1. From the **Resource name** dropdown, choose a sensor you would like to visualize.
1. From the **Capture method** dropdown, choose a method of data capture (for example **Readings**).
1. From the **Path** dropdown, choose the data that this table should visualize.

Use a custom MQL aggregation pipeline stage (or series of stages) to transform your sensor data into a flat object where each field corresponds to a column in the table.
Consider the following sensor data, which contains information about air quality in a field named `readings`:

```json
"data" {
 "readings": {
  "gas_resistance": 114978.66606781945,
  "temperature": 22.96,
  "pressure": 1016.18,
  "humidity": 48.318
}
```

To visualize this data in a table with columns titled "gas_resistance," "temperature," "pressure," and "humidity," use the following custom MQL stage:

```mql
{
  "$project": {
    "data": 1
  }
}
```

Alternatively, specify individual fields in your `$project` stage to customize the titles of your columns:

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

## Third party tools

Configure data query and use a third-party visualization tool like Grafana to visualize your sensor data.

### Prerequisites

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the docs to [capture data](/data-ai/capture-data/capture-sync/) from a sensor.

{{% /expand%}}

{{% expand "The Viam CLI to set up data query. Click to see instructions." %}}

You must have the Viam CLI installed to configure querying with third-party tools.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

### Configure data query

If you want to query data from third party tools, you have to configure data query to obtain the credentials you need to connect to the third party service.

{{< readfile "/static/include/how-to/query-data.md" >}}

### Visualize data with third-party tools

When you sync captured data to Viam, that data is stored in the Viam organization’s MongoDB Atlas Data Federation instance.
You can use third-party visualization tools, such as Grafana, to visualize your data.
Your chosen third-party visualization tool must be able to connect to a [MongoDB Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/query/sql/connect/) instance as its data store.

Select a tab below to learn how to configure your visualization tool for use with Viam:

#### Grafana

{{< table >}}
{{% tablestep start=1 %}}
**Choose Grafana instance**

[Install](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) or set up Grafana.
You can use either a local instance of Grafana Enterprise or Grafana Cloud, and can use the free trial version of Grafana Cloud if desired.

{{% /tablestep %}}
{{% tablestep %}}
**Install connector to MongoDB data source**

Navigate to your Grafana web UI.
Go to **Connections > Add new connection** and add the [Grafana MongoDB data source](https://grafana.com/grafana/plugins/grafana-mongodb-datasource/) plugin to your Grafana instance.

{{<imgproc src="/tutorials/visualize-data-grafana/search-grafana-plugins.png" resize="800x" declaredimensions=true alt="The Grafana plugin search interface showing the results for a search for mongodb" class="shadow" >}}

Install the datasource plugin.

{{% /tablestep %}}
{{% tablestep %}}
**Configure a data connection**

Navigate to the Grafana MongoDB data source that you just installed.
Select **Add new data source**.

Enter the following information in the configuration UI for the plugin:

- **Connection string**: Enter the following connection string, and replace `<MONGODB-ATLAS-DF-HOSTNAME>` with your database hostname as configured with the `viam data database configure` command, and replace `<DATABASE-NAME>` with the desired database name to query.
  For most use cases with Viam, this database name will be `sensorData`:

  ```sh {class="command-line" data-prompt="$"}
  mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
  ```

- **User**: Enter the following username, substituting your organization ID as determined earlier, for `<YOUR-ORG-ID>`:

  ```sh {class="command-line" data-prompt="$"}
  db-user-<YOUR-ORG-ID>
  ```

- **Password**: Enter the password you provided earlier.

  {{<imgproc src="/tutorials/visualize-data-grafana/configure-grafana-mongodb-datasource.png" resize="800x" declaredimensions=true alt="The Grafana data source plugin configuration page, showing the connection string and username filled in with the configuration determined from the previous steps" class="shadow" >}}

{{< /tablestep >}}
{{% tablestep %}}
**Use Grafana for dashboards**

With your data connection established, you can then build dashboards that provide insight into your data.

Grafana additionally supports the ability to directly [query and transform your data](https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/) within a dashboard to generate more granular visualizations of specific data.
You might use this functionality to visualize only a single day's metrics, limit the visualization to a select machine or component, or to isolate an outlier in your reported data, for example.

You can query your captured data within a Grafana dashboard using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

For example, try the following query to obtain readings from a sensor, replacing `sensor-1` with the name of your component:

```mql
sensorData.readings.aggregate([
            {$match: {
              component_name: "sensor-1",
              time_received: {$gte: ISODate(${__from})}
              }},
            {$limit: 1000}
            ]
          )
```

See the [guide on querying data](/data-ai/data/query/) for more information.

<!-- markdownlint-disable-file MD034 -->

{{% /tablestep %}}
{{< /table >}}

#### Other visualization tools

{{< table >}}
{{% tablestep start=1 %}}
**Install connector to MongoDB data source**

Some visualization clients are able to connect to the Viam MongoDB Atlas Data Federation instance natively, while others require that you install and configure an additional plugin or connector.
For example, Tableau requires both the [Atlas SQL JDBC Driver](https://www.mongodb.com/try/download/jdbc-driver) as well as the [Tableau Connector](https://www.mongodb.com/try/download/tableau-connector) in order to successfully connect and access data.

Check with the documentation for your third-party visualization tool to be sure you have the required additional software installed to connect to a MongoDB Atlas Data Federation instance.

{{% /tablestep %}}
{{% tablestep %}}
**Configure a data connection**

Most third-party visualization tools require the _connection URI_ (also called the connection string) to that database server, and the _credentials_ to authenticate to that server in order to visualize your data.
Some third-party tools instead require a _hostname_ and _database name_ of the database server.
This is what they look like:

{{< tabs >}}
{{% tab name="Connection URI and credentials" %}}

If your client supports a connection URI, use the following format and replace `YOUR-PASSWORD-HERE` with your database password as configured with the `viam data database configure` command:

```sh {class="command-line" data-prompt="$"}
mongodb://db-user-abcdef12-abcd-abcd-abcd-abcdef123456:YOUR-PASSWORD-HERE@data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/?ssl=true&authSource=admin
```

You can also specify a desired database name in your connection URI, if desired.
For example, to use the `sensorData` database, the default database name for uploaded sensor data, your connection string would resemble:

```sh {class="command-line" data-prompt="$"}
mongodb://db-user-abcdef12-abcd-abcd-abcd-abcdef123456:YOUR-PASSWORD-HERE@data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/sensorData?ssl=true&authSource=admin
```

{{% /tab %}}
{{% tab name="Hostname and database name" %}}

If you client doesn't use a connection URI, you can supply the hostname and database name of the database server instead.
Substitute the hostname returned from the `viam data database hostname` command for `<MONGODB-ATLAS-DF-HOSTNAME>` and the desired database name to query for `<DATABASE-NAME>`:

```sh {class="command-line" data-prompt="$"}
mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
```

For example, to use the `sensorData` database, the default name for uploaded data, your connection string would resemble:

```sh {class="command-line" data-prompt="$"}
mongodb://data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/sensorData?directConnection=true&authSource=admin&tls=true
```

If you are using a connection URI, the hostname and database name are already included in the URI string.

You database user name is of the following form:

```sh {class="command-line" data-prompt="$"}
db-user-<YOUR-ORG-ID>
```

Substitute your organization ID for `<YOUR-ORG-ID>`.

{{< /tab >}}
{{% /tabs %}}

{{% /tablestep %}}
{{% tablestep %}}
**Use visualization tools for dashboards**

Some third-party visualization tools support the ability to directly query your data within their platform to generate more granular visualizations of specific data.
You might use this functionality to visualize only a single day's metrics, limit the visualization to a select machine or component, or to isolate an outlier in your reported data, for example.

While every third-party tool is different, you would generally query your data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
See the [guide on querying data](/data-ai/data/query/) for more information.

<!-- markdownlint-disable-file MD034 -->

{{% /tablestep %}}
{{< /table >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CGq3XIRQjUQ">}}

For more detailed instructions on using Grafana, including a full step-by-step configuration walkthrough, see [visualizing data with Grafana](/tutorials/services/visualize-data-grafana/).

On top of visualizing sensor data with third-party tools, you can also [query it with the Python SDK](/dev/reference/apis/data-client/) or [query it in the web UI](/data-ai/data/query/).

To see full projects using visualization, check out these resources:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{% manualcard link="https://www.viam.com/post/harnessing-the-power-of-tableau-to-visualize-sensor-data" img="services/data/tableau-preview.png" alt="Tableau dashboard" %}}

### Visualize data with Tableau

Turn a data dump into valuable insights that drive smarter decision-making and monitor sensor data in real-time.

{{% /manualcard %}}
{{< /cards >}}
