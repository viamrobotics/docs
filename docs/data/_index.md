---
linkTitle: "Overview"
title: "Manage data"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "Record sensor data on your robot, sync it to the cloud, and query, export, or use it for ML training."
aliases:
  - /build/data/
  - /services/data/capture/
  - /data/capture/
  - /build/micro-rdk/data_management/
  - /services/data/cloud-sync/
  - /data/cloud-sync/
  - /services/data/capture-sync/
  - /how-tos/sensor-data/
  - /services/data/
  - fleet/data-management/
  - /manage/data-management/
  - /services/data-management/
  - /manage/data/
  - /data-management/
  - /manage/data/view/
  - /data/view/
  - /services/data/view/
  - /how-tos/collect-data/
  - /how-tos/collect-sensor-data/
  - /get-started/quickstarts/collect-data/
  - /use-cases/collect-sensor-data/
  - /use-cases/image-data/
  - /get-started/collect-data/
  - /fleet/data-management/
  - /data-ai/capture-data/capture-sync/
  - /data/data-capture-reference/
  - /data/how-sync-works/
  - /data-ai/capture-data/advanced/how-sync-works/
  - /data/capture-sync/how-sync-works/
  - /data-ai/
  - /data-ai/capture-data/
  - /data-ai/data/
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

See [Query data](/data/query/query-data/) and [Query reference](/data/query/query-reference/).

## Transform and pipeline

Data pipelines run scheduled MQL aggregations on your captured data. Use them to compute hourly averages, detect trends, or reshape data for downstream tools. Pipelines run on a cron schedule with optional backfill for historical data.

A hot data store keeps a rolling window of recent data in a fast-query database, so you can build real-time dashboards without scanning the full archive.

See [Configure data pipelines](/data/query/configure-data-pipelines/) and [Hot data store](/data/query/hot-data-store/).

## Export and integrate

Viam is not a data silo. You can export data to your own tools and databases:

- **CLI export**: download binary or tabular data in bulk.
- **SDK access**: query and download data programmatically from Python or Go.
- **Direct MongoDB connection**: connect Grafana, Tableau, or custom scripts directly to your data through a MongoDB connection URI.

See [Export data](/data/export/export-data/) and [Sync to your database](/data/export/sync-data-to-your-database/).

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

For debugging, Viam includes OpenTelemetry distributed tracing that traces requests across your SDK code, viam-server, and modules. Traces can be exported to Jaeger, Grafana Tempo, Datadog, or saved to disk for later analysis.

Monitoring dashboards can be built with Viam's Teleop workspace or with Grafana connected to your data through MongoDB.

See [Trigger on data events](/data/trigger-on-data/), [Debug and trace](/data/debug-and-trace/), and [Visualize data](/data/visualize-data/).

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
