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
  - /tutorials/services/visualize-data-grafana/
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "fleet"]
date: "2024-12-04"
updated: "2025-09-10"
description: "Use teleop or Grafana to visualize captured sensor data."
---

Once you have used the data management service to [capture data](/data-ai/capture-data/capture-sync/), you can visualize your data using

- a [Teleop](#teleop-dashboard) dashboard
- a variety of [third-party tools](#third-party-tools), including Grafana, Tableau, Google's Looker Studio, and more

## Teleop dashboard

Create a dashboard to visualize data for machines in your organization.

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

1. Enter a unique name for your workspace in the top left of the page, replacing the placeholder `untitled-workspace` text.

1. Use the **Select location** dropdown to select the location that contains the machine that you would like to visualize data from.

1. Use the **Select machine** dropdown to select the machine that you would like to visualize data from.

### Add a widget

1. Click **Add widget** and select a widget type to create a new widget on your workspace.

   See [widget types](/manage/troubleshoot/teleoperate/custom-interface/#widget-types) for more information about each type.

1. To configure the widget, click the pencil icon in the top right of your widget:

   {{<imgproc src="/services/data/visualize-widget-configure.png" alt="Click the pencil icon to configure your widget." style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

You can mix and match multiple widgets to visualize many kinds of data collected by your machine:

{{<imgproc src="/services/data/visualize-workspace.png" resize="1200x" style="width: 700px" class="fill imgzoom shadow" declaredimensions=true alt="Workspace containing multiple widgets displaying sensor data visualizations.">}}

To arrange widgets on your workspace, click and drag the grid icon in the top left of your widget:

{{<imgproc src="/services/data/visualize-widget-move.png" alt="Click the grid icon to move a widget." style="width:500px" resize="1200x" class="imgzoom fill shadow" >}}

## Third party tools

When you sync captured data to Viam, that data is stored in a MongoDB Atlas Data Federation instance.
You can use third-party visualization tools, such as Grafana, to connect to it and visualize your data, as long as the tool supports [MongoDB Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/query/sql/connect/) as a data store.

To use a third-party visualization tool like Grafana to visualize your data, you must first [configure data query](#configure-data-query).

### Prerequisites

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the docs to [capture data](/data-ai/capture-data/capture-sync/) from a sensor.

{{% /expand%}}

{{% expand "The Viam CLI to set up data query. Click to see instructions." %}}

You must have the Viam CLI installed to configure querying with third-party tools.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

### Configure data query

Configuring data query will provide you with the credentials you need to connect to your data using a compatible client such as `mongosh`, Grafana, or a third-party visualization service.

{{< readfile "/static/include/how-to/query-data.md" >}}

{{< alert title="Tip" color="tip" >}}
You may find it useful to browse your data first, before creating a visualization dashboard based on it.
We recommend [MongoDB Compass](https://www.mongodb.com/products/tools/compass) to connect to your Viam data store.
Once connected, browse your data using Compass' [Schema Analyzer](https://www.mongodb.com/docs/compass/current/schema/) to see the types of data you have available.
{{< /alert >}}

### Visualize data with third-party tools

You can use the connection information you obtained when [configuring data query](#configure-data-query) with any third-party tool that supports MongoDB Atlas Data Federation as its data store.

Once connected, you can visualize captured sensor readings as well as any other time-series data, including metadata such as machine ID, organization ID, and tags.

Below are the steps for [Grafana](#grafana) and for [other visualization tools](#other-visualization-tools).

#### Grafana

{{< table >}}
{{% tablestep start=1 %}}
**Choose Grafana instance**

[Install](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) or set up Grafana.
You can use either a local instance of Grafana Enterprise or Grafana Cloud.
The free trial version of Grafana Cloud is sufficient for testing.

{{% /tablestep %}}
{{% tablestep %}}
**Install connector to MongoDB data source**

Navigate to your Grafana web UI.
Go to **Connections > Add new connection** and add the [Grafana MongoDB data source](https://grafana.com/grafana/plugins/grafana-mongodb-datasource/) plugin to your Grafana instance.

{{% alert title="Note" color="note" %}}
Be sure to install the MongoDB _data source_, not the _integration_.
{{% /alert %}}

{{<imgproc src="/tutorials/visualize-data-grafana/search-grafana-plugins.png" resize="800x" style="width: 500px" declaredimensions=true alt="The Grafana plugin search interface showing the results for a search for mongodb" class="shadow imgzoom" >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure a data connection**

On the page of the Grafana MongoDB data source that you just installed, select **Add new data source**.

Enter the following information in the configuration UI for the plugin:

- **Connection string**: Enter the following connection string.
  Then replace `<MONGODB-ATLAS-DF-HOSTNAME>` with your database hostname as configured with the `viam data database configure` command.
  The `<DATABASE-NAME>` for sensor data is `sensorData`.

  ```sh {class="command-line" data-prompt="$"}
  mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
  ```

- **User**: Enter the following username, substituting your organization ID for `<YOUR-ORG-ID>`:

  ```sh {class="command-line" data-prompt="$"}
  db-user-<YOUR-ORG-ID>
  ```

- **Password**: Enter the password for the database user.
  This is the password provided when configuring data query.

  {{<imgproc src="/tutorials/visualize-data-grafana/configure-grafana-mongodb-datasource.png" resize="800x" style="width: 500px" declaredimensions=true alt="The Grafana data source plugin configuration page, showing the connection string and username filled in with the configuration determined from the previous steps" class="shadow imgzoom" >}}

For more information on the Grafana MongoDB plugin, see [Configure the MongoDB data source](https://grafana.com/docs/plugins/grafana-mongodb-datasource/latest/configure/).

{{< /tablestep >}}
{{% tablestep %}}
**Use Grafana for dashboards**

With your data connection established, Grafana can now access all synced sensor data under your [organization](/dev/reference/glossary/#organization), from any machine.

You can now build dashboards that provide insight into your data.

You can also [query and transform your data](https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/).
This way, you can visualize different things, such as:

- a single day's data
- a single machine's or component's data
- outliers in your data

{{% expand "Click here for resources on building a Grafana Dashboard." %}}

- Local Grafana instance: [Build your first dashboard](https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/)
- Grafana Cloud: [Create a dashboard in Grafana Cloud](https://grafana.com/docs/grafana-cloud/visualizations/dashboards/build-dashboards/create-dashboard/)

{{% /expand%}}

{{< /tablestep >}}
{{% tablestep %}}
**Query data from Grafana**

You can also use query language directly in Grafana using the [MongoDB Query Editor](https://grafana.com/docs/plugins/grafana-mongodb-datasource/latest/query-editor/), which enables data query functionality similar to that of the MongoDB shell, `mongosh`.

For example, try the following query to obtain readings from a sensor, replacing `sensor-1` with the name of your component:

```mql
sensorData.readings.aggregate([
  {
    $match: {
      component_name: "sensor-1",
      time_received: { $gte: ISODate(${__from}) }
    }
  },
  { $limit: 1000 }
])
```

This query uses the Grafana global variable `$__from`, which is populated by the value set from the `From` dropdown menu on your dashboard.
The value is dynamically updated when you change your desired time range from that dropdown menu.
See Grafana's [Global variables documentation](https://grafana.com/docs/grafana/latest/dashboards/variables/add-template-variables/#global-variables) for more information.

{{< /tablestep >}}
{{% tablestep %}}
**Optimize your queries**

For optimal performance when querying large datasets, see [query optimization and performance best practices](/data-ai/data/query/#query-optimization-and-performance-best-practices).

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

You can also specify a database name in your connection URI.
For example, to use the `sensorData` database, the default database name for uploaded sensor data, your connection string would resemble:

```sh {class="command-line" data-prompt="$"}
mongodb://db-user-abcdef12-abcd-abcd-abcd-abcdef123456:YOUR-PASSWORD-HERE@data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/sensorData?ssl=true&authSource=admin
```

{{% /tab %}}
{{% tab name="Hostname and database name" %}}

If your client doesn't use a connection URI, you can supply the hostname and database name of the database server instead.

Substitute the hostname returned from the `viam data database hostname` command for `<MONGODB-ATLAS-DF-HOSTNAME>` and the desired database name to query for `<DATABASE-NAME>`:

```sh {class="command-line" data-prompt="$"}
mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
```

For example, to use the `sensorData` database, the default name for uploaded data, your connection string would resemble:

```sh {class="command-line" data-prompt="$"}
mongodb://data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/sensorData?directConnection=true&authSource=admin&tls=true
```

Your database user name is of the following form:

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
If available, you can use this functionality to visualize different things, such as:

- a single day's data
- a single machine's or component's data
- outliers in your data

While every third-party tool is different, you would generally query your data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
See the [guide on querying data](/data-ai/data/query/) for more information.
For optimal performance when querying large datasets, see the [query optimization and performance best practices](/data-ai/data/query/#query-optimization-and-performance-best-practices) section.

<!-- markdownlint-disable-file MD034 -->

{{% /tablestep %}}
{{< /table >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CGq3XIRQjUQ">}}
