---
title: "Performance Monitoring Data Capture"
linkTitle: "Monitor Performance"
description: "Capture and sync data about your machines' performance."
weight: 12
type: "docs"
tags: ["data management", "cloud", "sync"]
icon: true
images: ["/services/data/monitor.gif"]
videos: ["/services/data/monitor.webm", "/services/data/monitor.mp4"]
aliases:
  - "/services/data/capture/"
  - "/data/capture/performance-metrics/"
no_service: true
# SME: Alexa Greenberg
---

You can capture and monitor the following metrics about the performance of individual machines or your entire fleet:

- **Wireless Signal Strength and Quality**: signal level, link quality, and noise level
- **Memory Usage**: memory statistics, including total available memory, used percentage, and specifics on various types of memory (cached, free, slab, etc.)
- **CPU Utilization**: CPU usage across different states (user, system, idle, etc.)
- **Disk I/O**: metrics on read and write operations, including bytes transferred and operation times
- **Network Traffic**: detailed network statistics, including bytes sent and received, packet information, and error counts, providing a deep dive into a device's network performance

## Requirements

To capture data from a machine, you need to [create a machine in Viam](/cloud/machines/#add-a-new-machine) and follow the setup instructions to install `viam-server` and connect it to the Viam app.

{{< alert title="Note" color="note" >}}
You must run `viam-server` with `sudo` to monitor machine performance metrics.
{{< /alert >}}

## Add sensor to measure performance metrics

To obtain performance metrics about your machine, use the [`viam-telegraf-sensor`](https://app.viam.com/module/viam/viam-telegraf-sensor) module from the [Viam registry](/registry/).
The module provides a [sensor](/components/sensor/) that allows you to obtain readings containing your machine's performance metrics.

1. Go to your machine's **CONFIGURE** page. Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
2. Then select the `viam:viam-sensor:telegrafsensor` model from the [`viam-telegraf-sensor` module](https://app.viam.com/module/viam/viam-telegraf-sensor).
3. Click **Add module**, then enter a name for your sensor, for example `my-telegrafsensor`, and click **Create**.
4. To enable or disable specific metrics, add them to the attributes configuration.
   For example:

   ```json
   {
     "disable_kernel": true
   }
   ```

   See [the `telegrafsensor` module documentation](https://github.com/viamrobotics/viam-telegraf-sensor?tab=readme-ov-file#attributes) for the full list of attributes available.

5. Save the configuration.

For more information, see [add a module from the Viam Registry](/registry/configure/#add-a-modular-resource-from-the-viam-registry).

In the next step you will configure the data management service to capture and sync the performance metrics from your configured sensor.

### Test sensor data

After you configure your sensor, navigate to the [**CONTROL** tab](/fleet/control/) and select the **Sensors** dropdown panel.
To access detailed readings from your sensor, click on the **Get Readings** button.

{{<gif webm_src="/services/data/monitor.webm" mp4_src="/services/data/monitor.mp4" alt="sensor control tab">}}

## Configure data management service to capture and sync sensor data

To capture the data from your configured sensor, you need to add the [data management service](/services/data/) and configure it to capture and sync the sensor data:

1. On your machine's **CONFIGURE** page, go to the **Services** subtab and click **Create service**.
2. Select the **data management** service and give it a name.
   For example, `data_manager`.
3. Click **Create**.
4. Find your `telegrafsensor`'s configuration card.
   In the **Data capture** section of the sensor's config, click **Add method**, select the `Readings` **Method** type and set the **Frequency** to 0.2Hz.
5. Click **Save**.

### View data

View your sensor data on the [**DATA** tab](https://app.viam.com/data/view?view=sensors).

![View of sensor data](/services/data/sensor-data.png)

### Next steps

The data you obtain about your machines is associated with metadata about the machine and time of capture.
Once you have captured data about your machines, you can query your captured data with any tools that with SQL or MQL or visualize your data with tools like Grafana:

{{< cards >}}
{{% card link="/use-cases/sensor-data-query/" %}}
{{% card link="/use-cases/sensor-data-visualize/" %}}
{{< /cards >}}
