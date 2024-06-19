---
title: "Visualize sensor data from any machines"
linkTitle: "Visualize and analyze sensor data"
weight: 32
type: "docs"
images: ["/services/icons/data-visualization.svg"]
description: "Visualize sensor data from the Viam app using popular tools like Grafana."
modulescript: true
aliases:
  - /data/visualize/
---

You can use the data management service to capture sensor or time-series data from any machine and sync that data to the cloud.
Then, you can visualize your data with a variety of third-party tools, including Grafana, Tableau, Google's Looker Studio, and more.
You can choose to visualize data from a component on one machine, from multiple components together, or from many components across a fleet of machines, all from a single pane of glass.

For example, you can configure data capture for several sensors on one machine or for several sensors across multiple machines to report the ambient operating temperature.
You can then visualize that data to easily understand how the ambient temperature affects your machines' operation.

You can do all of this using the [Viam app](https://app.viam.com/) user interface. You will not need to write any code.

{{< alert title="In this page" color="tip" >}}

1. [Configuring data query](#configure-data-query).
1. [Visualizing data with third-party tools](#visualize-data-with-third-party-tools).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "At least one configured sensor. Click to see instructions." %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a sensor model](/components/sensor/) that supports your sensor.

{{% /expand%}}

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the guide to [capture sensor data](/use-cases/sensor-data-query/).

If you're not sure which sensor model to choose, start with the [`viam:viam-sensor:telegrafsensor`](https://github.com/viamrobotics/viam-telegraf-sensor) which captures performance data (CPU, memory usage, and more) from your machine.

{{% /expand%}}

{{% expand "The Viam CLI to set up data query. Click to see instructions." %}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

## Configure data query

If you want to query data from third party tools, you have to configure data query to obtain the credentials you need to connect to the third party service.

{{< readfile "/static/include/how-to/query-data.md" >}}

## Visualize data with third-party tools

When you sync captured data to Viam, that data is stored in the Viam organization’s MongoDB Atlas Data Federation instance.
Your chosen third-party visualization tool must be able to connect to a [MongoDB Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/query/sql/connect/) instance as its data store.

{{< table >}}
{{< tablestep >}}
**1. Install connector to MongoDB data source**

For example, if you are using [Grafana](https://grafana.com/), you must install and configure the [Grafana MongoDB data source](https://grafana.com/grafana/plugins/grafana-mongodb-datasource/) plugin.
See the [Visualize Data Using Grafana](/tutorials/services/visualize-data-grafana/) tutorial for a detailed walkthrough for Grafana.
{{< /tablestep >}}
{{< tablestep >}}
**2. Configure a data connection**

Most third-party visualization tools require the _connection URI_ (also called the connection string) to that database server, and the _credentials_ to authenticate to that server in order to visualize your data.
Some third-party tools instead require a _hostname_ and _database name_ of the database server.
This is what they look like:

{{< tabs >}}
{{% tab name="Connection URI and credentials" %}}

If your client supports a connection URI, use the following format:

```sh {class="command-line" data-prompt="$"}
mongodb://db-user-abcdef12-abcd-abcd-abcd-abcdef123456:YOUR-PASSWORD-HERE@data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/?ssl=true&authSource=admin
```

You can also specify a desired database name in your connection URI, if desired.
For example, to use the `sensorData` database, the default name for uploaded data, your connection string would resemble:

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

{{% /tab %}}
{{< /tabs >}}

{{< /tablestep >}}
{{< tablestep >}}
**3. Using visualization tools for dashboards**

You can choose to visualize data from a component on one machine, from multiple components together, or from many components across a fleet of machines, all from a single pane of glass.

Some third-party visualization tools support the ability to directly query your data within their platform to generate more granular visualizations of specific data.
You might use this functionality to visualize only a single day's metrics, limit the visualization to a select machine or component, or to isolate an outlier in your reported data, for example.

While every third-party tool is different, you would generally query your data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}. See the following guide on [querying sensor data](/use-cases/sensor-data-query/) for more information.

<!-- markdownlint-disable-file MD034 -->

{{< /tablestep >}}
{{< /table >}}

## Next steps

For a walkthrough of visualizing data with a specific tool, see [visualizing data with Grafana](/tutorials/services/visualize-data-grafana/).

On top of visualizing sensor data with third-party tools, you can also [query it with the Python SDK](/use-cases/sensor-data-query-sdk/) or [query it with the Viam app](/use-cases/sensor-data-query/).

{{< cards >}}
{{% card link="/use-cases/sensor-data-query-sdk/" %}}
{{% card link="/use-cases/sensor-data-query/" %}}
{{< /cards >}}

To see full projects using visualization, check out these resources:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{% manualcard link="https://www.viam.com/post/harnessing-the-power-of-tableau-to-visualize-sensor-data" img="services/data/tableau-preview.png" imageAlt="Tableau dashboard" %}}

### Visualize data with Tableau

Turn a data dump into valuable insights that drive smarter decision-making and monitor sensor data in real-time.

{{% /manualcard %}}
{{< /cards >}}
