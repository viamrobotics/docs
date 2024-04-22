---
title: "Configure a Webhook"
linkTitle: "Webhooks"
weight: 50
type: "docs"
description: "Configure a webhook to trigger actions when certain types of data are sent from your machine to the cloud, or when the internet connectivity of your machine changes."
tags: ["webhooks"]
---

Webhooks allow you to trigger actions when certain types of data are sent from your machine to the cloud, or when the internet connectivity of your machine changes.
For example, you can configure a webhook to send you a notification when your robot's sensor collects a new reading.
Viam provides two webhook types depending on the event you want to trigger on:

- `"part_data_ingested"`: trigger when a sensor on the machine part collects a new reading
- `"part_online"`: trigger when the machine part is online

To configure a webhook:

{{< tabs name="Types of Webhooks" >}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Select **JSON** mode.

2. Follow the instructions depending on the type of webhook you want to implement:

{{% tab name="part_data_ingested" %}}

1. Paste the following JSON template into your JSON config.
   `"webhooks"` is a top-level section like `"components"`, `"services"`, or any of the other config sections.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
  "webhooks": [
    {
      "url": "<Insert your own cloud function or lambda URL for sending the event>",
      "event": {
        "attributes": {
          "data_types": ["binary", "tabular", "file"]
        },
        "type": "part_data_ingested"
      }
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
  "webhooks": [
    {
      "url": "https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws",
      "event": {
        "attributes": {
          "data_types": ["binary", "tabular"]
        },
        "type": "part_data_ingested"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

2. Replace the URL value with the URL of your cloud/lambda function.
3. Edit the `data_types` list to include only the types of data you want to trigger on.
4. Configure [data capture](/data/capture/) and [cloud sync](/data/cloud-sync/) for the relevant components.
   For example, if you want to trigger a webhook on temperature readings, configure data capture and sync on your temperature sensor.
   Be aware that the component must return the type of data you configured in `data_types`.
5. Write your cloud/lambda function to process the request from `viam-server`.
   The following example function sends a Slack message with a machine's details, such as robot and location IDs, when it receives a request:

   ```python {class="line-numbers linkable-line-numbers"}
   import functions_framework
   import requests
   import time

   @functions_framework.http
   def hello_http(request):
     payload = {
       "Org-ID": request.headers['org-id'] if 'org-id' in request.headers else 'no value',
       "Location-ID": request.headers['location-id'] if 'location-id' in request.headers else 'no value',
       "Part-ID": request.headers['part-id'] if 'part-id' in request.headers else 'no value',
       "Robot-ID": request.headers['robot-id'] if 'robot-id' in request.headers else 'no value'
     }

     slack_url = "<paste in your own Slack URL>"
     headers = {}

     response = requests.post(slack_url, json=payload, headers=headers)

     request_json = request.get_json(silent=True)
     request_args = request.args

     return 'Sent request to {}'.format(slack_url)

   ```

{{% /tab %}}
{{% tab name="part_online" %}}

1. Paste the following JSON template into your raw JSON config.
   `"webhooks"` is a top-level section like `"components"`, `"services"`, or any of the other config sections.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
  "webhooks": [
    {
      "url": "<Insert your own cloud function or lambda URL for sending the event>",
      "event": {
        "type": "part_online",
        "attributes": {
          "seconds_between_notifications": 10
        }
      }
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
      "service_configs": []
    }
  ],
  "webhooks": [
    {
      "url": "https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws",
      "event": {
        "type": "part_online",
        "attributes": {
          "seconds_between_notifications": 10
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

2. Replace the URL value with the URL of your cloud/lambda function.
3. While your part is online, the webhook action triggers at a specified interval.
   Edit the `seconds_between_notifications` attribute to set this interval according to your preferences.
4. Write your cloud/lambda function to process the request from `viam-server`.
   The following example function sends a Slack message with a machine's details, such as robot and location IDs, when it receives a request:

   ```python {class="line-numbers linkable-line-numbers"}
   import functions_framework
   import requests
   import time

   @functions_framework.http
   def hello_http(request):
     payload = {
       "Org-ID": request.headers['org-id'] if 'org-id' in request.headers else 'no value',
       "Location-ID": request.headers['location-id'] if 'location-id' in request.headers else 'no value',
       "Part-ID": request.headers['part-id'] if 'part-id' in request.headers else 'no value',
       "Robot-ID": request.headers['robot-id'] if 'robot-id' in request.headers else 'no value'
     }

     slack_url = "<paste in your own Slack URL>"
     headers = {}

     response = requests.post(slack_url, json=payload, headers=headers)

     request_json = request.get_json(silent=True)
     request_args = request.args

     return 'Sent request to {}'.format(slack_url)

   ```

{{% /tab %}}
{{< /tabs >}}
