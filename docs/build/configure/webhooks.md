---
title: "Configure a Webhook"
linkTitle: "Webhooks"
weight: 50
type: "docs"
description: "Configure a webhook to trigger actions when data is sent from your machine to the cloud, or when your machine's internet connectivity changes."
tags: ["webhooks"]
---

Webhooks allow you to trigger actions when certain types of data are sent from your machine to the cloud, or when the internet connectivity of your machine changes.
For example, you can configure a webhook to send you a notification when your robot's sensor collects a new reading.
Viam provides two webhook types depending on the event you want to trigger on:

- **Data has been synced to the cloud**: trigger when data from the machine is synced
- **Part is online**: trigger continuously at specified interval while the {{< glossary_tooltip term_id="part" text="machine part" >}} is online
- **Part is offline**: trigger continuously at specified interval while the machine part is offline

To configure a webhook:

{{< tabs >}}
{{% tab name="Config Builder" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Webhook**.

   {{<imgproc src="/build/configure/webhook-create.png" resize="x400" declaredimensions=true alt="The Create menu with Webhook at the bottom of the list of options." >}}

2. Name the webhook and click **Create**.

3. Select the type of event to trigger on from the **Type** dropdown.

4. Follow the instructions depending on the type of webhook you want to implement:

{{< tabs name="Types of Webhooks" >}}
{{% tab name="Data synced to cloud" %}}

5. Select the types of data you want to trigger on from the dropdown.
   Whenever any data of the type you select is synced from any component on your machine, the webhook will trigger.

{{% alert title="Note" color="note" %}}
Be sure to configure [data capture](/data/capture/) and [cloud sync](/data/cloud-sync/) for the relevant components.
For example, if you want to trigger a webhook on temperature readings, configure data capture and sync on your temperature sensor.
Be aware that the component must return the type of data you configure in the webhook's **Data Types**.
{{% /alert %}}

{{% /tab %}}
{{% tab name="Part is online" %}}

5. While your part is online, the webhook action triggers at a specified interval.
   Edit the **Time between notifications** attribute to set this interval according to your preferences.

{{% /tab %}}
{{% tab name="Part is offline" %}}

5. While your part is offline, the webhook action triggers at a specified interval.
   Edit the **Time between notifications** attribute to set this interval according to your preferences.

{{% /tab %}}
{{< /tabs >}}

6. Replace the URL value with the URL of your cloud/lambda function.

   ![The webhook configured with an example URL in the Viam app.](/build/configure/webhook-configured.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

If you prefer to configure your webhook with raw JSON instead of the config builder, you can paste one of the following JSON templates into your JSON config.
`"webhooks"` is a top-level section like `"components"` or `"services"`.

{{< tabs >}}
{{% tab name="JSON Template: Data Synced" %}}

```json {class="line-numbers linkable-line-numbers"}
  "webhooks": [
    {
      "url": "<Insert your own cloud function or lambda URL for sending the event>?data_type=binary",
      "event": {
        "type": "part_data_ingested",
        "attributes": {
          "data_types": ["binary", "tabular", "file"]
        },
        "type": "part_data_ingested",
        "headers": {
          "Component-Type": "<Component type>",
          "Component-Name": "<Component name>",
          "Method-Name": "<Method name>",
          "Min-Time-Received": "<Minimum time>",
          "Max-Time-Received": "<Maximum time>",
        }
      }
    }
  ]
```

{{% /tab %}}
{{% tab name="JSON Template: Part Online" %}}

```json {class="line-numbers linkable-line-numbers"}
  "webhooks": [
    {
      "url": "https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws?data_type=binary",
      "event": {
        "type": "part_online",
        "attributes": {
          "data_types": ["binary", "tabular"]
        },
        "type": "part_data_ingested",
        "headers": {
          "Component-Type": "sensor",
          "Component-Name": "my_temp_sensor",
          "Method-Name": "temperature_reading",
          "Min-Time-Received": "2024-01-01T00:00:00",
          "Max-Time-Received": "2024-01-01T23:59:59"
        }
      }
    }
  ]
```

{{% /tab %}}
{{< /tabs >}}

2. Replace the URL value with the URL of your cloud/lambda function.
3. Edit the `data_types` list to include only the types of data you want to trigger on.
4. Configure [data capture](/data/capture/) and [cloud sync](/data/cloud-sync/) for the relevant components.
   For example, if you want to trigger a webhook on temperature readings, configure data capture and sync on your temperature sensor.
   Be aware that the component must return the type of data you configured in `data_types`.
5. Write your cloud/lambda function to process the request from `viam-server`.
   The following example function sends a Slack message with a machine's details, such as robot and location IDs, as well as other relevant headers, when it receives a request:

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
       "Robot-ID": request.headers['robot-id'] if 'robot-id' in request.headers else 'no value',
       "Component-Type": request.headers['component-type'] if 'component-type' in request.headers else 'no value',
       "Component-Name": request.headers['component-name'] if 'component-name' in request.headers else 'no value',
       "Method-Name": request.headers['method-name'] if 'method-name' in request.headers else 'no value',
       "Min-Time-Received": request.headers['min-time-received'] if 'min-time-received' in request.headers else 'no value',
       "Max-Time-Received": request.headers['max-time-received'] if 'max-time-received' in request.headers else 'no value',

      "Data-Type": request.args['data_type'] if 'data_type' in request.args else 'no value'
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
        "type": "part_offline",
        "attributes": {
          "seconds_between_notifications": <number of seconds>
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
        "type": "part_data_ingested",
        "attributes": {
          "data_types": ["binary", "tabular"]
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
   The following example function sends a Slack message with a machine's details, such as robot and location IDs, as well as other relevant headers, when it receives a request:

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
       "Robot-ID": request.headers['robot-id'] if 'robot-id' in request.headers else 'no value',
       "Component-Type": request.headers['component-type'] if 'component-type' in request.headers else 'no value',
       "Component-Name": request.headers['component-name'] if 'component-name' in request.headers else 'no value',
       "Method-Name": request.headers['method-name'] if 'method-name' in request.headers else 'no value',
       "Min-Time-Received": request.headers['min-time-received'] if 'min-time-received' in request.headers else 'no value',
       "Max-Time-Received": request.headers['max-time-received'] if 'max-time-received' in request.headers else 'no value',

      "Data-Type": request.args['data_type'] if 'data_type' in request.args else 'no value'
     }

     slack_url = "<paste in your own Slack URL>"
     headers = {}

     response = requests.post(slack_url, json=payload, headers=headers)

     request_json = request.get_json(silent=True)
     request_args = request.args

     return 'Sent request to {}'.format(slack_url)

   ```

## More examples

The [Monitor Job Site Helmet Usage with Computer Vision tutorial](/tutorials/projects/helmet/#configure-a-webhook-on-your-machine) uses webhooks to send email notifications.

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
