---
linkTitle: "Set up alerts"
title: "Set up alerts"
weight: 20
layout: "docs"
type: "docs"
description: "Configure triggers to receive email or webhook notifications when machines need attention."
aliases:
  - /manage/troubleshoot/alert/
  - /build/configure/webhooks/
  - /build/configure/triggers/
  - /configure/triggers/
  - /how-tos/performance-metrics/
  - /data/capture/performance-metrics/
  - /services/data/capture/performance-metrics/
---

Configure triggers to receive email or webhook notifications when your machines need attention. Triggers fire when specific events occur, such as a sensor reading crossing a threshold, a machine going offline, or error logs appearing.

## Types of alerts

| Trigger type          | Fires when                               | Use case                                                     |
| --------------------- | ---------------------------------------- | ------------------------------------------------------------ |
| Telemetry sync        | Data syncs from a machine to the cloud   | Know when any data arrives                                   |
| Conditional telemetry | Synced data meets a condition you define | CPU above 80%, temperature below freezing, battery under 20% |
| Machine logs          | Error, warning, or info logs appear      | Catch errors without watching the LOGS tab                   |
| Part online           | A machine part comes online              | Know when a machine reconnects after maintenance             |
| Part offline          | A machine part goes offline              | Respond to unexpected disconnections                         |

## Prerequisites

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

## Alert on telemetry

To alert on sensor data, you need three things: a sensor producing data, the data management service capturing and syncing that data, and a trigger that fires when the data arrives or meets a condition.

### Add a performance sensor

To monitor machine health metrics like CPU usage, memory, and temperature, add a performance metrics sensor.

{{< tabs >}}
{{% tab name="Linux" %}}

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part and select **Component or service**.
Search for and add the `hwmonitor:cpu_monitor` model from the [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) module.

You can add additional sensors for memory, temperature, and other metrics.
See the [`sbc-hwmonitor` module page](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) for the full list.

{{% /tab %}}
{{% tab name="macOS" %}}

