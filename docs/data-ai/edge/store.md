---
linkTitle: "Store"
title: "Store data"
weight: 40
layout: "docs"
type: "docs"
languages: []
date: "2024-12-03"
description: "Different ways you can store data in the Viam cloud."
---

## Cache most recent data

If you want faster access to your most recent sensor readings, you can configure hot data storage.
The hot data store keeps a rolling window of hot data for faster queries.
All historical data remains in your default storage.

To configure the hot data store:

1. Use the `recent_data_store` attribute on each capture method in your data manager service.
2. Configure your queries' data source to the hot data store by passing the `use_recent_data` boolean argument to [tabularDataByMQL](/dev/reference/apis/data-client/#tabulardatabymql).

{{% expand "Click to view a sample configuration" %}}

The following sample configuration captures data from a sensor at 0.5 Hz.
`viam-server` stores the last 24 hours of data in a shared recent-data database, while continuing to write all data to blob storage:

```json {class="line-numbers linkable-line-numbers" data-line="17-19"}
{
  "components": [
    {
      "name": "sensor-1",
      "api": "rdk:component:sensor",
      "model": "rdk:builtin:fake",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.5,
                "additional_params": {},
                "recent_data_store": {
                  "stored_hours": 24
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

{{% /expand%}}

## Store in your own MongoDB cluster

You can configure direct capture of tabular data to a MongoDB instance alongside disk storage on your edge device.
This can be useful for powering real-time dashboards before data is synced from the edge to the cloud.
The MongoDB instance can be a locally running instance or a cluster in the cloud.

Configure using the `mongo_capture_config` attributes in your data manager service.
You can configure data sync to a MongoDB instance separately from data sync to the Viam Cloud.

{{< expand "Click to view sample configuration with MongoDB data store." >}}

This sample configuration captures fake sensor readings both to the configured MongoDB URI as well as to the `~/.viam/capture` directory on disk.
It does not sync the data to the Viam Cloud.

```json
{
  "components": [
    {
      "name": "sensor-1",
      "api": "rdk:component:sensor",
      "model": "rdk:builtin:fake",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.5,
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
  "services": [
    {
      "name": "data_manager-1",
      "api": "rdk:service:data_manager",
      "attributes": {
        "mongo_capture_config": {
          "uri": "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
        }
      }
    }
  ]
}
```

{{< /expand >}}

{{< expand "Click to view sample configuration with MongoDB data store and sync to the Viam Cloud." >}}

This sample configuration captures fake sensor readings both to the configured MongoDB URI as well as to the `~/.viam/capture` directory on disk.
It syncs data to the Viam Cloud every 0.1 minutes.

```json
{
  "components": [
    {
      "name": "sensor-1",
      "api": "rdk:component:sensor",
      "model": "rdk:builtin:fake",
      "attributes": {},
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Readings",
                "capture_frequency_hz": 0.5,
                "additional_params": {}
              }
            ]
          }
        }
      ]
    }
  ],
  "services": [
    {
      "name": "data_manager-1",
      "api": "rdk:service:data_manager",
      "attributes": {
        "mongo_capture_config": {
          "uri": "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
        },
        "additional_sync_paths": [],
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "capture_disabled": false,
        "sync_disabled": false,
        "tags": []
      }
    }
  ]
}
```

{{< /expand >}}

When `mongo_capture_config.uri` is configured, data capture will attempt to connect to the configured MongoDB server and write captured tabular data to the configured `mongo_capture_config.database` and `mongo_capture_config.collection` (or their defaults if unconfigured) after enqueuing that data to be written to disk.

If writes to MongoDB fail for any reason, data capture will log an error for each failed write and continue capturing.

Failing to write to MongoDB doesn't affect capturing and syncing data to cloud storage other than adding capture latency.

{{< alert title="Caution" color="caution" >}}

- Capturing directly to MongoDB may write data to MongoDB that later fails to be written to disk (and therefore never gets synced to cloud storage).
- Capturing directly to MongoDB does not retry failed writes to MongoDB. As a consequence, it is NOT guaranteed all data captured will be written to MongoDB.
  This can happen in cases such as MongoDB being inaccessible to `viam-server` or writes timing out.
- Capturing directly to MongoDB may reduce the maximum frequency that data capture can capture data due to the added latency of writing to MongoDB.
  If your use case needs to support very high capture rates, this feature may not be appropriate.

{{< /alert >}}

## Configure retention

Configure how long your synced data remains stored in the cloud:

- **Retain data up to a certain size (for example, 100GB) or for a specific length of time (for example, 14 days):** Set `retention_policies` at the resource level.
  See the `retention_policy` field in [data capture configuration attributes](/data-ai/reference/advanced-data-capture-sync/#click-to-view-data-capture-attributes).
- **Delete data captured by a machine when you delete the machine:** Control whether your cloud data is deleted when a machine or machine part is removed.
  See the `delete_data_on_part_deletion` field in the [data management service configuration attributes](/data-ai/reference/advanced-data-capture-sync/#click-to-view-data-management-attributes).
