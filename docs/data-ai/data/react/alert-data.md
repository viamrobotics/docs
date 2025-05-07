---
linkTitle: "Respond to new data"
title: "Respond to new data"
weight: 60
layout: "docs"
type: "docs"
description: "Use triggers to send email notifications or webhook requests when data from the machine is synced."
prev: "/data-ai/data/cloud/export/"
---

You can use triggers to send email notifications or webhook requests when data from the machine is synced, even captured from a specific component with a specified condition.
For example, you can configure a trigger to send you a notification when your robot's sensor collects a new reading.

Follow this guide to learn how to configure a trigger to send webhook requests or emails for the following events:

- **Data has been synced to the cloud**: trigger when data from the machine is synced
- **Conditional data ingestion**: trigger any time data is captured from a specified component with a specified method and condition

## Configure a trigger

To configure a trigger:

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine on the [Viam app](https://app.viam.com).
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow" >}}

2. Name the trigger and click **Create**.

3. Select trigger **Type**.
   Configure additional attributes:

{{< tabs name="Types of Triggers" >}}
{{% tab name="Data synced to cloud" %}}

Select the data types for which the trigger should send requests.
Whenever data of the specified data types is ingested, a `POST` request will be sent.

{{% /tab %}}
{{% tab name="Conditional data ingestion" %}}

Select the component you want to capture data from and the method you want to capture data from.
Then, add any conditions.

These can include a key, a value, and a logical operator.
For example, a trigger configured to fire when data is captured from the motor `motor-1`'s `IsPowered` method when `is_on` is equal to `True`:

{{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x400" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." class="shadow" >}}

For more information, see [Conditions](#conditions).

{{% alert title="Note" color="note" %}}
You must [configure data capture](/data-ai/data/edge/capture-sync/#configure-data-capture-and-sync-for-individual-resources) for your component to use this trigger.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

<ol><li style="counter-reset: item 3">Add <strong>Webhooks</strong> or <strong>Emails</strong></li></ol>

{{< tabs name="Notifications types" >}}
{{% tab name="Webhooks" %}}

Click **Add Webhook**.
Add the URL of your cloud function or lambda.
Configure the time between notifications.

{{<imgproc src="/build/configure/trigger-configured.png" resize="x400" style="width: 500px" declaredimensions=true alt="The trigger configured with an example URL in the Viam app." class="shadow" >}}

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

When configuring triggers to fire on data inside a JSON object, such as data from a sensor's `readings` object, the key you specify is the key inside the `readings` object (without `readings`).
For example:

{{< tabs >}}
{{% tab name="1 level of nesting" %}}

If your sensor returns readings of the format `{ "Line-Neutral AC RMS Voltage": 130 }`, the key you would specify is `"Line-Neutral AC RMS Voltage"`:

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

If your sensor returns readings of the format `{ "coordinate": { "latitude": 50 } }`, the key you would specify is `"coordinate.latitude"`:

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

{{< readfile "/static/include/webhooks.md" >}}
