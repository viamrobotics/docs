---
title: "Trigger Cloud Sync conditionally"
linkTitle: "Trigger Sync"
description: "Configure cloud sync to automatically capture data in the Viam app."
weight: 36
type: "docs"
tags: ["data management", "cloud", "sync"]
# SME: Alexa Greenberg
---

If you rely on mobile data but have intermittent WiFi connection in certain locations or at certain times of the day, you may want to trigger sync to only occur when these conditions are met.

To set up conditional syncing you need to create a module with custom sync logic and then change the configuration of the data manager to enable selective sync.

## Add module

In this example, you will learn how to configure sync to only trigger at a specific time of day.
If you need to trigger sync based on a different condition, adjust the module logic accordingly.

###

TODO: Change to time of day.

## Add sensor

On your machine's **Config** tab, add a sensor based on your module.
The sensor will return true when your condition occurs.
In the next step you will configure the data manager to take this into account when syncing.

{{< tabs >}}
{{% tab name="Config builder" %}}

{{% /tab %}}
{{% tab name="JSON" %}}

{{% /tab %}}
{{< /tabs >}}

```
    {
      "attributes": {},
      "depends_on": [],
      "model": "selectivesync:demo:time",
      "name": "selective-syncer",
      "namespace": "rdk",
      "service_configs": [
        {
          "attributes": {
            "capture_methods": []
          },
          "type": "data_manager"
        }
      ],
      "type": "sensor"
    },
```

## Enable selective sync

On your machine's **Config** tab, switch to **JSON** mode and add a `selective_syncer_name` with the name for the sensor you configured:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers" data-line="6"}
{
  "attributes": {
    "additional_sync_paths": [],
    "capture_dir": "",
    "capture_disabled": false,
    "selective_syncer_name": "selective-syncer",
    "sync_disabled": false,
    "sync_interval_mins": 0.1,
    "tags": []
  },
  "name": "Data-Management-Service",
  "type": "data_manager"
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers" data-line="3-18,44-50,53-65"}
{
  "components": [
    {
      "attributes": {},
      "depends_on": [],
      "model": "selectivesync:demo:time",
      "name": "selective-syncer",
      "namespace": "rdk",
      "service_configs": [
        {
          "attributes": {
            "capture_methods": []
          },
          "type": "data_manager"
        }
      ],
      "type": "sensor"
    },
    {
      "name": "webcam",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": [],
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "ReadImage",
                "additional_params": {
                  "mime_type": "image/jpeg"
                },
                "capture_frequency_hz": 1
              }
            ]
          }
        }
      ]
    }
  ],
  "modules": [
    {
      "executable_path": "/Users/alexagreenberg/viam-labs/trigger-sync-examples-v2/time-interval-trigger/time-interval-trigger",
      "name": "test-module",
      "type": "local"
    }
  ],
  "packages": [],
  "services": [
    {
      "attributes": {
        "additional_sync_paths": [],
        "capture_dir": "",
        "capture_disabled": false,
        "selective_syncer_name": "selective-syncer",
        "sync_disabled": false,
        "sync_interval_mins": 0.1,
        "tags": []
      },
      "name": "Data-Management-Service",
      "type": "data_manager"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Test

bla
