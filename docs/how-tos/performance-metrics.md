---
title: "Monitor machine performance metrics"
linkTitle: "Monitor Performance"
description: "Capture and sync data about your machines' performance."
weight: 100
type: "docs"
tags: ["data management", "cloud", "sync"]
images: ["/services/data/monitor.gif"]
videos: ["/services/data/monitor.webm", "/services/data/monitor.mp4"]
aliases:
  - "/data/capture/performance-metrics/"
  - "/services/data/capture/performance-metrics/"
languages: []
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "registry"]
level: "Beginner"
date: "2024-08-23"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

You can use the [`viam-telegraf-sensor`](https://app.viam.com/module/viam/viam-telegraf-sensor) {{< glossary_tooltip term_id="module" text="module" >}} to capture and monitor the following metrics about the performance of individual machines or your entire fleet:

- **Wireless Signal Strength and Quality**: Signal level, link quality, and noise level
- **Memory Usage**: Memory statistics, including total available memory, used percentage, and specifics on various types of memory (cached, free, slab, etc.)
- **CPU Usage**: CPU usage across different states (user, system, idle, etc.)
- **Disk I/O**: Metrics on read and write operations, including bytes transferred and operation times
- **Network Traffic**: Detailed network statistics, including bytes sent and received, packet information, and error counts, providing a deep dive into a device's network performance

{{% alert title="In this page" color="tip" %}}

- [Configure the `viam-telegraf-sensor`](#add-the-telegraf-sensor)
- [Configure the data management service to capture and sync data from the telegraf sensor](#configure-the-data-management-service)
- [View the synced data](#view-synced-data)

{{% /alert %}}

## Prerequisites

{{% expand "Install telegraf. Click to see instructions." %}}

On macOS, you must also install telegraf by running `brew install telegraf` in your terminal before using this module.

If you are on another operating system, telegraf will be installed automatically for you.

{{% /expand%}}

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{< alert title="Note" color="note" >}}
You must run `viam-server` with `sudo` to monitor machine performance metrics.
{{< /alert >}}

## Add the telegraf-sensor

{{< table >}}
{{% tablestep link="/registry/configure/#add-a-modular-resource-from-the-viam-registry" %}}
**1. Add the performance metrics sensor**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Component**.

Search for and add the `viam:viam-sensor:telegrafsensor` model provided by the [`viam-telegraf-sensor` module](https://app.viam.com/module/viam/viam-telegraf-sensor).

{{% /tablestep %}}

<!-- markdownlint-disable-file MD034 -->

{{% tablestep link="https://github.com/viamrobotics/viam-telegraf-sensor" %}}
**2. (Optional) Customize the sensor configuration**

To enable or disable specific metrics, add them to the attributes configuration.
You can find a list of configurable attributes in the [module README](https://github.com/viamrobotics/viam-telegraf-sensor).
For example:

```json
{
  "disable_kernel": true
}
```

{{% /tablestep %}}
{{% tablestep  %}}
**3. Test the sensor**

**Save the configuration.**

Now, click **Test** at the bottom of the sensor configuration card to view the readings.
You can also see readings on the **CONTROL** tab.

![Test panel with readings displayed.](/how-tos/telegraf-test.png)

{{% /tablestep %}}
{{< /table >}}

## Configure the data management service

To capture the data from your configured sensor, you need to add the [data management service](/services/data/) and configure it to capture and sync the sensor data:

{{< table >}}
{{% tablestep link="/services/data/" %}}
**1. Add the data management service**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.
Also leave both **Capturing** and **Syncing** toggles in the "on" position.

{{% /tablestep %}}
{{% tablestep %}}
**2. Configure data capture on the telegraf sensor**

Return to your `telegrafsensor`'s configuration card.

In the **Data capture** section, click **Add method**.

From the **Method** dropdown select `Readings`.
Set the **Frequency** to `0.05` Hz to capture readings once every 20 seconds.

![Sensor readings capture configuration.](/how-tos/capture-readings.png)

Save your config.
{{% /tablestep %}}
{{< /table >}}

## View synced data

Click the **...** menu in the upper-right corner of the sensor configuration card.
Select **View captured data**.
If you do not immediately see data, wait a minute for the data to be captured and synced at the intervals you specified, then refresh the page.

![View of sensor data](/services/data/sensor-data.png)

## Stop data capture

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your sensor's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## Next steps

The data you obtain about your machines is associated with metadata about the machine and time of capture.
Once you have captured data about your machines, you can query your captured data with any tools that with SQL or MQL or visualize your data with tools like Grafana:

{{< cards >}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{% card link="/how-tos/sensor-data-visualize/" %}}
{{< /cards >}}
