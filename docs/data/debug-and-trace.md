---
linkTitle: "Debug and trace"
title: "Debug and trace"
weight: 50
layout: "docs"
type: "docs"
description: "Use distributed tracing to debug what your robot did, trace requests across components, and export traces to observability tools."
date: "2026-03-26"
---

When something goes wrong on your robot, you need to understand what happened and when. Viam includes distributed tracing built on [OpenTelemetry](https://opentelemetry.io/) that traces requests across your SDK code, `viam-server`, and any modules running on the machine.

## What tracing provides

- **Request-level visibility**: trace a single API call from your SDK through viam-server to the component or module that handles it.
- **Latency breakdown**: see how long each step in the call chain takes.
- **Cross-module correlation**: trace context propagates automatically across gRPC boundaries, including into modules.
- **Export to standard tools**: send traces to Jaeger, Grafana Tempo, Datadog, or any OpenTelemetry-compatible backend.

## Enable tracing

Add a `tracing` section to your machine's JSON configuration:

```json
{
  "tracing": {
    "enabled": true,
    "disk": true
  }
}
```

| Field          | Type   | Description                                                                                                              |
| -------------- | ------ | ------------------------------------------------------------------------------------------------------------------------ |
| `enabled`      | bool   | Enable or disable tracing for this machine.                                                                              |
| `disk`         | bool   | Save traces to local disk at `~/.viam/trace/{part-id}/traces`. Uses OTLP binary format with 2GB file rotation.           |
| `console`      | bool   | Print traces to stdout in real time. Useful for local development. Note: cannot capture spans from modules in this mode. |
| `otlpendpoint` | string | Send traces to an external OTLP gRPC endpoint (for example, `localhost:4317` for a local Jaeger instance).               |

You can enable multiple export options at once (for example, both `disk` and `otlpendpoint`).

## Retrieve traces from a machine

Use the Viam CLI to download or view traces:

**Download traces from a remote machine:**

```bash
viam traces get-remote
```

This downloads trace files from the machine to your local disk.

**Print traces from a remote machine:**

```bash
viam traces print-remote
```

**Print traces from a local file:**

```bash
viam traces print-local <path-to-trace-file>
```

**Import local traces to an OTLP collector:**

```bash
viam traces import-local <path-to-trace-file>
```

This sends saved trace data to an OTLP endpoint, which is useful for loading historical traces into Jaeger or Tempo after the fact.

## Export to an observability backend

To send traces directly to an observability tool, set the `otlpendpoint` field to your collector's gRPC address.

**Example: Jaeger running locally:**

```json
{
  "tracing": {
    "enabled": true,
    "otlpendpoint": "localhost:4317"
  }
}
```

Start Jaeger with OTLP support:

```bash
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  jaegertracing/all-in-one:latest
```

Then open `http://localhost:16686` to view traces. You should see the `rdk` service with spans for each API call your robot handles.

## What traces show

Each trace represents a request flowing through the system. A typical trace includes:

- **SDK call**: your Python or Go code calling a component method
- **gRPC transport**: the request traveling from your code to viam-server
- **viam-server handling**: routing the request to the correct component or service
- **Module execution**: if the component is provided by a module, the trace continues into the module's handler

Spans include timing, status codes, and any errors that occurred. This lets you see exactly where a request failed or where latency is concentrated.

## Combine with data queries

Tracing shows you the request path. Data capture shows you the sensor values. Together they give you a complete picture:

1. Use a time-range query on captured data to find when a sensor reading was anomalous.
2. Check traces from the same time window to see what requests were happening and whether any errors occurred.
3. Correlate the sensor reading with the component's processing trace to understand the full context.

For time-range queries on captured data, see [Query data](/data/query/query-data/).

## Troubleshooting

{{< expand "No traces appearing" >}}

- Verify `"enabled": true` in the tracing config.
- If using disk export, check `~/.viam/trace/{part-id}/traces` for trace files.
- If using an OTLP endpoint, verify the collector is running and accepting connections on the configured port.
- Traces are generated per-request. If no API calls are being made (no SDK code running, no test panel interactions), there will be no traces.

{{< /expand >}}

{{< expand "Module traces missing" >}}

- Module traces are sent back to viam-server through the `SendTraces` RPC and forwarded to your configured exporters. If module traces are missing, check the module's logs for connection errors.
- Console export (`"console": true`) cannot capture module spans due to ordering constraints. Use disk or OTLP export instead.

{{< /expand >}}
