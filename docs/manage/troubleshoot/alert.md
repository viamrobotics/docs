---
linkTitle: "Alert on machine telemetry"
title: "Alert on machine telemetry"
weight: 20
layout: "docs"
type: "docs"
description: "Receive alerts for events involving machine performance telemetry."
tags: ["triggers"]
images: ["/services/data/monitor.gif"]
videos: ["/services/data/monitor.webm", "/services/data/monitor.mp4"]
languages: []
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "registry"]
aliases:
  - /build/configure/webhooks/
  - /build/configure/triggers/
  - "/data/capture/performance-metrics/"
  - "/services/data/capture/performance-metrics/"
  - /configure/triggers/
  - /how-tos/performance-metrics/
date: "2024-12-07"
next: "/manage/troubleshoot/teleoperate/custom-interface/"
# updated: ""  # When the content was last entirely checked
cost: "0"
---

You can configure triggers that alert you when machine telemetry data syncs from your local device to the Viam cloud:

- **Telemetry sync**: Alerts whenever certain telemetry syncs
- **Conditional telemetry sync**: Alert only when synced telemetry satisfies a condition

For example, you can configure a trigger to send you a notification when your machine's CPU usage reaches a certain threshold.

Additionally, you can receive continuous alerts at a specified interval indicating one of the following machine statuses:

- **Part is online**: alert while the {{< glossary_tooltip term_id="part" text="machine part" >}} is online
- **Part is offline**: alert while the machine part is offline

### Prerequisites

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "On macOS, an installation of Telegraf." %}}

