---
title: "Visualize Data With Grafana"
linkTitle: "Visualize Data With Grafana"
type: "docs"
description: "Collect data from your machine or fleet and visualize it in Grafana."
imageAlt: "Grafana visualization showing collected temperature readings from a fleet of machines."
images: ["/tutorials/visualize-data-grafana/grafana-dashboard-preview.png"]
tags: ["data management", "data", "services", "visualize"]
authors: []
languages: []
viamresources: ["data_manager"]
platformarea: ["data"]
level: "Intermediate"
date: "2024-01-19"
cost: "0"
no_list: true
# SMEs: Data team, Natalia Jacobowitz
---

<!-- After following this tutorial, you will be able to use the data management service to capture and sync sensor data from your machine to Viam, from which you can then configure a visualization dashboard such as Grafana to view and optionally query your sensor readings. -->

Once you have [configured data query](/data-ai/data/query/#query-data-using-third-party-tools) for your organization's data store, you can visualize your data from a variety of third-party tools, including Grafana.

You can choose to visualize data from a component on one machine, from multiple components together, or from many components across a fleet of machines, all from a single pane of glass.

Only components that capture [sensor](/operate/reference/components/sensor/) readings or other time-series data support data visualization.

You can visualize both the captured data itself as well as its metadata, including machine ID, organization ID, and tags.

Follow the steps in this tutorial to learn how to collect data from your machine, sync that data to Viam, enable third-party access to that data, and present that data visually and flexibly in Grafana.

{{% alert title="Info" color="info" %}}
This tutorial focuses on using Grafana to visualize your captured data.
For general guidance appropriate for any third-party visualization tool, see [Visualize data](/data-ai/data/visualize/).
{{% /alert %}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CGq3XIRQjUQ">}}

## Prerequisites

Before following this tutorial, ensure you have:

- Added a new machine on [Viam](https://app.viam.com) and follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} to install `viam-server` on the computer you're using for your project and connect to Viam.
- A configured [sensor component](/operate/reference/components/sensor/), such as the [`bme280`](https://app.viam.com/module/viam/bosch) sensor, that reports data.
  If it's a physical sensor, make sure to connect it to your machine's computer.

  - This tutorial uses a dataset of plant moisture measurements, originally captured for our [Plant watering tutorial](/tutorials/projects/make-a-plant-watering-robot/) using an analog resistive soil moisture sensor connected to an analog-to-digital-converter (ADC).
    The ADC functionality was provided by the [`mcp300x-adc-sensor` module](https://app.viam.com/module/hazalmestci/mcp300x-adc-sensor) from the [registry](https://app.viam.com/registry).

  - If you already have data synced to Viam that you want to use, you can skip this requirement, and can skip directly to the [Configure data query](#configure-data-query) portion of this tutorial.

- A Grafana instance.

  - You can use either a local instance of Grafana Enterprise, or Grafana Cloud.
    This tutorial will use Grafana Cloud.
  - You can use the free trial version of Grafana Cloud.

## The data management service

You can manage how your machine captures and syncs data to the cloud using the data management service.

### Add the data management service

First, add the data management service to your machine to be able capture and sync data:

1. Navigate to your machine's **CONFIGURE** tab.
1. Click the **+** button in the left-hand menu and select **Component or service** from the dropdown.
1. Select **data management**.
1. Give the service a name, like `viam-data-manager`, then click **Create**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data locally to the <file>~/.viam/capture</file> directory, and syncs captured data files to Viam every 6 seconds (`0.1` minutes in the configuration).
   Leave the default settings as they are, and click **Save** in the upper-right corner of the screen to save your changes.

   {{< imgproc src="/tutorials/data-management/data-management-conf.png" alt="The data management service configuration pane with default settings shown for both capturing and syncing" resize="900x" >}}

For more information, see [data management service configuration](/data-ai/capture-data/capture-sync/).

### Configure data capture for a component

Once you have added the data management service, you can configure data capture for specific components on your machine.
For this tutorial, you will configure data capture for a [sensor](/operate/reference/components/sensor/) component, gathering sensor readings to later visualize in Grafana.
Only sensor readings or other time-series data can be visualized in this manner.

To enable data capture for a sensor component:

1. Navigate to your machine's **CONFIGURE** tab.

1. In the configuration pane for your [configured sensor component](#prerequisites), find the **Data capture** section, and click the **Add method** button to enable data capture for this camera.

   - Set the **Method** to `Readings` and the **Frequency** to `0.333`.
     This will capture readings from the sensor device roughly once every 3 seconds.
     You can adjust the capture frequency if you want the sensor to capture more or less data, but avoid configuring data capture to higher rates than your hardware can handle, as this could lead to performance degradation.

     {{< imgproc src="/tutorials/visualize-data-grafana/sensor-data-capture.png" alt="The sensor component configuration pane with data capture configuration enabled using type Readings and a capture frequency of 0.333" resize="900x" >}}

1. Click **Save Config** at the bottom of the window to save your changes.

After a short while, your sensor will begin capturing live readings, and syncing those readings to Viam.
You can check that data is being captured and synced by clicking on the menu icon on the sensor configuration pane. and selecting **View captured data**.

For more information see [data management service configuration](/data-ai/capture-data/capture-sync/).

### Configure data query

Next, enable the ability to query your synced data.
When you sync captured data to Viam, that data is stored in the Viam organization’s [MongoDB Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance.
Configuring data query allows you to directly [query your data](/data-ai/data/query/#query-using-third-party-tools) using a compatible client (such as `mongosh`) or Grafana to access that data and visualize it.

To enable data query:

1. Follow the steps to [configure data query](/data-ai/data/query/#configure-data-query).

1. Note the username and hostname returned from these steps, in addition to the password you chose for that user.
   You will use this information in the next section.

## Configure Grafana

With your machine capturing data and syncing it to Viam, and direct query of that data configured, you can now configure Grafana to access and visualize that data:

1. Navigate to your Grafana web UI, and add the [Grafana MongoDB data source](https://grafana.com/grafana/plugins/grafana-mongodb-datasource/) plugin to your Grafana instance.

   {{<imgproc src="/tutorials/visualize-data-grafana/search-grafana-plugins.png" resize="800x" declaredimensions=true alt="The Grafana plugin search interface showing the results for a search for mongodb">}}

   For more information, see [Install Grafana Plugins](https://grafana.com/docs/grafana/latest/administration/plugin-management/#install-grafana-plugins).

1. Navigate to the Grafana data source management page, and select the Grafana MongoDB data source that you just added.
   For more information, see [Grafana data source management](https://grafana.com/docs/grafana/latest/administration/data-source-management/).

1. Enter the following information in the configuration UI for that plugin:

   - **Connection string**: Enter the following connection string, substituting the hostname returned from the previous section for `<MONGODB-ATLAS-DF-HOSTNAME>` and the desired database name to query for `<DATABASE-NAME>`:

     ```sh {class="command-line" data-prompt="$"}
     mongodb://<MONGODB-ATLAS-DF-HOSTNAME>/<DATABASE-NAME>?directConnection=true&authSource=admin&tls=true
     ```

     For example, to use the `sensorData` database, the default name for uploaded sensor data, your connection string would resemble:

     ```sh {class="command-line" data-prompt="$"}
     mongodb://data-federation-abcdef12-abcd-abcd-abcd-abcdef123456-e4irv.a.query.mongodb.net/sensorData?directConnection=true&authSource=admin&tls=true
     ```

     The connection string is specific to your organization ID and configured user.
     You must have followed the steps under [configure data query](/data-ai/data/query/#configure-data-query) previously in order for this URL to be valid.

   - **Credentials: User**: Enter the following username, substituting your organization ID as determined earlier, for `<YOUR-ORG-ID>`:

     ```sh {class="command-line" data-prompt="$"}
     db-user-<YOUR-ORG-ID>
     ```

     For example, using the organization ID from the previous example, your connection string would resemble:

     ```sh {class="command-line" data-prompt="$"}
     db-user-abcdef12-abcd-abcd-abcd-abcdef123456
     ```

   - **Credentials: Password**: Enter the password you provided when you [configured data query](/data-ai/data/query/#configure-data-query) previously.

   {{<imgproc src="/tutorials/visualize-data-grafana/configure-grafana-mongodb-datasource.png" resize="800x" declaredimensions=true alt="The Grafana data source plugin configuration page, showing the connection string and username filled in with the configuration determined from the previous steps">}}

1. Click the **Save & test** button to save your settings.
   Grafana will perform a health check on your configuration settings to verify that everything looks good.

This connection allows Grafana to access all synced sensor data under your [organization](/dev/reference/glossary/#organization), from any machine.

## Visualize your data

With the data connection configured, Grafana now has access to your data and you are ready to create a new dashboard to visualize that data.

- If you are using a local Grafana instance, see [Build your first dashboard](https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/)
- If you are using Grafana Cloud, see [Create a dashboard in Grafana Cloud](https://grafana.com/docs/grafana-cloud/visualizations/dashboards/build-dashboards/create-dashboard/)

When prompted to select a data source, select the MongoDB data source that you added earlier.

{{<imgproc src="/tutorials/visualize-data-grafana/grafana-add-new-connection.png" resize="800x" declaredimensions=true alt="The Grafana configuration page for adding a new connection, with the MongoDB data source shown">}}

{{% alert title="Note" color="note" %}}
Be sure to install the MongoDB _data source_, not the _integration_.
{{% /alert %}}

Select the visualization type that matches your data, which is most likely **Time series**.

When done, click **Save** to save your dashboard.

The example below displays readings from a fleet of deployed machines, each equipped with a temperature sensor, reporting the ambient temperature of the office over the course of the day.

{{<imgproc src="/tutorials/visualize-data-grafana/grafana-dashboard-example.png" resize="800x" declaredimensions=true alt="An example Grafana dashboard, showing the temperature readings from a fleet of deployed machines with temperature sensors, plotted over the course of the day, with separate colors for each sensor.">}}

{{< alert title="Tip" color="tip" >}}
If you have a lot of data, or are exploring an existing data set that you are not familiar with, you may find it useful to browse your data first, before creating a visualization dashboard based on it.

You can use [MongoDB Compass](https://www.mongodb.com/products/tools/compass) to connect to your Viam data store using the same connection string and credentials as above, and browse your data using Compass' [Schema Analyzer](https://www.mongodb.com/docs/compass/current/schema/), which offers fast insights into what types of data you have available.

{{<imgproc src="/tutorials/visualize-data-grafana/compass-schema-analyzer.png" resize="800x" declaredimensions=true alt="The MongoDB Compass Schema tab, showing the data types and relative makeup of the moisture sensor readings dataset.">}}
{{< /alert >}}

### Query your data in Grafana

You can also use query language directly in Grafana using the [MongoDB Query Editor](https://grafana.com/docs/plugins/grafana-mongodb-datasource/latest/query-editor/), which enables data query functionality similar to that of the MongoDB shell, `mongosh`.

For example, to limit the visualization of the plant watering data set to just the `moisture-sensor` component, within a certain time range, and limiting returned results to 1000 records, you could use the following query in the query editor:

```mongodb {class="command-line" data-prompt=">"}
sensorData.readings.aggregate([
            {$match: {
              component_name: "moisture-sensor",
              time_received: {$gte: ISODate(${__from})}
              }},
            {$limit: 1000}
            ]
          )

```

This query uses the Grafana global variable `$__from`, which is populated by the value set from the `From` dropdown menu on your dashboard, allowing for visualizations based on this query to be dynamically updated when you change your desired time range from that dropdown menu.
See Grafana's [Global variables documentation](https://grafana.com/docs/grafana/latest/dashboards/variables/add-template-variables/#global-variables) for more information.

{{% alert title="Performance Tip" color="tip" %}}
To improve performance when querying large datasets, see [Query optimization and performance best practices](/data-ai/data/query/#query-optimization-and-performance-best-practices).
{{% /alert %}}

{{<imgproc src="/tutorials/visualize-data-grafana/grafana-dashboard-query.png" resize="1000x" declaredimensions=true alt="A Grafana dashboard configuration screen, showing an MQL query entered to limit the visualization to the specific moisture-sensor component, and using the $__from variable to allow for use of a UI dropdown to control the time range.">}}

## Next steps

In this tutorial, you learned:

- how to use the [data management service](/data-ai/capture-data/capture-sync/) to capture data from your machine and sync it to Viam
- how to [enable data query access](/data-ai/data/query/#configure-data-query) to your synced data
- how to connect Grafana to your data
- how to build a dashboard visualizing that data
- how to use query language to dynamically update the visualization based on UI selections

From here you could:

- include data from additional sensors, or from more machines in your fleet, to be able to view everything together from a single pane of glass
- experiment with your query language syntax to give more flexibility to the operator, by allowing for more UI-based customization of the visualization using Grafana global variables

For more ideas, check out our other [tutorials](/tutorials/).

{{< snippet "social.md" >}}
