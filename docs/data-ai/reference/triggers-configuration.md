---
title: "Trigger configuration"
linkTitle: "Trigger configuration"
weight: 60
type: "docs"
tags: ["data management", "trigger", "webhook"]
description: "Detailed information about how to configure triggers and webhooks."
date: "2025-05-05"
updated: "2025-09-18"
---

Triggers can alert you by email or webhook when any of the following events occur:

- [machine telemetry data syncs from your local device to the Viam cloud](/manage/troubleshoot/alert/)
- [data syncs from a machine](/data-ai/data/alert-data/)
- [service detects a specified object or classifies a specified label](/data-ai/ai/alert/)

This page provides a reference for the Trigger attributes.
For step-by-step configuration information, see the links above instead.

## JSON configuration templates

### Part status trigger template

The following template demonstrates the structure of a JSON configuration for a trigger that alerts when a part is online or offline:

```json {class="line-numbers linkable-line-numbers"}
"triggers": [
  {
    "name": "<trigger name>",
    "event": {
      "type": "part_online|part_offline"
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

### Data sync trigger template

The following template demonstrates the structure of a JSON configuration for a trigger that alerts when data syncs to the Viam cloud:

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
    {
      "name": "<trigger name>",
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
          "seconds_between_notifications": <number of seconds>
        }
      ]
    }
  ]
```

### Conditional trigger template

The following template demonstrates the structure of a JSON configuration for a conditional trigger:

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

## Trigger attributes

Triggers support the following attributes:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the trigger |
| `event` |  object | **Required** | The trigger event object, which contains the following fields: <ul><li>`type`: The type of the event to trigger on. Options: <ul><li>`part_data_ingested`: fire when data syncs</li> <li>`conditional_data_ingested`: fire when data that meets a certain condition syncs</li> <li>`part_online`: fire when the part is online</li> <li>`part_offline`: fire when the part is offline</li></ul></li><li>`data_types`: Required with `type` `part_data_ingested`. An array of data types that trigger the event. Options: `binary`, `tabular`, `file`, `unspecified`. </li><li> `conditional`: Required when `type` is `conditional_data_ingested`. For more information about this field, see [Conditional attributes](/data-ai/reference/triggers-configuration/#conditional-attributes). </li></ul> |
| `notifications` |  object | **Required** | The notifications object, which contains the following fields: <ul><li>`type`: The type of the notification. Options: `webhook`, `email`</li><li>`value`: The URL to send the request to or the email address to notify.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> For more information on webhooks, see [Webhook attributes](#webhook-attributes). |
| `notes` | string | Optional | Descriptive text to document the purpose, configuration details, or other important information about this trigger. |

## Conditional attributes

The `conditional` object for the `conditional_data_ingested` trigger type includes the following attributes:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `data_capture_method` | string | **Required** | The method of data capture to trigger on. <br> Example: `sensor:<name-of-component>:Readings`. |
| `conditions` | object | Optional | Conditions that, when true, fire the trigger. Evaluated each time data syncs from the linked component. When this object is empty or not present, the trigger fires each time data syncs from the linked component. <br> Options: <ul><li>`evals`:<ul><li>`operator`: Logical operator for the condition. </li><li>`value`: An object containing a single field and value. The field specifies the path, in the synced data, to the left operand of the conditional. For nested fields, use periods as separators or define the nested structure in JSON. The value specifies an object, string, boolean, regular expression, or integer used as a right operand in the conditional. </li></ul></li></ul> |

The `operator` attribute supports the following values:

| Name    | Description                |
| ------- | -------------------------- |
| `lt`    | less than                  |
| `gt`    | greater than               |
| `lte`   | less than or equal to      |
| `gte`   | greater than or equal to   |
| `eq`    | equal to                   |
| `neq`   | not equal to               |
| `regex` | matches regular expression |

### Example

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

### Nested key example

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

## Webhook attributes

### Request types

When an event occurs, Viam sends an HTTP request to the URL you specified for the trigger:

<!-- prettier-ignore -->
| Trigger type | HTTP Method |
| ------------ | ----------- |
| `part_data_ingested` | POST |
| `conditional_data_ingested` | POST |
| `part_online` | GET |
| `part_offline` | GET |

### Headers

The request includes the following headers:

<!-- prettier-ignore -->
| Header Key | Description | Trigger types |
| ---------- | ----------- | ------------- |
| `Org-Id` | The ID of the organization that triggered the request. | all |
| `Organization-Name` | The name of the organization that triggered the request. | `part_online`, `part_offline` |
| `Location-Id` | The location of the machine that triggered the request. | all |
| `Location-Name` | The location of the machine that triggered the request. | `part_online`, `part_offline` |
| `Part-Id` | The part of the machine that triggered the request. | all |
| `Machine-Name` | The name of the machine that triggered the request. | `part_online`, `part_offline` |
| `Robot-Id` | The ID of the machine that triggered the request. | all |

### Body

The request body includes the following data:

<!-- prettier-ignore -->
| Data Key | Description | Trigger types |
| -------- | ----------- | ------------- |
| `component_name` | The name of the component for which data was ingested. | `part_data_ingested`, `conditional_data_ingested` |
| `component_type` | The type of component for which data was ingested. | `part_data_ingested`, `conditional_data_ingested` |
| `method_name` | The name of the method from which data was ingested. | `part_data_ingested`, `conditional_data_ingested` |
| `min_time_received` | Indicates the earliest time a piece of data was received. | `part_data_ingested` |
| `max_time_received` | Indicates the latest time a piece of data was received. | `part_data_ingested` |
| `machine_name` | The name of the machine that triggered the request. | `part_data_ingested`, `conditional_data_ingested` |
| `location_name` | The location of the machine that triggered the request. | `part_data_ingested`, `conditional_data_ingested` |
| `org_name` | The name of the organization that triggered the request. | `part_data_ingested`, `conditional_data_ingested` |
| `file_id` | The ID of the file that was ingested. | `part_data_ingested` |
| `trigger_condition` | The condition that triggered the request. | `conditional_data_ingested` |
| `data` | The ingested sensor data. Includes `metadata` with `received_at` and `requested_at` timestamps and `data` in the form `map[string]any`. | `part_data_ingested`, `conditional_data_ingested` (sensor data) |

### Example cloud function

If you are using a cloud function or lambda to process the request from `viam-server`, you can use this template.

The following example function prints the received headers:

{{< tabs >}}
{{% tab name="Flask" %}}

```python {class="line-numbers linkable-line-numbers"}
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

### Troubleshooting

If the HTTP request Viam sends results in an error, you can see this error logged in the machine logs.

For example:

```txt
9/18/2025, 12:52:59 PM error app.trigger.trigger-1     Trigger failed to notify https://testurl.com for robotPartId abc1234d-1a23-1a23-123a-1abc23d45e67. Component: N/A, Method: N/A, TriggerType: part_online, NotificationType: webhook, Error: received unretryable status code: 404 in webhook response, ResponseCode: 404
```
