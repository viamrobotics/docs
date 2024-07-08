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
{{% tab name="Config Builder" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." >}}

2. Name the trigger and click **Create**.

3. Select the type of event to trigger on from the **Type** dropdown.

4. Follow the instructions depending on the type of trigger you want to implement:

{{< tabs name="Types of Triggers" >}}
{{% tab name="Data synced to cloud" %}}

5. Select the types of data you want to trigger on from the dropdown.
   Whenever any data of the type you select is synced from any component on your machine, the trigger will trigger.

{{% alert title="Note" color="note" %}}
Be sure to configure [data capture](/services/data/capture/) and [cloud sync](/services/data/cloud-sync/) for the relevant components.
For example, if you want to trigger a trigger on temperature readings, configure data capture and sync on your temperature sensor.
Be aware that the component must return the type of data you configure in the trigger's **Data Types**.
{{% /alert %}}

{{% /tab %}}
{{% tab name="Part is online" %}}

5. While your part is online, the trigger action executes at a specified interval.
   Edit the **Time between notifications** attribute to set this interval according to your preferences.

{{% /tab %}}
{{% tab name="Part is offline" %}}

5. While your part is offline, the trigger action executes at a specified interval.
   Edit the **Time between notifications** attribute to set this interval according to your preferences.

{{% /tab %}}
{{< /tabs >}}

6. Replace the URL value with the URL of your cloud/lambda function.

   ![The trigger configured with an example URL in the Viam app.](/build/configure/trigger-configured.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

If you prefer to configure your trigger with raw JSON instead of the config builder, you can paste one of the following JSON templates into your JSON config.
`"triggers"` is a top-level section like `"components"` or `"services"`.

{{< tabs >}}
{{% tab name="JSON Template: Data Synced" %}}

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
    {
      "url": "<Insert your own cloud function or lambda URL for sending the event>",
      "event": {
        "type": "part_data_ingested",
        "attributes": {
          "data_types": ["binary", "tabular", "file"]
        }
      }
    }
  ]
```

{{% /tab %}}
{{% tab name="JSON Template: Part Online" %}}

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
    {
      "url": "<Insert your own cloud function or lambda URL for sending the event>",
      "event": {
        "type": "part_online",
        "attributes": {
          "seconds_between_notifications": <number of seconds>
        }
      }
    }
  ]
```

{{% /tab %}}
{{% tab name="JSON Template: Part Offline" %}}

```json {class="line-numbers linkable-line-numbers"}
  "triggers": [
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
  "triggers": [
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

{{% /tab %}}
{{< /tabs >}}

7. Write your cloud/lambda function to process the request from `viam-server`.
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
       "Robot-ID": request.headers['robot-id'] if 'robot-id' in request.headers else 'no value',
       "Machine-Name": request.headers['machine-name'] if 'machine-name' in request.headers else 'no value',
       "Location-Name": request.headers['location-name'] if 'location-name' in request.headers else 'no value',
       "Organization-Name": request.headers['organization-name'] if 'organization-name' in request.headers else 'no value'
     }

     slack_url = "<paste in your own Slack URL>"
     headers = {}

     response = requests.post(slack_url, json=payload, headers=headers)

     request_json = request.get_json(silent=True)
     request_args = request.args

     return 'Sent request to {}'.format(slack_url)

   ```

## More examples

The [Monitor Job Site Helmet Usage with Computer Vision tutorial](/tutorials/projects/helmet/#configure-a-trigger-on-your-machine) uses triggers to send email notifications.

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
