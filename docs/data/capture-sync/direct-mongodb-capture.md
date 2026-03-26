---
linkTitle: "Direct MongoDB capture"
title: "Direct MongoDB capture"
weight: 8
layout: "docs"
type: "docs"
description: "Write tabular data directly to a MongoDB instance alongside normal disk capture."
date: "2025-02-10"
---

Write tabular data directly to a MongoDB instance alongside normal disk capture. This is useful for powering real-time dashboards before data syncs from the edge to the cloud. The MongoDB instance can be local or a cloud cluster.

{{< alert title="Caution" color="caution" >}}

- Data written to MongoDB may not also make it to disk (and therefore may never sync to cloud storage).
- Failed MongoDB writes are logged but not retried. Not all captured data is guaranteed to reach MongoDB.
- The added write latency may reduce the maximum achievable capture frequency.

{{< /alert >}}

## Configure

Configure using the `mongo_capture_config` attributes in your data management service. MongoDB capture and cloud sync are independent. You can enable either or both.

Add the following to your data management service attributes:

```json
{
  "mongo_capture_config": {
    "uri": "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"
  }
}
```

The `uri` field accepts any standard [MongoDB connection string](https://www.mongodb.com/docs/v6.2/reference/connection-string/). You can optionally specify `database` (default: `"sensorData"`) and `collection` (default: `"readings"`).

See the [data management service attributes](/data/capture-sync/advanced-data-capture-sync/#data-management-service-attributes) for the full list of `mongo_capture_config` fields.

## Example: MongoDB capture with cloud sync

This configuration captures sensor readings to both a local MongoDB instance and disk, with cloud sync enabled:

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
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "sync_disabled": false,
        "tags": []
      }
    }
  ]
}
```

To capture to MongoDB without cloud sync, set `"sync_disabled": true`.

If writes to MongoDB fail, data capture logs an error for each failed write and continues capturing. MongoDB write failures do not prevent data from being captured to disk or synced to the cloud.
