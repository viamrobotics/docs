---
linkTitle: "Alert on machine telemetry"
title: "Alert on machine telemetry"
weight: 20
layout: "docs"
type: "docs"
description: "Configure a trigger to trigger actions when data is sent from your machine to the cloud, or when your machine's internet connectivity changes."
tags: ["triggers"]
aliases:
  - /build/configure/webhooks/
  - /build/configure/triggers/
date: "2024-10-17"
# updated: ""  # When the content was last entirely checked
---

{{< alert title="Note" color="note" >}}
TODO: Mke this more about performance metrics.
{{< /alert >}}


You can receive alerts for the following machine events:

- **Data has been synced to the cloud**: receive an email or webhook when data from the machine is synced
- **Part is online**: receive an email or webhook continuously at a specified interval while the {{< glossary_tooltip term_id="part" text="machine part" >}} is online
- **Part is offline**: receive an email or webhook continuously at a specified interval while the machine part is offline
- **Conditional data ingestion**: receive an email or webhook any time data is captured that meets a certain condition

For example, you can configure a trigger to send you a notification when your robot's sensor collects a new reading.

## Data synced

You must [configure data capture](/services/data/) for your machine to use this trigger.

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

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
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "my_temp_sensor",
      "model": "bme280",
      "type": "sensor",
      "namespace": "rdk",
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

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

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
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
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

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

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
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ],
  "triggers": [
    {
      "name": "trigger-1",
      "event": {
        "type": "part_offline",
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

## Data meets condition

You must [configure data capture](/services/data/) for your machine to use this trigger.

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

2. Name the trigger and click **Create**.

3. Select **Conditional data ingestion** as the trigger **Type**.

   Then select the component you want to capture data from and the method you want to capture data from.
   Next, add any conditions.

   These can include a key, a value, and a logical operator.
   For example, a trigger configured to fire when data is captured from the motor `motor-1`'s `IsPowered` method when `is_on` is equal to `True`:

   {{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x400" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." >}}

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
          "condition": {
            "evals": [
              {
                "operator": "<lt|gt|lte|gte|eq|neq>",
                "value": <object, string, or int>
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
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "my_temp_sensor",
      "model": "bme280",
      "type": "sensor",
      "namespace": "rdk",
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

The `conditional` object for the `conditional_data_ingested` trigger includes the following options:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `data_capture_method` | string | **Required** | The method of data capture to trigger on. <br> Example: `sensor:<name-of-component>:Readings`. |
| `condition` | object | Optional | Any additional conditions for the method to fire the trigger. Leave out this object for the trigger to fire any time there is data synced. <br> Options: <ul><li>`evals`:<ul><li>`operator`: Logical operator for the condition. </li><li>`value`: An object, string, or integer that specifies the value of the method of the condition, along with the key or nested keys of the measurements in data capture. </li></ul></li></ul> |

Options for `operator`:

| Name  | Description              |
| ----- | ------------------------ |
| `lt`  | Less than                |
| `gt`  | Greater than             |
| `lte` | Less than or equal to    |
| `gte` | Greater than or equal to |
| `eq`  | Equals                   |
| `neq` | Does not equal           |

Examples:

{{< tabs >}}
{{% tab name="1 level of nesting" %}}

```json {class="line-numbers linkable-line-numbers"}
"condition": {
  "evals": [
    {
      "operator": "lt",
      "value": {
        "Line-Neutral AC RMS Voltage": 130
      }
    }
  ]
}
```

This eval would trigger for the following sensor reading:

```json {class="line-numbers linkable-line-numbers"}
{
  "readings": {
    "Line-Neutral AC RMS Voltage": 100
  }
}
```

{{% /tab %}}
{{% tab name="2 levels of nesting" %}}

```json {class="line-numbers linkable-line-numbers"}
"condition": {
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

This eval would trigger for the following sensor reading:

```json {class="line-numbers linkable-line-numbers"}
{
  "readings": {
    "coordinate": {
      "latitude": 40
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

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
| `Org-Id` | The ID of the organization that triggered the request. | all |
| `Organization-Name` | The name of the organization that triggered the request. | `part_online`, `part_offline` |
| `Location-Id` | The location of the machine that triggered the request. | all |
| `Location-Name` | The location of the machine that triggered the request. | `part_online`, `part_offline` |
| `Part-Id` |  The part of the machine that triggered the request. | all |
| `Machine-Name` | The name of the machine that triggered the request. | `part_online`, `part_offline` |
| `Robot-Id` | The ID of the machine that triggered the request. | all |

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
