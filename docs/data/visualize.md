---
title: "Visualize Data with Dashboards"
linkTitle: "Visualize Data"
weight: 50
no_list: true
type: "docs"
tags: ["data management", "data", "services", "visualize"]
description: "Visualize tabular data from the Viam app using popular tools like Grafana."
icon: true
images: ["/services/icons/data-visualization.svg"]
# SME: Devin Hilly
---

Once you have [configured data query](/data/query/#configure-data-query) for your organization's data store, you can visualize your data from a variety of third-party tools, including Grafana, Tableau, Google's Looker Studio, and more.
You can choose to visualize data from a component on one machine, from multiple components together, or from many components across a fleet of machines, all from a single pane of glass.

You can visualize both the captured data itself as well as its metadata, including machine ID, organization ID, and [tags](/data/dataset/#image-tags).

Only components that capture tabular data, such as [sensor](/components/sensor/) readings or other time-series data, support data visualization.

{{% alert title="Tip" color="tip" %}}

For a full walkthrough using Grafana specifically, see the [Visualize Data Using Grafana](/tutorials/services/visualize-data-grafana/) tutorial.

{{% /alert %}}

## Requirements

Before you can visualize your data, you must:

1. [Add the data management service](/data/capture/#add-the-data-management-service) to your machine.
1. [Configure data capture](/data/capture/) for at least one component, such as a sensor.
   Only components that capture tabular data support data visualization.
1. [Configure cloud sync](/data/cloud-sync/), and sync data to the Viam app.
   When you are able to [view your data in the Viam app](/data/view/), you are ready to proceed.
1. [Configure data query](/data/query/#configure-data-query) to allow third-party visualization tools, such as Grafana, to access your synced data.

Your chosen third-party visualization tool must be able to connect to a [MongoDB Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/query/sql/connect/) instance as its data store.
For example, if you are using [Grafana](https://grafana.com/), you must install and configure the [Grafana MongoDB data source](https://grafana.com/grafana/plugins/grafana-mongodb-datasource/) plugin.
See the [Visualize Data Using Grafana](/tutorials/services/visualize-data-grafana/) tutorial for a detailed walkthrough.

## Visualize data using third-party tools

With data query configured, you can use a variety of popular third-party tools to access and visualize that data in a configurable manner.

### Configure a data connection

When you sync captured data to Viam, that data is stored in the Viam organization’s MongoDB Atlas Data Federation instance.

Most third-party visualization tools require the _connection string_ to that database server, and the _credentials_ to authenticate to that server in order to visualize your data.

When you [configured data query](/data/query/#configure-data-query), this information was provided to you:

- **Connection string**: The connection string your visualization tool uses to connect to and query your data.
  Substitute the hostname returned from the `viam data database hostname` command for `<MONGODB-ATLAS-DF-HOSTNAME>` and the desired database name to query for `<DATABASE-NAME>`:

  ```sh
  mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
  ```

  For example, to use the `sensorData` database, the default name for uploaded tabular data, your connection string would resemble:

  ```sh
  mongodb://data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/sensorData?directConnection=true&authSource=admin&tls=true
  ```

- **Username**: Your database user. Substitute your organization ID for `<YOUR-ORG-ID>`:

  ```sh
  db-user-<YOUR-ORG-ID>
  ```

  For example, your connection string would resemble:

  ```sh
  db-user-abcdef12-abcd-abcd-abcd-abcdef123456
  ```

- **Password**: Your chosen password for your database user, configured with the `viam data database` command.

With your data connection configured, you can then follow the instructions for your specific third-party visualization tool to be able to visualize that data on your chosen platform.

### Write queries to visualize specific data

Some third-party visualization tools support the ability to directly query your data within their platform to generate more granular visualizations of specific data.
You might use this functionality to visualize only a single day's metrics, limit the visualization to a select machine or component, or to isolate an outlier in your reported data, for example.

While every third-party tool is different, you would generally query your data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

See [Query your data](/data/query/#query) for examples.

## Next steps

For a detailed walkthrough of setting up a Grafana instance to visualize your machine's data, see the following tutorial:

{{< cards >}}
{{% card link="/tutorials/services/visualize-data-grafana/" %}}
{{< /cards >}}
