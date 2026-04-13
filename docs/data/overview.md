---
linkTitle: "Overview"
title: "Manage data"
weight: 1
layout: "docs"
type: "docs"
description: "Record sensor data on your robot, sync it to the cloud, and query, export, or use it for ML training."
---

Your robot's sensors, cameras, and other components produce data you need to record, analyze, and act on. Viam's data management service lets you configure which components to capture from, sync captured data to the cloud, and query, export, or use it for ML training without building a custom data pipeline.

## How data flows

Data moves through four stages, from your robot to actionable insights:

1. **Capture on the machine.** You configure which components to record from and at what frequency. Captured data is written to local disk. Nothing is captured until you configure it.
2. **Sync to the cloud.** A separate process uploads captured data to Viam's cloud at a configurable interval, then deletes local files. If the machine goes offline, data buffers locally and syncs when connectivity returns.
3. **Store.** In the cloud, tabular data (sensor readings, motor positions, encoder ticks) is stored in MongoDB. Binary data (images, point clouds, audio) is stored in blob storage. Both are indexed and queryable.
4. **Use.** From the cloud, you can query data with SQL or MQL, export it to your own database, build datasets for ML training, create monitoring dashboards, or trigger alerts when data meets a condition.

Capture and sync run independently: you can capture without syncing, or sync files from other sources without using Viam's capture.

To get started recording data, see [Capture and sync data](/data/capture-sync/capture-and-sync-data/).

## Query and explore

All captured tabular data is queryable through SQL and MQL, either in the Viam app's query editor or programmatically through the SDK. You can run ad-hoc queries for data exploration, create custom indexes to speed up frequent queries, and save queries for reuse. An AI-assisted query builder helps you write MQL aggregation pipelines.

Binary data (images, point clouds) is browsable and filterable in the Viam app's Data tab, with viewers for images, video, and 3D point clouds.

See [Query data](/data/query-data/) and [Query reference](/data/reference/).

## Transform and pipeline

Data pipelines run scheduled MQL aggregations on your captured data. Use them to compute hourly averages, detect trends, or reshape data for downstream tools. Pipelines run on a cron schedule with optional backfill for historical data.

A hot data store keeps a rolling window of recent data in a fast-query database, so you can build real-time dashboards without scanning the full archive.

See [Create a data pipeline](/data/pipelines/create-a-pipeline/) and [Hot data store](/data/hot-data-store/).

## Export and integrate

Viam is not a data silo. You can export data to your own tools and databases:

- **CLI export**: download binary or tabular data in bulk.
- **SDK access**: query and download data programmatically from Python or Go.
- **Direct MongoDB connection**: connect Grafana, Tableau, or custom scripts directly to your data through a MongoDB connection URI.

See [Export data](/data/export-data/) and [Sync to your database](/data/sync-data-to-your-database/).

## Delete data

You can delete captured data through the Viam app, the CLI, or the SDK. The SQL and MQL query editor is read-only: you cannot run `DELETE`, `DROP TABLE`, or any write operation through it.

**In the Viam app:**

- **Images and binary data**: on the **DATA** tab, select one or more items and click **Delete selected**, or use **Delete all** with the current filters applied. Point clouds, video, and file uploads can also be deleted this way.
- **Tabular data (sensor readings)**: the Sensors tab does not have a delete button. Use the CLI or SDK instead.

**From the CLI:**

```bash
# Delete tabular data older than N days
viam data delete-tabular --org-id=<org-id> --delete-older-than-days=30

# Delete binary data within a time range
viam data delete binary --org-ids=<org-id> --start=2026-01-01T00:00:00Z --end=2026-02-01T00:00:00Z
```

**From the SDK:**

The [data client API](/dev/reference/apis/data-client/) provides three delete methods:

- `delete_tabular_data(organization_id, delete_older_than_days)` deletes tabular rows older than a number of days.
- `delete_binary_data_by_filter(filter)` deletes binary data matching a filter (organization, location, time range, and so on).
- `delete_binary_data_by_ids(binary_ids)` deletes specific binary items by ID.

**Retention policies** can also auto-delete data in the cloud after a configured number of days. See [Platform-managed capture settings](/data/reference/#platform-managed-capture-settings) for the `retention_policy` field.

## Annotate and train

Captured images can be tagged, annotated with bounding boxes, and organized into datasets for ML training. Viam provides a complete path from captured data to a deployed model:

1. Capture images from your robot's cameras.
2. Label them with tags and bounding boxes in the Viam app.
3. Organize labeled images into a dataset.
4. Submit a training job (Vertex AI AutoML or your own training container).
5. Deploy the trained model back to your robot.

See [Create a dataset](/train/create-a-dataset/) and the training section for details.

## Monitor and debug

Triggers send webhooks or email alerts when synced data meets a condition, so you can respond to events like temperature spikes or detection results without polling.

Monitoring dashboards can be built with Viam's Teleop workspace or with Grafana connected to your data through MongoDB.

### OpenTelemetry distributed tracing

Viam includes OpenTelemetry (OTel) tracing that propagates trace context across your SDK code, `viam-server`, and modules. Traces cover gRPC request lifecycle, data capture operations, and module calls. When tracing is enabled on `viam-server`, module tracing is activated automatically.

To enable tracing, add a `tracing` block to your machine's JSON config:

```json
{
  "tracing": {
    "enabled": true,
    "disk": true
  }
}
```

This writes traces to `$HOME/.viam/trace/<part-id>/traces/` as compressed OTLP protobuf files. To export directly to an OTLP-compatible backend (Jaeger, Grafana Tempo, Datadog, or any OTLP collector), set `otlpendpoint` instead:

```json
{
  "tracing": {
    "enabled": true,
    "otlpendpoint": "localhost:4317"
  }
}
```

Download and import saved traces with the CLI. See [Traces](/monitor/troubleshoot/#traces) for the full CLI reference.

See [Trigger on data events](/data/trigger-on-data/) and [Visualize data](/data/visualize-data/).

## Manage data volume

Robots can generate more data than your network can transfer or your budget can store. Viam provides several tools to control data volume:

- **Capture frequency**: set per-component, from sub-second to infrequent intervals.
- **Conditional sync**: a sensor on the machine decides whether to sync or hold data.
- **Edge filtering**: write a custom sensor module that evaluates data before capture and only records what matters.
- **Retention policies**: configure how long data is retained in the cloud.

See [Filter at the edge](/data/filter-at-the-edge/) and [Conditional sync](/data/capture-sync/conditional-sync/).

## Security and data integrity

Data is encrypted in transit using {{< glossary_tooltip term_id="grpc" text="gRPC" >}} and encrypted at rest by the cloud storage provider.

The sync process is designed to prevent data loss and duplication:

- If the connection drops, the service retries at exponentially increasing intervals until restored.
- Sync resumes where it left off without duplicating data.
- Files still being written are not synced until they stabilize (configurable, default 10 seconds).
