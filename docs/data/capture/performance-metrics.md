---
title: "Performance Monitoring Data Capture"
linkTitle: "Monitor Performance"
description: "Capture and sync data about your machines' performance."
weight: 12
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: true
images: ["/data/monitor.gif"]
videos: ["/data/monitor.webm", "/data/monitor.mp4"]
aliases:
  - "/services/data/capture/"
# SME: Alexa Greenberg
---

You can capture and monitor the following metrics about the performance of individual machines or your entire fleet:

- **Wireless Signal Strength and Quality**: signal level, link quality, and noise level
- **Memory Usage**: memory statistics, including total available memory, used percentage, and specifics on various types of memory (cached, free, slab, etc.)
- **CPU Utilization**: CPU usage across different states (user, system, idle, etc.)
- **Disk I/O**: metrics on read and write operations, including bytes transferred and operation times
- **Network Traffic**: detailed network statistics, including bytes sent and received, packet information, and error counts, providing a deep dive into a device's network performance

## Requirements

To capture data from a machine, you need to [create a machine in Viam](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine) and follow the setup instructions to install `viam-server` and connect it to the Viam app.

{{< alert title="Note" color="note" >}}
You must run `viam-server` with `sudo` to monitor machine performance metrics.
{{< /alert >}}

## Add sensor to measure performance metrics

To obtain performance metrics about your machine, use the [`viam-telegraf-sensor`](https://app.viam.com/module/viam/viam-telegraf-sensor) module from the [Viam registry](/registry/).
The module provides a [sensor](/components/sensor/) that allows you to obtain readings containing your machine's performance metrics.

1. Go to your machine's **Config** page and click **Create component**.
2. Then select the `viam:viam-sensor:telegrafsensor` model from the [`viam-telegraf-sensor` module](https://app.viam.com/module/viam/viam-telegraf-sensor).
3. Click **Add module**, then enter a name for your sensor, for example `my-telegrafsensor`, and click **Create**.

In the next step you will configure the data manager to capture and sync the performance metrics from your configured sensor.

For more information, see [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry).

### Test sensor data

After you configure your sensor, navigate to the [Control tab](/fleet/machines/#control) and select the **Sensors** dropdown panel.
To access detailed readings from your sensor, click on the **Get Readings** button.

{{<gif webm_src="/data/monitor.webm" mp4_src="/data/monitor.mp4" alt="sensor control tab">}}

## Configure data manager to capture and sync sensor data

To capture the data from your configured sensor, you need to add the [data management service](https://docs.viam.com/data/) and configure it to capture and sync the sensor data:

1. On your machine's **Config** page, go to the **Services** subtab and click **Create service**.
2. Select the **data management** service and give it a name.
   For example `data_manager`.
3. Click **Create**.
4. Go to the **Components** subtab and find your `telegrafsensor`'s configuration card.
   In the **Data capture configuration** section of the sensor's config, click **Add method**, select the `Readings` **Type** and set the **Frequency** to 0.2Hz.
5. Click **Save config**.

### View data

View your sensor data on the [**Data** tab](https://app.viam.com/data/view?view=sensors).

![View of sensor data](/data/sensor-data.png)

### Next steps

The data you obtain about your machines is associated with metadata about the machine and time of capture.
Once you have captured data about your machines, you can query your captured data with any tools that with SQL or MQL or visualize your data with tools like Grafana:

{{< cards >}}
{{% card link="/data/query/" %}}
{{% card link="/data/visualize" %}}
{{< /cards >}}
