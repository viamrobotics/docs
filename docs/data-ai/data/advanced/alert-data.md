---
linkTitle: "Alert on data"
title: "Alert on data"
weight: 60
layout: "docs"
type: "docs"
description: "Use triggers to send email notifications or webhook requests when data from the machine is synced."
prev: "/data-ai/data/export/"
---

You can use triggers to send alerts by email or webhook when data syncs from a machine.
For example, a trigger could alert you when a sensor detects a temperature greater than 100 degrees Celsius.

You can configure triggers to alert in the following scenarios:

- **Data has been synced to the cloud**: alert when any data syncs from the machine
- **Conditional data ingestion**: alert any time synced data meets a specified condition

## Configure a trigger

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Trigger**.

   {{<imgproc src="/build/configure/trigger-create.png" resize="x400" declaredimensions=true alt="The Create menu with Trigger at the bottom of the list of options." class="shadow" >}}

1. Enter a name and click **Create**.

1. In the **Type** dropdown, choose one of the following types:

   - **Data has been synced to the cloud**:
     Whenever your machine syncs data of any of the specified data types, the trigger sends an alert.
     Then, select the data types for which the trigger should send requests.
   - **Conditional data ingestion**:
     Whenever your machine syncs data that meets certain criteria, the trigger sends an alert.

     1. Choose the target component and method for your condition.
     1. Add a **condition**: specify a **key** in the synced data, an **operator**, and a **value**.
        When data from the target component and method syncs from your machine, the trigger uses the key as a path to look up a value in the synced data object.
        The trigger applies the operator to the extracted value and the value you specified in your condition.

        For example, the following trigger sends an alert when the `cpu-monitor` component's `Readings` method syncs `cpu` usage greater than `50`:

        {{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x400" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." class="shadow" >}}

        For more information, see [Conditional attributes](/data-ai/reference/triggers-configuration/#conditional-attributes).

1. To add a notification method, add an entry to the **Webhooks** or **Email** sub-panels:

   To add an email notification:

   1. Click **Add Email**.
      {{<imgproc src="/build/configure/trigger-configured-email.png" resize="x400" style="width: 500px" declaredimensions=true alt="A trigger configured with an example email." class="shadow" >}}
   1. Add the email you wish to be notified whenever this trigger is triggered.
   1. Configure the time between notifications.

   To add a webhook notification:

   1. Click **Add Webhook**.
      {{<imgproc src="/build/configure/trigger-configured.png" resize="x400" style="width: 500px" declaredimensions=true alt="A trigger configured with an example URL." class="shadow" >}}
   1. Add the URL of your cloud function.
   1. Configure the time between notifications.
   1. Write your cloud function to process the [webhook](/data-ai/reference/triggers-configuration/#webhook-attributes).
      Use your cloud function to process data or interact with any external API, including Twilio, PagerDuty, or Zapier.

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="32-49"}
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

For more information about triggers, see [Trigger Configuration](/data-ai/reference/triggers-configuration/).

{{% /tab %}}
{{< /tabs >}}
