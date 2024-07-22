---
title: "Configure a Trigger"
linkTitle: "Triggers"
weight: 50
type: "docs"
description: "Configure a trigger to trigger actions when data is sent from your machine to the cloud, or when your machine's internet connectivity changes."
tags: ["triggers"]
aliases:
  - /build/configure/webhooks/
---

Triggers allow you to execute actions when certain types of data are sent from your machine to the cloud, or when the internet connectivity of your machine changes.
For example, you can configure a trigger to send you a notification when your robot's sensor collects a new reading.
Viam provides three trigger types depending on the event you want to trigger on:

- **Data has been synced to the cloud**: trigger when data from the machine is synced
- **Part is online**: trigger continuously at a specified interval while the {{< glossary_tooltip term_id="part" text="machine part" >}} is online
- **Part is offline**: trigger continuously at a specified interval while the machine part is offline

To configure a trigger:

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

2. Name the trigger and click **Create**.

3. Select trigger **Type**.
   For the respective type, configure the respective attributes:

{{< tabs name="Types of Triggers" >}}
{{% tab name="Data synced to cloud" %}}

Select the data types for which the Trigger should send requests.
Whenever data of the specified data types is ingested, a `POST` request will be sent.

{{% alert title="Note" color="note" %}}

You must have [data capture](/services/data/capture/) and [cloud sync](/services/data/cloud-sync/) configured for the relevant components to use this trigger and the component must return the type of data you configure in the trigger's **Data Types**.
For example, if you want to trigger a trigger on temperature readings, configure data capture and sync on your temperature sensor.
{{% /alert %}}

{{% /tab %}}
{{% tab name="Part is online" %}}

Edit the **Time between notifications** attribute to set the interval at which this trigger will send `GET` requests when the part is online.

{{% /tab %}}
{{% tab name="Part is offline" %}}

Edit the **Time between notifications** attribute to set the interval at which this trigger will send `GET` requests when the part is offline.

{{% /tab %}}
{{< /tabs >}}

4. Replace the **URL** value with the URL of your cloud function or lambda.

   ![The trigger configured with an example URL in the Viam app.](/build/configure/trigger-configured.png)

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
| `event` |  object | **Required** | The trigger event object: <ul><li>`type`: The type of the event to trigger on. Options: `"part_online"`, `"part_offline"`, `"part_data_ingested"`.</li><li>`data_types`: Required with `type` `"part_data_ingested"`. The data types that trigger the event. Options: `"binary"`, `"tabular"`, `"file"`, `"unspecified"`.</li></ul> |
| `notifications` |  object | **Required** | The notifications object: <ul><li>`type`: The type of the notification. Options: `"webhook"`.</li><li>`value`: The URL to send the request to.</li><li>`seconds_between_notifications`: The interval between notifications in seconds.</li></ul> |

5. Write your cloud function or lambda to process the request from `viam-server`.
   The following example function prints the received headers:

   {{< tabs >}}
   {{% tab name="Flask" %}}

```python {class="line-numbers linkable-line-numbers" }
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_http_get():
    headers = request.headers
    print(headers)
    payload = {
        "Org-Id": headers.get('org-id', 'no value'),
        "Organization-Name": headers.get('organization-name', 'no value'),
        "Location-Id": headers.get('location-id', 'no value'),
        "Location-Name": headers.get('location-name', 'no value'),
        "Part-Id": headers.get('part-id', 'no value'),
        "Part-Name": headers.get('part-name', 'no value'),
        "Robot-Id": headers.get('robot-id', 'no value'),
        "Machine-Name": headers.get('machine-name', 'no value'),
        "Component-Type": headers.get('component-type', 'no value'),
        "Component-Name": headers.get('component-name', 'no value'),
        "Method-Name": headers.get('method-name', 'no value'),
        "Min-Time-Received": headers.get('min-time-received', 'no value'),
        "Max-Time-Received": headers.get('max-time-received', 'no value'),
        "Data-Type": request.args.get('data_type', 'no value')
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
    payload = {
        "Org-Id": headers.get('org-id', 'no value'),
        "Organization-Name": headers.get('organization-name', 'no value'),
        "Location-Id": headers.get('location-id', 'no value'),
        "Location-Name": headers.get('location-name', 'no value'),
        "Part-Id": headers.get('part-id', 'no value'),
        "Part-Name": headers.get('part-name', 'no value'),
        "Robot-Id": headers.get('robot-id', 'no value'),
        "Machine-Name": headers.get('machine-name', 'no value'),
        "Component-Type": headers.get('component-type', 'no value'),
        "Component-Name": headers.get('component-name', 'no value'),
        "Method-Name": headers.get('method-name', 'no value'),
        "Min-Time-Received": headers.get('min-time-received', 'no value'),
        "Max-Time-Received": headers.get('max-time-received', 'no value'),
        "Data-Type": request.args.get('data_type', 'no value')
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
| `part_online` | GET |
| `part_offline` | GET |

The request includes the following headers:

<!-- prettier-ignore -->
| Header Key | Description | Trigger types |
| ---------- | ----------- | ------------- |
| `Org-Id` | The ID of the organization that triggered the request. | `part_data_ingested` |
| `Organization-Name` | The name of the organization that triggered the request. | `part_online`, `part_offline` |
| `Location-Id` | The location of the machine that triggered the request. | all |
| `Location-Name` | The location of the machine that triggered the request. | `part_online`, `part_offline` |
| `Part-Id` |  The part of the machine that triggered the request. | all |
| `Machine-Name` | The name of the machine that triggered the request. | `part_online`, `part_offline` |
| `Robot-Id` | The ID of the machine that triggered the request. | all |
| `Component-Type` | The type of component for which data was ingested. | `part_data_ingested` |
| `Component-Name` | The name of the component for which data was ingested. | `part_data_ingested` |
| `Method-Name` | The name of the method from which data was ingested. Only for `part_data_ingested` triggers. | `part_data_ingested` |
| `Min-Time-Received` | Indicates the earliest time a piece of data was received. | `part_data_ingested` |
| `Max-Time-Received` | Indicates the latest time a piece of data was received. | `part_data_ingested` |

## Next steps

To see an example project that uses triggers to send email notification, see the [Monitor Job Site Helmet Usage with Computer Vision tutorial](/tutorials/projects/helmet/#configure-a-trigger-on-your-machine).

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
