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

Once you have used the data management service to [capture data](/use-cases/collect-sensor-data/), you can visualize your data with a variety of third-party tools, including Grafana, Tableau, Google's Looker Studio, and more.
You can choose to visualize data from a component on one machine, from multiple components together, or from many components across a fleet of machines.

For example, you can configure data capture for several sensors across multiple machines to report the ambient operating temperature.
You can then visualize that data to easily understand how the ambient temperature affects your machines' operation.

You can do all of this using the [Viam app](https://app.viam.com/) user interface. You will not need to write any code.

{{< alert title="In this page" color="tip" >}}

1. [Configuring data query](#configure-data-query).
1. [Visualizing data with third-party tools](#visualize-data-with-third-party-tools).

{{< /alert >}}

## Prerequisites

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the guide to [capture sensor data](/use-cases/collect-sensor-data/).

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

Select a tab below to learn how to configure your visualization tool for use with Viam:

{{< tabs >}}
{{% tab name="Grafana" %}}

{{< table >}}
{{< tablestep >}}
**1. Choose Grafana instance**

Install or set up Grafana. You can use either a local instance of Grafana or Grafana Cloud, and can use the free trial version of Grafana if desired.

{{< /tablestep >}}
{{< tablestep >}}
**2. Install connector to MongoDB data source**

Navigate to your Grafana web UI, and add the [Grafana MongoDB data source](https://grafana.com/grafana/plugins/grafana-mongodb-datasource/) plugin to your Grafana instance.

{{<imgproc src="/tutorials/visualize-data-grafana/search-grafana-plugins.png" resize="800x" declaredimensions=true alt="The Grafana plugin search interface showing the results for a search for mongodb">}}

{{< /tablestep >}}
{{< tablestep >}}
**3. Configure a data connection**

Navigate to the Grafana data source management page, and select the Grafana MongoDB data source that you just added.

Enter the following information in the configuration UI for that plugin:

- **Connection string**: Enter the following connection string, and replace `<MONGODB-ATLAS-DF-HOSTNAME>` with your database hostname as configured with the `viam data database configure` command, and replace `<DATABASE-NAME>` with the desired database name to query:

  ```sh
  mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
  ```

- **Credentials: User**: Enter the following username, substituting your organization ID as determined earlier, for `<YOUR-ORG-ID>`:

  ```sh
  db-user-<YOUR-ORG-ID>
  ```

- **Credentials: Password**: Enter the password you provided earlier.

{{<imgproc src="/tutorials/visualize-data-grafana/configure-grafana-mongodb-datasource.png" resize="800x" declaredimensions=true alt="The Grafana data source plugin configuration page, showing the connection string and username filled in with the configuration determined from the previous steps">}}

{{< /tablestep >}}
{{< tablestep >}}
**4. Use visualization tools for dashboards**

Some third-party visualization tools support the ability to directly query your data within their platform to generate more granular visualizations of specific data.
You might use this functionality to visualize only a single day's metrics, limit the visualization to a select machine or component, or to isolate an outlier in your reported data, for example.

While every third-party tool is different, you would generally query your data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
See the [guide on querying sensor data](/use-cases/sensor-data-query/) for more information.

<!-- markdownlint-disable-file MD034 -->

{{< /tablestep >}}
{{< /table >}}

{{% /tab %}}
{{% tab name="Other visualization tools" %}}

{{< table >}}
{{< tablestep >}}
**1. Install connector to MongoDB data source**

Some visualization clients are able to connect to the Viam MongoDB Atlas Data Federation instance natively, while others require that you install and configure an additional plugin or connector.
For example, Tableau requires both the [Atlas SQL JDBC Driver](https://www.mongodb.com/try/download/jdbc-driver) as well as the the [Tableau Connector](https://www.mongodb.com/try/download/tableau-connector) in order to successfully connect and access data.

Check with the documentation for your third-party visualization tool to be sure you have the required additional software installed to connect to a MongoDB Atlas Data Federation instance.

{{< /tablestep >}}
{{< tablestep >}}
**2. Configure a data connection**

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

{{< /tablestep >}}
{{< tablestep >}}
**3. Use visualization tools for dashboards**

Some third-party visualization tools support the ability to directly query your data within their platform to generate more granular visualizations of specific data.
You might use this functionality to visualize only a single day's metrics, limit the visualization to a select machine or component, or to isolate an outlier in your reported data, for example.

While every third-party tool is different, you would generally query your data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
See the [guide on querying sensor data](/use-cases/sensor-data-query/) for more information.

<!-- markdownlint-disable-file MD034 -->

{{< /tablestep >}}
{{< /table >}}

{{< /tabs >}}
{{< /tabs >}}

## Next steps

For more detailed instructions on using Grafana, including a full step-by-step configuration walkthrough, see [visualizing data with Grafana](/tutorials/services/visualize-data-grafana/).

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
