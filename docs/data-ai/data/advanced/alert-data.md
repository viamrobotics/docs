---
linkTitle: "Alert on data"
title: "Alert on data"
weight: 60
layout: "docs"
type: "docs"
no_list: true
description: "Use triggers to send email notifications or webhook requests when inferences are made."
---

Follow this guide to learn how to configure a trigger to send webhook requests or emails for the following events:

- **Data has been synced to the cloud**: trigger when data from the machine is synced
- **Conditional data ingestion**: trigger any time data is captured from a specified component with a specified method and condition

For example, you can configure a trigger to send you a notification when your robot's sensor collects a new reading.

To configure a trigger:

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

2. Name the trigger and click **Create**.

3. Select trigger **Type**.
   Configure additional attributes:

{{< tabs name="Types of Triggers" >}}
{{% tab name="Data synced to cloud" %}}

Select the data types for which the Trigger should send requests.
Whenever data of the specified data types is ingested, a `POST` request will be sent.

{{% /tab %}}
{{% tab name="Conditional data ingestion" %}}

Select the component you want to capture data from and the method you want to capture data from.
Then, add any conditions.

These can include a key, a value, and a logical operator.
For example, a trigger configured to fire when data is captured from the motor `motor-1`'s `IsPowered` method when `is_on` is equal to `True`:

{{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x400" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." >}}

For more information, see [Conditions](#conditions).

{{% alert title="Note" color="note" %}}
You must [configure data capture](/services/data/) for your component to use this trigger.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

4. Add **Webhooks** or **Emails**.

{{< tabs name="Notifications types" >}}
{{% tab name="Webhooks" %}}

Click **Add Webhook**.
Add the URL of your cloud function or lambda.
Configure the time between notifications.

![The trigger configured with an example URL in the Viam app.](/build/configure/trigger-configured.png)

{{% /tab %}}
{{% tab name="Emails" %}}

Click **Add Email**.
Add the email you wish to be notified whenever this trigger is triggered.
Configure the time between notifications.

![The trigger configured with an example email in the Viam app.](/build/configure/trigger-configured-email.png)

{{% /tab %}}
{{< /tabs >}}
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
        "type": "part_data_ingested",
        "data_ingested": {
          "data_types": ["binary", "tabular", "file"]
        }
      },
      "notifications": [
        {
          "type": "webhook",
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": 0
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
| `event` |  object | **Required** | The trigger event object: <ul><li>`type`: The type of the event to trigger on. Options: `part_data_ingested`, `conditional_data_ingested`.</li><li>`data_types`: Required with `type` `part_data_ingested`. The data types that trigger the event. Options: `binary`, `tabular`, `file`, `unspecified`. </li><li> `conditional`: Required with `type` `conditional_data_ingested`. See [Conditions](#conditions) for more information. </li></ul> |
| `notifications` |  object | **Required** | The notifications object: <ul><li>`type`: The type of the notification. Options: `webhook`, `email`</li><li>`value`: The URL to send the request to or the email address to notify.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> |

#### Conditions

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

5. If using a webhook, write your cloud function or lambda to process the request from `viam-server`.
   You can use your cloud function or lambda to interact with any external API such as, for example, Twilio, PagerDuty, or Zapier.
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

## Returned headers

When a trigger occurs, Viam sends a HTTP request to the URL you specified for the trigger:

<!-- prettier-ignore -->
| Trigger type | HTTP Method |
| ------------ | ----------- |
| `part_data_ingested` | POST |
| `conditional_data_ingested` | POST ||

The request includes the following headers:

<!-- prettier-ignore -->
| Header Key | Description |
| ---------- | ----------- |
| `Org-Id` | The ID of the organization that triggered the request. |
| `Location-Id` | The location of the machine that triggered the request. |
| `Part-Id` |  The part of the machine that triggered the request. |
| `Robot-Id` | The ID of the machine that triggered the request. |

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

## Next steps

To see an example project that uses triggers to send email notification, see the [Monitor Job Site Helmet Usage with Computer Vision tutorial](/tutorials/projects/helmet/#configure-a-trigger-on-your-machine).

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
