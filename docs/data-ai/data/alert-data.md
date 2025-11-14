---
linkTitle: "Trigger on data events"
title: "Trigger on data events"
weight: 200
layout: "docs"
type: "docs"
description: "Use triggers to send email notifications or webhook requests when data from the machine is synced."
date: "2025-09-12"
aliases:
  - /data-ai/data/advanced/alert-data/
---

You can use triggers to send webhooks or email alerts when data syncs from a machine.
For example, a trigger could alert you when a sensor detects a temperature greater than 100 degrees Celsius.

You can configure triggers to fire in the following scenarios:

- **Data has been synced to the cloud**: fire when any data syncs from the machine
- **Conditional data ingestion**: fire any time synced data meets a specified condition

## Configure a trigger

{{< tabs >}}
{{% tab name="Builder mode" %}}

1. Go to the **CONFIGURE** tab of your machine.
   Click the **+** (Create) button in the left side menu and select **Trigger**.

1. Enter a name and click **Create**.

1. In the **Type** dropdown, choose one of the following event types:

   - **Data has been synced to the cloud**:
     Whenever your machine syncs data of any of the specified data types, the trigger fires.
     Then select the data types for which the trigger should send requests.
   - **Conditional data ingestion**:
     Whenever your machine syncs data that meets certain criteria, the trigger fires.

     1. Choose the target component and method for your condition.
     1. Add a **condition**: specify a **key** in the synced data, an **operator**, and a **value**.
        When data from the target component and method syncs from your machine, the trigger uses the key as a path to look up a value in the synced data object.
        The trigger applies the operator to the extracted value and the value you specified in your condition.

        For example, the following trigger sends an alert when the `cpu-monitor` component's `Readings` method syncs `cpu` usage greater than `50`:

        {{<imgproc src="/build/configure/conditional-data-ingested.png" resize="x800" declaredimensions=true alt="Example conditional data ingestion trigger with a condition." style="width: 600px" class="shadow imgzoom" >}}

        To see the data your components are returning, use each component's **TEST** panel.

        For more information about conditional attributes, see [Conditional attributes](/data-ai/reference/triggers-configuration/#conditional-attributes).

1. Next, configure what should happen when an event occurs.
   You can add **Webhooks** and **Email** notifications:

   To add a webhook:

   1. Click **Add Webhook**.
   1. Add the URL of your cloud function.
   1. Configure the time between notifications.
   1. Write your cloud function to process the [webhook](/data-ai/reference/triggers-configuration/#webhook-attributes).
      Use your cloud function to process data or interact with external APIs, such as Twilio, PagerDuty, or Zapier.
      For an example function, see [Example cloud function](/data-ai/reference/triggers-configuration/#example-cloud-function).

   To add an email notification:

   1. Click **Add Email**.
   1. Add the email address where you wish to be notified whenever this trigger fires.
   1. Configure the time between notifications.

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following JSON configuration shows how to set up a trigger that fires when any data is synced to the cloud:

```json {class="line-numbers linkable-line-numbers" data-line="32-54"}
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
          "value": "https://1abcde2ab3cd4efg5abcdefgh10zyxwv.lambda-url.us-east-1.on.aws",
          "seconds_between_notifications": 60
        },
        {
          "type": "email",
          "value": "test@viam.com",
          "seconds_between_notifications": 60
        }
      ]
    }
  ]
}
```

For more information about triggers, see [Trigger Configuration](/data-ai/reference/triggers-configuration/).

{{% /tab %}}
{{< /tabs >}}