To install [`telegraf`](https://github.com/influxdata/telegraf), run the following command:

```sh {class="command-line" data-prompt="$"}
brew install telegraf
```

{{% /expand %}}

## Alert on telemetry sync

{{< tabs >}}
{{% tab name="Linux" %}}

The following steps show you how to configure [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) sensors to monitor different metrics about a machine, such as:

- `memory_monitor`: Memory stats for the SBC.
- `cpu_monitor`: Reports per-core and overall usage percentages.
- `temperature`: Reports the temperature of various temperature sensors.

{{% /tab %}}
{{% tab name="macOS" %}}

The following steps show you how to configure [`telegraf`](https://app.viam.com/module/viam/viam-telegraf-sensor) sensors to monitor different metrics about a machine, such as:

- `mem`: Memory stats for the SBC.
- `cpu`: Reports per-core and overall usage percentages.

{{% /tab %}}
{{< /tabs >}}

### Add performance sensor

{{< tabs >}}
{{% tab name="Linux" %}}

{{< table >}}
{{% tablestep start=1 %}}
**Add the performance metrics sensors**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.

Search for and add the `hwmonitor:cpu_monitor` model provided by the [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor).

{{% /tablestep %}}

<!-- markdownlint-disable-file MD034 -->

{{% tablestep %}}
**(Optional) Customize the sensor configuration**

Add additional sensors for any other metrics you want to track.
You can find a list of sensors on the [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) module page.

{{% /tablestep %}}
{{% tablestep  number=3 %}}
**Test the sensor**

Click **Save** to put your configuration changes into effect.

Now, click **Test** at the bottom of the sensor configuration card to view the readings.
You can also see readings on the **CONTROL** tab.

{{<imgproc src="/how-tos/telegraf-test.png" resize="1000x" style="width:600px" class="shadow imgzoom" declaredimensions=true alt="Test panel with readings displayed.">}}

{{% /tablestep %}}
{{< /table >}}
{{% /tab %}}
{{% tab name="macOS" %}}
{{< table >}}
{{% tablestep start=1 %}}
**Add the performance metrics sensors**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Component**.

Search for and add the [`viam-sensor:telegrafsensor` model](https://github.com/viam-modules/viam-telegraf-sensor).

{{% /tablestep %}}

<!-- markdownlint-disable-file MD034 -->

{{% tablestep %}}
**(Optional) Customize the sensor configuration**

Add additional sensors for any other metrics you want to track.
You can find a list of sensors on the [`viam-telegraf-sensor`](https://app.viam.com/module/viam/viam-telegraf-sensor) module page.

{{% /tablestep %}}
{{% tablestep  number=3 %}}
**Test the sensor**

Click **Save** to apply your configuration changes.

Now, click **Test** at the bottom of the sensor configuration card to view the readings.
You can also see readings on the **CONTROL** tab.

{{<imgproc src="/how-tos/telegraf-test.png" resize="1000x" style="width:600px" class="shadow imgzoom" declaredimensions=true alt="Test panel with readings displayed.">}}

{{% /tablestep %}}
{{< /table >}}
{{% /tab %}}
{{< /tabs >}}

### Configure data management

To capture or alert on the data from your configured sensor, you must add the [data management service](/data-ai/capture-data/capture-sync/) and configure it to capture and sync the sensor data:

{{< table >}}
{{% tablestep start=1 %}}
**Add the data management service**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.
Also leave both **Capturing** and **Syncing** toggles in the "on" position.

{{% /tablestep %}}
{{% tablestep %}}
**Configure data capture on the sensor**

Return to your sensor's configuration card.

In the **Data capture** section, click **Add method**.

From the **Method** dropdown select `Readings`.
Set the **Frequency** to `0.05` Hz to capture readings once every 20 seconds.

{{<imgproc src="/how-tos/capture-readings.png" resize="1000x" style="width:600px" class="shadow imgzoom" declaredimensions=true alt="Sensor readings capture configuration.">}}

Click the **Save** button to apply your configuration changes.
{{% /tablestep %}}
{{% tablestep %}}
**View synced data**

Click the **...** menu in the upper-right corner of the sensor configuration card.
Select **View captured data**.
If you do not immediately see data, wait a minute for the data to be captured and synced at the intervals you specified, then refresh the page.

![View of sensor data](/services/data/sensor-data.png)

{{% /tablestep %}}
{{< /table >}}

### Configure trigger

{{< tabs >}}
{{% tab name="Builder mode" %}}

Use **Builder mode** to create a trigger:

{{< table >}}
{{< tablestep >}}

Go to the **CONFIGURE** tab of your machine.
Click the **+** (Create) button in the left side menu and select **Trigger**.

{{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options.">}}

{{< /tablestep >}}
{{< tablestep >}}
**Create the trigger**

Enter a name and click **Create**.

{{< /tablestep >}}
{{< tablestep >}}
**Configure type**

In the **Type** dropdown, choose one of the following types:

- **Data has been synced to the cloud**:
  Whenever your machine syncs data of any of the specified data types, the trigger sends an alert.

  To use this trigger type, select the data types for which the trigger should send requests.

- **Conditional data ingestion**:
  Whenever your machine syncs data that meets certain criteria, the trigger sends an alert.

  To use this trigger type:

  1. Choose the target component and method for your condition.
  1. Add a **condition**: specify a **key** in the synced data, an **operator**, and a **value**.
     When data from the target component and method syncs from your machine, the trigger uses the key as a path to look up a value in the synced data object.
     The trigger applies the operator to the extracted value and the value you specified in your condition.

     For example, the following trigger sends an alert when the `cpu-monitor` component's `Readings` method syncs `cpu` usage greater than `50`:

     {{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x400" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." class="shadow" >}}

     For more information, see [Conditional attributes](/data-ai/reference/triggers-configuration/#conditional-attributes).

{{< /tablestep >}}
{{< tablestep >}}
**Configure alert frequency**

To add a notification method, add an entry to the **Webhooks** or **Email** sub-panels:

To add an email notification:

1.  Click **Add Email**.
    {{<imgproc src="/build/configure/trigger-configured-email.png" resize="x400" style="width: 500px" declaredimensions=true alt="The trigger configured with an example email." class="shadow" >}}
1.  Add the email you wish to be notified whenever this trigger is triggered.
1.  Configure the time between notifications.

To add a webhook notification:

1.  Click **Add Webhook**.
    {{<imgproc src="/build/configure/trigger-configured.png" resize="x400" style="width: 500px" declaredimensions=true alt="The trigger configured with an example URL." class="shadow" >}}
1.  Add the URL of your cloud function.
1.  Configure the time between notifications.
1.  Write your cloud function to process the [webhook](/data-ai/reference/triggers-configuration/#webhook-attributes).
    Use your cloud function to process data or interact with any external API, including Twilio, PagerDuty, or Zapier.

{{< /tablestep >}}
{{< /table >}}

{{% /tab %}}
{{% tab name="JSON mode" %}}

Use the following template in your `components` JSON to configure the top-level `triggers` field:

{{< tabs >}}
{{% tab name="Telemetry sync" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "trigger-1",
    "event": {
      "type": "part_data_ingested",
      "data_ingested": {
        "data_types": ["binary", "tabular", "file", "unspecified"]
      }
    },
    "notifications": [
      {
        "type": "<webhook|email>",
        "value": "<webhook URL or email address>",
        "seconds_between_notifications": <int>
      }
    ]
  }
]
```

{{% /tab %}}
{{% tab name="Conditional telemetry sync" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "<trigger name>",
    "event": {
      "type": "conditional_data_ingested",
      "conditional": {
        "data_capture_method": "<component>:<name-of-component>:<method>",
        "conditions": {
          "evals": [
            {
              "operator": "<lt|gt|lte|gte|eq|neq|regex>",
              "value": <object, string, bool, regex, or int>
            }
          ]
        }
      }
    },
    "notifications": [
      {
        "type": "<webhook|email>",
        "value": "<webhook URL or email address>",
        "seconds_between_notifications": <number of seconds>
      }
    ]
  }
]
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

For more information about triggers, see [Trigger configuration](/data-ai/reference/triggers-configuration/).

### Stop data capture

If this is a test project, make sure you stop data capture to avoid charges for syncing unwanted data.

In the **Data capture** section of your sensor's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your configuration.

## Alert on machine status

### Part is online

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow">}}

2. Name the trigger and click **Create**.

3. Select **Part is online** as the trigger **Type**.

4. To add a notification method, add an entry to the **Webhooks** or **Email** sub-panels:

   To add an email notification:

   1. Click **Add Email**.
      {{<imgproc src="/build/configure/trigger-configured-email.png" resize="x400" style="width: 500px" declaredimensions=true alt="The trigger configured with an example email." class="shadow" >}}
   1. Add the email you wish to be notified whenever this trigger is triggered.
   1. Configure the time between notifications.

   To add a webhook notification:

   1. Click **Add Webhook**.
      {{<imgproc src="/build/configure/trigger-configured.png" resize="x400" style="width: 500px" declaredimensions=true alt="The trigger configured with an example URL." class="shadow" >}}
   1. Add the URL of your cloud function.
   1. Configure the time between notifications.
   1. Write your cloud function to process the [webhook attributes](/data-ai/reference/triggers-configuration/#webhook-attributes).
      Use your cloud function to process data or interact with any external API, including Twilio, PagerDuty, or Zapier.

{{% /tab %}}
{{% tab name="JSON mode" %}}

Use the following template in your `components` JSON to configure the top-level `triggers` field:

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "<trigger name>",
    "event": {
      "type": "part_online"
    },
    "notifications": [
      {
        "type": "<webhook|email>",
        "value": "<webhook URL or email address>",
        "seconds_between_notifications": <number of seconds>
      }
    ]
  }
]
```

{{% /tab %}}
{{< /tabs >}}

For more information about triggers, see [Trigger configuration](/data-ai/reference/triggers-configuration/).

### Part is offline

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow">}}

2. Name the trigger and click **Create**.

3. Select **Part is offline** as the trigger **Type**.

4. Add **Webhooks** or **Emails** and configure the time between notifications.
   For more information on webhooks, see [Webhook attributes](/data-ai/reference/triggers-configuration/#webhook-attributes).

{{% /tab %}}
{{% tab name="JSON mode" %}}

Use the following template in your `components` JSON to configure the top-level `triggers` field:

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "<trigger name>",
    "event": {
      "type": "part_offline"
    },
     "notifications": [
      {
        "type": "webhook|email",
        "value": "<webhook URL or email address>",
        "seconds_between_notifications": <number of seconds>
      }
     ]
  }
]
```

{{% /tab %}}
{{< /tabs >}}

For more information about triggers, see [Trigger configuration](/data-ai/reference/triggers-configuration/).