First install [`telegraf`](https://github.com/influxdata/telegraf):

```sh {class="command-line" data-prompt="$"}
brew install telegraf
```

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part and select **Component**.
Search for and add the [`viam-sensor:telegrafsensor` model](https://github.com/viam-modules/viam-telegraf-sensor).

You can add additional sensors for other metrics.
See the [`viam-telegraf-sensor` module page](https://app.viam.com/module/viam/viam-telegraf-sensor) for the full list.

{{% /tab %}}
{{< /tabs >}}

Click **Save**, then click **Test** at the bottom of the sensor configuration card to verify readings are coming through.

### Configure data capture

1. On your sensor's configuration card, click **+** on the **Data Capture** card.
1. If you see a "Data management service missing" banner, click
   **Create data management service**, click **Save**, navigate back to
   your sensor, and click **+** on the **Data Capture** card again.
1. Select `Readings` from the **Method** dropdown and set the **Frequency** to `0.05` Hz (once every 20 seconds).
1. Click **Save**.

To verify data is syncing, click the **...** menu on the sensor card and select **View captured data**.
Wait a minute for data to capture and sync, then refresh.

### Configure the trigger

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab.
   Click **+** in the left sidebar and select **Trigger**.
1. Enter a name and click **Create**.
1. In the **Type** dropdown, choose:
   - **Data has been synced to the cloud**: fires whenever data of the selected types syncs.
   - **Conditional data ingestion**: fires when synced data meets a condition you define.
     Choose the target component and method, then add a condition with a key, operator, and value.
     For example, to alert when CPU usage exceeds 50%: select your cpu-monitor component, Readings method, key `cpu`, operator `greater than`, value `50`.
1. Add notification methods:
   - **Email specific addresses**: toggle on, add addresses, set alert frequency.
   - **Email all machine owners**: toggle on, set alert frequency.
   - **Webhook**: click **Add Webhook**, enter your cloud function URL, set alert frequency.
     See [Trigger configuration](/reference/triggers/#webhook-attributes) for webhook payload details.
1. Click **Save**.

{{% /tab %}}
{{% tab name="JSON mode" %}}

Add a `triggers` field to your machine configuration:

{{< tabs >}}
{{% tab name="Telemetry sync" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "trigger-1",
    "event": {
      "type": "part_data_ingested",
      "data_ingested": {
        "data_types": ["binary", "tabular", "file"]
      }
    },
    "notifications": [
      {
        "type": "email",
        "value": "you@example.com",
        "seconds_between_notifications": 300
      }
    ]
  }
]
```

{{% /tab %}}
{{% tab name="Conditional telemetry" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "cpu-alert",
    "event": {
      "type": "conditional_data_ingested",
      "conditional": {
        "data_capture_method": "sensor:cpu-monitor:Readings",
        "conditions": {
          "evals": [
            {
              "operator": "gt",
              "value": {
                "cpu": 50
              }
            }
          ]
        }
      }
    },
    "notifications": [
      {
        "type": "email",
        "value": "you@example.com",
        "seconds_between_notifications": 600
      }
    ]
  }
]
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

### Stop data capture

If this is a test, stop data capture to avoid charges for syncing unwanted data.
In the **Data capture** section of your sensor's configuration, toggle the switch to **Off** and click **Save**.

## Alert on machine logs

Configure a trigger that fires when machine logs of a specified level appear.
Viam checks for matching logs once per hour.

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab.
   Click **+** in the left sidebar and select **Trigger**.
1. Enter a name and click **Create**.
1. Select **Conditional logs ingestion** as the trigger **Type**.
1. Select the log levels to alert on: **Error**, **Warn**, or **Info**.
1. Add notification methods (email or webhook) and set the alert frequency.
1. Click **Save**.

{{% /tab %}}
{{% tab name="JSON mode" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "error-log-alert",
    "event": {
      "type": "conditional_logs_ingested",
      "log_levels": ["error", "warn"]
    },
    "notifications": [
      {
        "type": "email",
        "value": "you@example.com"
      }
    ]
  }
]
```

The notification interval for log triggers is always one hour.

{{% /tab %}}
{{< /tabs >}}

## Alert on machine status

### Part online

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab.
   Click **+** in the left sidebar and select **Trigger**.
1. Enter a name and click **Create**.
1. Select **Part is online** as the trigger **Type**.
1. Add notification methods and set the alert frequency.
1. Click **Save**.

{{% /tab %}}
{{% tab name="JSON mode" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "machine-online",
    "event": {
      "type": "part_online"
    },
    "notifications": [
      {
        "type": "email",
        "value": "you@example.com",
        "seconds_between_notifications": 600
      }
    ]
  }
]
```

{{% /tab %}}
{{< /tabs >}}

### Part offline

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab.
   Click **+** in the left sidebar and select **Trigger**.
1. Enter a name and click **Create**.
1. Select **Part is offline** as the trigger **Type**.
1. Add notification methods and set the alert frequency.
1. Click **Save**.

{{% /tab %}}
{{% tab name="JSON mode" %}}

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "machine-offline",
    "event": {
      "type": "part_offline"
    },
    "notifications": [
      {
        "type": "email",
        "value": "you@example.com",
        "seconds_between_notifications": 300
      }
    ]
  }
]
```

{{% /tab %}}
{{< /tabs >}}

Viam uses a 60-second buffer before declaring a part offline.
This prevents false alerts from brief network interruptions.

## Manage alert frequency

Every notification method has a `seconds_between_notifications` setting that controls the minimum time between consecutive alerts.
If a trigger fires more frequently than this interval, Viam suppresses the extra notifications.

Set this value based on how quickly you need to respond:

- **Critical alerts** (machine offline, safety thresholds): 60-300 seconds
- **Operational alerts** (elevated CPU, low battery): 300-600 seconds
- **Informational alerts** (data sync confirmations): 3600 seconds or more

Starting with a longer interval and shortening it as needed is better than starting short and dealing with notification noise.

## Use the CLI

You can also manage triggers from the command line:

```sh {class="command-line" data-prompt="$"}
viam machines part add-trigger --part <part-name-or-id>
```

```sh {class="command-line" data-prompt="$"}
viam machines part delete-trigger --part <part-name-or-id> --name <trigger-name>
```

## Other alert types

- For alerts based on data sync events (not tied to machine health), see [Trigger on data events](/data/trigger-on-data/).
- For alerts when an ML model detects specific objects or classifications, see [Alert on detections](/vision/alert-on-detections/).
- For full trigger configuration reference, see [Trigger configuration](/reference/triggers/).
