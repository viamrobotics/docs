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

You can receive alerts for the following events involving machine performance telemetry:

- [**Machine telemetry data that meets certain conditions**](#data-meets-condition): receive an email or webhook any time data is captured that meets a certain condition
- [**Machine telemetry data has been synced to the cloud**](#data-synced): receive an email or webhook when data from the machine is synced
- [**Part is online**](#part-is-online): receive an email or webhook continuously at a specified interval while the {{< glossary_tooltip term_id="part" text="machine part" >}} is online
- [**Part is offline**](#part-is-offline): receive an email or webhook continuously at a specified interval while the machine part is offline

For example, you can configure a trigger to send you a notification when your machine's CPU usage reaches a certain threshold.

{{< alert title="Tip" color="tip" >}}
You can also configure alerts on any other machine data, for more information on that, see [Alert on data](/data-ai/data/advanced/alert-data/).
{{< /alert >}}

## Data meets condition

The following steps let you configure [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) sensors to monitor different metrics about a machine, such as:

- `memory_monitor`: Memory stats for the SBC.
- `cpu_monitor`: Reports per-core and overall usage percentages.
- `temperature`: Reports the temperature of various temperature sensors.

{{% expand "On macOS use telegraf instead. Click to see more info." %}}

[`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) is not supported on macOS.
You can use the [`telegraf`](https://app.viam.com/module/viam/viam-telegraf-sensor) sensor instead.

You must also install telegraf by running `brew install telegraf` in your terminal before using this module.

{{% /expand%}}

### Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

### Add performance sensor

{{< table >}}
{{% tablestep number=1 %}}
**Add the performance metrics sensors**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Component**.

Search for and add the `hwmonitor:cpu_monitor` model provided by the [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor).

{{% /tablestep %}}

<!-- markdownlint-disable-file MD034 -->

{{% tablestep number=2 %}}
**(Optional) Customize the sensor configuration**

Add additional sensors for any other metrics you want to track.
You can find a list of the sensors the [`sbc-hwmonitor`](https://app.viam.com/module/rinzlerlabs/sbc-hwmonitor) module page.

{{% /tablestep %}}
{{% tablestep  number=3 %}}
**Test the sensor**

**Save the configuration.**

Now, click **Test** at the bottom of the sensor configuration card to view the readings.
You can also see readings on the **CONTROL** tab.

{{<imgproc src="/how-tos/telegraf-test.png" resize="1000x" style="width:600px" class="shadow imgzoom" declaredimensions=true alt="Test panel with readings displayed.">}}

{{% /tablestep %}}
{{< /table >}}

### Configure data management

To capture or alert on the data from your configured sensor, you must add the [data management service](/data-ai/capture-data/capture-sync/) and configure it to capture and sync the sensor data:

{{< table >}}
{{% tablestep number=1 %}}
**1. Add the data management service**

On your machine's **CONFIGURE** page, click the **+** icon next to your machine part in the left-hand menu and select **Service**.

Select the `data management / RDK` service and click **Create**.
You can leave the default data sync interval of `0.1` minutes to sync every 6 seconds.
Also leave both **Capturing** and **Syncing** toggles in the "on" position.

{{% /tablestep %}}
{{% tablestep number=2 %}}
**Configure data capture on the sensor**

Return to your sensor's configuration card.

In the **Data capture** section, click **Add method**.

From the **Method** dropdown select `Readings`.
Set the **Frequency** to `0.05` Hz to capture readings once every 20 seconds.

{{<imgproc src="/how-tos/capture-readings.png" resize="1000x" style="width:600px" class="shadow imgzoom" declaredimensions=true alt="Sensor readings capture configuration.">}}

**Save your config.**
{{% /tablestep %}}
{{< /table >}}

{{% expand "Click for instructions to view synced data" %}}

Click the **...** menu in the upper-right corner of the sensor configuration card.
Select **View captured data**.
If you do not immediately see data, wait a minute for the data to be captured and synced at the intervals you specified, then refresh the page.

![View of sensor data](/services/data/sensor-data.png)

{{% /expand%}}

### Configure conditional trigger

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow">}}

2. Name the trigger and click **Create**.

3. Select **Conditional data ingestion** as the trigger **Type**.

   Then select the component you want to capture data from and the method you want to capture data from.
   Next, add any conditions.

   These can include a key, a value, and a logical operator.
   For example, a trigger configured to fire when data is captured from the sensor `cpu-monitor`'s `Readings` method when `cpu` is greater than `50`:

   {{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x400" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." class="shadow">}}

   For more information, see [Conditions](#conditions).

4. Add **Webhooks** or **Emails** and configure the time between notifications.
   For more information on webhooks, see [Webhooks](#webhooks).

{{% /tab %}}
{{% tab name="JSON mode" %}}

To configure your trigger by using **JSON** mode instead of **Builder** mode, paste one of the following JSON templates into your JSON config.
`"triggers"` is a top-level section, similar to `"components"` or `"services"`.

{{< tabs >}}
{{% tab name="JSON Template: Conditional Data Ingestion" %}}

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
          "type": "email",
          "value": "<fill-in-email-here>",
          "seconds_between_notifications": <number of seconds>
        }
      ]
    }
]

```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "my_temp_sensor",
      "model": "bme280",
      "api": "rdk:component:sensor",
      "attributes": {},
      "depends_on": [],
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "additional_params": {},
                "capture_frequency_hz": 0.017
              }
            ]
          }
        }
      ]
    }
  ],
  "triggers": [
    {
      "name": "trigger-1",
      "event": {
        "type": "conditional_data_ingested",
        "conditional": {
          "data_capture_method": "sensor:my_temp_sensor:Readings",
          "condition": {
            "evals": [
              {
                "operator": "gt",
                "value": {
                  "co2": 1000
                }
              }
            ]
          }
        }
      },
      "notifications": [
        {
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": 10
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for triggers:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the trigger |
| `event` |  object | **Required** | The trigger event object: <ul><li>`type`: `conditional_data_ingested`.</li><li>`conditional`: Condition object. See [Conditions](#conditions) for more information. </li></ul> |
| `notifications` |  object | **Required** | The notifications object: <ul><li>`type`: The type of the notification. Options: `webhook`, `email`</li><li>`value`: The URL to send the request to or the email address to notify.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> |

### Conditions

The `conditions` object for the `conditional_data_ingested` trigger includes the following options:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `data_capture_method` | string | **Required** | The method of data capture to trigger on. <br> Example: `sensor:<name-of-component>:Readings`. |
| `conditions` | object | Optional | Conditions that, when true, fire the trigger. Evaluated each time data syncs from the linked component. When this object is empty or not present, the trigger fires each time data syncs from the linked component. <br> Options: <ul><li>`evals`:<ul><li>`operator`: Logical operator for the condition. </li><li>`value`: An object containing a single field and value. The field specifies the path, in the synced data, to the left operand of the conditional. For nested fields, use periods as separators or define the nested structure in JSON. The value specifies an object, string, boolean, regular expression, or integer used as a right operand in the conditional. </li></ul></li></ul> |

Options for `operator`:

| Name    | Description                |
| ------- | -------------------------- |
| `lt`    | less than                  |
| `gt`    | greater than               |
| `lte`   | less than or equal to      |
| `gte`   | greater than or equal to   |
| `eq`    | equal to                   |
| `neq`   | not equal to               |
| `regex` | matches regular expression |

#### Examples

The following condition defines a trigger that fires based on the value of the `cpu` field of synced data:

```json {class="line-numbers linkable-line-numbers"}
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
```

The following sensor reading fires the trigger, since `80 > 50` is `true`:

```json {class="line-numbers linkable-line-numbers"}
{
  "readings": {
    "cpu": 80
  }
}
```

##### Nested Data

The following condition defines a trigger that fires based on a value nested in the `coordinate.latitude` field of synced data:

```json {class="line-numbers linkable-line-numbers"}
"conditions": {
  "evals": [
    {
      "operator": "lt",
      "value": {
        "coordinate": {
          "latitude": 50
        }
      }
    }
  ]
}
```

The following sensor reading fires the trigger, since `40 < 50` is `true`:

```json {class="line-numbers linkable-line-numbers"}
{
  "readings": {
    "coordinate": {
      "latitude": 40
    }
  }
}
```

### Stop data capture

If this is a test project, make sure you stop data capture to avoid charges for a large amount of unwanted data.

In the **Data capture** section of your sensor's configuration, toggle the switch to **Off**.

Click the **Save** button in the top right corner of the page to save your config.

## Data synced

You must [configure data capture](/data-ai/capture-data/capture-sync/) for your machine to use this trigger.

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow">}}

2. Name the trigger and click **Create**.

3. Select **Data synced to cloud** as the **Type**.

   Then, select the data types for which the Trigger should send requests.
   Whenever data of the specified data types is ingested, a `POST` request will be sent.

4. Add **Webhooks** or **Emails** and configure the time between notifications.
   For more information on webhooks, see [Webhooks](#webhooks).

{{% /tab %}}
{{% tab name="JSON mode" %}}

To configure your trigger by using **JSON** mode instead of **Builder** mode, paste one of the following JSON templates into your JSON config.
`"triggers"` is a top-level section, similar to `"components"` or `"services"`.

{{< tabs >}}
{{% tab name="JSON Template: Data Synced" %}}

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
    {
      "name": "<trigger name>",
      "event": {
        "type": "part_data_ingested",
        "data_ingested": {
          "data_types": ["binary", "tabular", "file"]
        }
      },
      "notifications": [
        {
          "type": "webhook",
          "value": "https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws",
          "seconds_between_notifications": <number of seconds>
        }
      ]
    }
  ]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "cpu-monitor",
      "api": "rdk:component:sensor",
      "model": "rinzlerlabs:hwmonitor:cpu_monitor",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.05,
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
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
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": 10
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for triggers:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the trigger |
| `event` |  object | **Required** | The trigger event object: <ul><li>`type`: `part_data_ingested`.</li><li>`data_types`: The data types that trigger the event. Options: `binary`, `tabular`, `file`, `unspecified`. </li></ul> |
| `notifications` |  object | **Required** | The notifications object: <ul><li>`type`: The type of the notification. Options: `webhook`, `email`</li><li>`value`: The URL to send the request to or the email address to notify.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> |

## Part is online

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow">}}

2. Name the trigger and click **Create**.

3. Select **Part is online** as the trigger **Type**.

4. Add **Webhooks** or **Emails** and configure the time between notifications.
   For more information on webhooks, see [Webhooks](#webhooks).

{{% /tab %}}
{{% tab name="JSON mode" %}}

To configure your trigger by using **JSON** mode instead of **Builder** mode, paste one of the following JSON templates into your JSON config.
`"triggers"` is a top-level section, similar to `"components"` or `"services"`.

{{< tabs >}}
{{% tab name="JSON Template: Part Online" %}}

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
    {
      "name": "<trigger name>",
      "event": {
        "type": "part_online"
      },
      "notifications": [
        {
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": <number of seconds>
        }
      ]
    }
  ]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "cpu-monitor",
      "api": "rdk:component:sensor",
      "model": "rinzlerlabs:hwmonitor:cpu_monitor",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.05,
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
  "triggers": [
    {
      "name": "trigger-1",
      "event": {
        "type": "part_online"
      },
      "notifications": [
        {
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": 10
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for triggers:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the trigger |
| `event` |  object | **Required** | The trigger event object: <ul><li>`type`: `part_online`.</li></ul> |
| `notifications` |  object | **Required** | The notifications object: <ul><li>`type`: The type of the notification. Options: `webhook`, `email`</li><li>`value`: The URL to send the request to or the email address to notify.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> |

## Part is offline

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow">}}

2. Name the trigger and click **Create**.

3. Select **Part is offline** as the trigger **Type**.

4. Add **Webhooks** or **Emails** and configure the time between notifications.
   For more information on webhooks, see [Webhooks](#webhooks).

{{% /tab %}}
{{% tab name="JSON mode" %}}

To configure your trigger by using **JSON** mode instead of **Builder** mode, paste one of the following JSON templates into your JSON config.
`"triggers"` is a top-level section, similar to `"components"` or `"services"`.

{{< tabs >}}
{{% tab name="JSON Template: Part Offline" %}}

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
    {
      "name": "<trigger name>",
      "event": {
        "type": "part_offline"
      },
       "notifications": [
        {
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": <number of seconds>
        }
       ]
    }
  ]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "cpu-monitor",
      "api": "rdk:component:sensor",
      "model": "rinzlerlabs:hwmonitor:cpu_monitor",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.05,
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
  "triggers": [
    {
      "name": "trigger-1",
      "event": {
        "type": "part_offline"
      },
      "notifications": [
        {
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": 10
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for triggers:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the trigger |
| `event` |  object | **Required** | The trigger event object: <ul><li>`type`: `part_offline`.</li></ul> |
| `notifications` |  object | **Required** | The notifications object: <ul><li>`type`: The type of the notification. Options: `webhook`, `email`</li><li>`value`: The URL to send the request to or the email address to notify.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> |

## Webhooks

### Example cloud function

If you are using a cloud function or lambda to process the request from `viam-server`, you can use this template.

The following example function prints the received headers:

{{< tabs >}}
{{% tab name="Flask" %}}

```python {class="line-numbers linkable-line-numbers" }
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def trigger():
    headers = request.headers
    data = {}
    if request.data:
        data = request.json
    payload = {
        "Org-Id": headers.get('org-id', 'no value'),
        "Organization-Name": headers.get('organization-name', '') or
        data.get('org_name', 'no value'),
        "Location-Id": headers.get('location-id', 'no value'),
        "Location-Name": headers.get('location-name', '') or
        data.get('location_name', 'no value'),
        "Part-Id": headers.get('part-id', 'no value'),
        "Part-Name": headers.get('part-name', 'no value'),
        "Robot-Id": headers.get('robot-id', 'no value'),
        "Machine-Name": headers.get('machine-name', '') or
        data.get('machine_name', 'no value'),
        "Component-Type": data.get('component_type', 'no value'),
        "Component-Name": data.get('component_name', 'no value'),
        "Method-Name": data.get('method_name', 'no value'),
        "Min-Time-Received": data.get('min_time_received', 'no value'),
        "Max-Time-Received": data.get('max_time_received', 'no value'),
        "Data-Type": data.get('data_type', 'no value'),
        "File-Id": data.get('file_id', 'no value'),
        "Trigger-Condition": data.get("trigger_condition", 'no value'),
        "Data": data.get('data', 'no value')
    }
    print(payload)

    return payload


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

{{% /tab %}}
{{% tab name="functions_framework" %}}

```python {class="line-numbers linkable-line-numbers"}
import functions_framework
import requests
import time


@functions_framework.http
def hello_http(request):
    headers = request.headers
    data = {}
    if request.data:
        data = request.json
    payload = {
        "Org-Id": headers.get("org-id", "no value"),
        "Organization-Name": headers.get("organization-name", "")
        or data.get("org_name", "no value"),
        "Location-Id": headers.get("location-id", "no value"),
        "Location-Name": headers.get("location-name", "")
        or data.get("location_name", "no value"),
        "Part-Id": headers.get("part-id", "no value"),
        "Part-Name": headers.get("part-name", "no value"),
        "Robot-Id": headers.get("robot-id", "no value"),
        "Machine-Name": headers.get("machine-name", "")
        or data.get("machine_name", "no value"),
        "Component-Type": data.get("component_type", "no value"),
        "Component-Name": data.get("component_name", "no value"),
        "Method-Name": data.get("method_name", "no value"),
        "Min-Time-Received": data.get("min_time_received", "no value"),
        "Max-Time-Received": data.get("max_time_received", "no value"),
        "Data-Type": data.get("data_type", "no value"),
        "File-Id": data.get('file_id', "no value"),
        "Trigger-Condition": data.get("trigger_condition", "no value"),
        "Data": data.get('data', "no value")
    }
    print(payload)

    return 'Received headers: {}'.format(payload)
```

{{% /tab %}}
{{< /tabs >}}

### Returned headers

When an event occurs, Viam sends a HTTP request to the URL you specified for the trigger:

<!-- prettier-ignore -->
| Trigger type | HTTP Method |
| ------------ | ----------- |
| `part_data_ingested` | POST |
| `conditional_data_ingested` | POST |
| `part_online` | GET |
| `part_offline` | GET |

The request includes the following headers:

<!-- prettier-ignore -->
| Header Key | Description | Trigger types |
| ---------- | ----------- | ------------- |
| `org-Id` | The ID of the organization that triggered the request. | all |
| `organization-Name` | The name of the organization that triggered the request. | `part_online`, `part_offline` |
| `location-Id` | The location of the machine that triggered the request. | all |
| `location-lame` | The location of the machine that triggered the request. | `part_online`, `part_offline` |
| `part-id` |  The part of the machine that triggered the request. | all |
| `machine-name` | The name of the machine that triggered the request. | `part_online`, `part_offline` |
| `robot-id` | The ID of the machine that triggered the request. | all |

### Returned data

The request body includes the following data:

<!-- prettier-ignore -->
| Data Key | Description | Trigger types |
| -------- | ----------- | ------------- |
| `component_name` | The name of the component for which data was ingested. | `part_data_ingested`, `conditional_data_ingested` |
| `component_type` | The type of component for which data was ingested. | `part_data_ingested`, `conditional_data_ingested` |
| `method_name` | The name of the method from which data was ingested. | `part_data_ingested`, `conditional_data_ingested` |
| `min_time_received` | Indicates the earliest time a piece of data was received. | `part_data_ingested` |
| `max_time_received` | Indicates the latest time a piece of data was received. | `part_data_ingested` |
| `method_name` | The name of the method that triggered the request. | `conditional_data_ingested` |
| `machine_name` | The name of the machine that triggered the request. | `part_data_ingested`, `conditional_data_ingested` |
| `location_name` | The location of the machine that triggered the request. | `part_data_ingested`, `conditional_data_ingested` |
| `org_name` | The name of the organization that triggered the request. | `part_data_ingested`, `conditional_data_ingested` |
| `file_id` | The id of the file that was ingested. | `part_data_ingested` |
| `trigger_condition` | The condition that triggered the request. | `conditional_data_ingested` |
| `data` | The ingested sensor data. Includes `metadata` with `received_at` and `requested_at` timestamps and `data` in the form `map[string]any`. | `part_data_ingested`, `conditional_data_ingested` (sensor data) |

## Example project

To see an example project that uses triggers to send email notification, see the [Monitor Job Site Helmet Usage with Computer Vision tutorial](/tutorials/projects/helmet/#configure-a-trigger-on-your-machine).

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
