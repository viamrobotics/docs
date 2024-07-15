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

3. Enter your preferred trigger type (for example, "**Data has been synced to the cloud**") into the field of the **Type** dropdown and select the type of event to trigger on.

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

6. Replace the **URL** value with the URL of your cloud function or lambda.

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
          "value": "<https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws>",
          "seconds_between_notifications": <number of seconds>
        }
      ],
      "headers": {
        "Component-Type": "<Component type>",
        "Component-Name": "<Component name>",
        "Method-Name": "<Method name>",
        "Min-Time-Received": "<Minimum time>",
        "Max-Time-Received": "<Maximum time>"
      }
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

7. Write your cloud function or lambda to process the request from `viam-server`.
   The following example function sends a message with a machine's details, such as robot and location IDs, when it receives a request:

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

     trigger_url = "<paste in your own trigger URL>"
     headers = {}

     response = requests.post(trigger_url, json=payload, headers=headers)

     request_json = request.get_json(silent=True)
     request_args = request.args

     return 'Sent request to {}'.format(trigger_url)

   ```

## `attributes`

To configure a trigger using JSON, you need to populate the `triggers` array with the appropriate attributes.

The attributes required to configure a trigger are outlined in the table below:

| Name                            | Required     | Parent Object   | Description                                   | Type             | Usage example |
| ------------------------------- | ------------ | --------------- | --------------------------------------------- | ---------------- | ------------- |
| `name`                          | **Required** | `triggers`      | The name of the trigger                       | string           |               |
| `type`                          | **Required** | `event`         | The type of event to trigger on               | string           |               |
| `data_types`                    | **Required** | `data_ingested` | The data types that trigger the event         | array of strings |               |
| `type`                          | **Required** | `notifications` | The type of notification to send              | string           |               |
| `value`                         | **Required** | `notifications` | The URL to send the notification to           | string           |               |
| `seconds_between_notifications` | Optional     | `notifications` | The interval between notifications in seconds | integer          |               |

## `headers`

You can populate the `headers` object in your JSON config to include additional context and data in your trigger configurations.

The `headers` object can include details such as the part of the machine involved, the type of component, the method being called, and the time range of the data.

When you configure your cloud function or lambda, you can access the headers to get detailed information about the event.
For example, the `Part-ID` header can be used to identify which specific part triggered the action, and the `Method-Name` header can identify which method was called.

The headers available for use are outlined below:

| Header Key          | Description                                               | Usage Example                                                      | Type   | Required |
| ------------------- | --------------------------------------------------------- | ------------------------------------------------------------------ | ------ | -------- |
| `Part-ID`           | Identifies the specific part of the machine.              | Isolate actions to a specific part of the machine.                 | string | Optional |
| `Robot-ID`          | Identifies the machine as a whole.                        | Useful for actions that pertain to the machine's entire system.    | string | Optional |
| `Location-ID`       | Identifies the location of the machine.                   | Location-based triggers or actions.                                | string | Optional |
| `Org-ID`            | Identifies the organization.                              | Organizational-level actions and tracking.                         | string | Optional |
| `Component-Type`    | Indicates the type of component involved.                 | Necessary for actions that depend on the component type.           | string | Optional |
| `Component-Name`    | Names the specific component.                             | Target the exact component for the action.                         | string | Optional |
| `Method-Name`       | Identifies the method being called.                       | Useful for actions triggered by specific methods.                  | string | Optional |
| `Min-Time-Received` | Indicates the earliest time a piece of data was received. | Useful for actions that depend on data timing.                     | string | Optional |
| `Max-Time-Received` | Indicates the latest time a piece of data was received.   | Similar to `Min-Time-Received`, useful for time-dependent actions. | string | Optional |

## More examples

The [Monitor Job Site Helmet Usage with Computer Vision tutorial](/tutorials/projects/helmet/#configure-a-trigger-on-your-machine) uses triggers to send email notifications.

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{< /cards >}}
