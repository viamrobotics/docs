---
linkTitle: "Trace requests"
title: "Trace requests with OpenTelemetry"
weight: 42
layout: "docs"
type: "docs"
description: "Enable OpenTelemetry tracing on a machine and in your modules to find where requests spend time and where they fail."
capabilities: ["logging", "module-development"]
diataxis: how-to
date: "2026-10-13"
aliases:
  - /data/debug-and-trace/
---

Viam includes OpenTelemetry (OTel) tracing that propagates trace context across your SDK code, `viam-server`, and modules. Traces cover gRPC request lifecycle, data capture operations, and module calls. When tracing is enabled on `viam-server`, module tracing is activated automatically.

## Enable tracing on a machine

To enable tracing, add a `tracing` block at the top level of your machine's JSON config (alongside `"components"` and `"services"`). You must set `enabled` to `true` **and** enable at least one export destination (`disk`, `console`, or `otlpendpoint`). Setting only `"enabled": true` without an export destination has no effect.

**Save traces to disk** for later retrieval with the CLI:

```json
{
  "tracing": {
    "enabled": true,
    "disk": true
  }
}
```

This writes traces to `$HOME/.viam/trace/<part-id>/traces/` as compressed OTLP protobuf files. Download and import saved traces with the CLI. See [Traces](/monitor/troubleshoot/#traces).

**Export directly to an OTLP-compatible backend** (Jaeger, Grafana Tempo, Datadog, or any OTLP collector):

```json
{
  "tracing": {
    "enabled": true,
    "otlpendpoint": "<collector-host>:4317"
  }
}
```

For local development, see the [Jaeger getting started guide](https://www.jaegertracing.io/docs/latest/getting-started/) to set up a local instance that accepts OTLP traces.

**Print traces to the console** for quick debugging without any external tools:

```json
{
  "tracing": {
    "enabled": true,
    "console": true
  }
}
```

You can combine multiple destinations (for example, `"disk": true` and `"otlpendpoint": "<collector-host>:4317"` together).

## Trace your module's methods

When tracing is enabled, each incoming component or service method call in your module opens its own span, nested under the RPC that triggered it.
Reading a camera, for example, produces a `GetImage` span under the caller's request span, so you can see how long that method takes as part of the whole request.

The Go, Python, and C++ SDKs all create these per-method spans.
`viam-server` sets the `VIAM_MODULE_TRACING` environment variable on each module process when tracing is enabled in the machine config.
The SDK inside the module records spans only when that variable is set.
You enable tracing once in the [`tracing` config block](#enable-tracing-on-a-machine), and individual modules pick it up.

Go modules record per-method spans automatically.
Python and C++ modules each need one more step, described below.

## Enable tracing in a Python module

Python module tracing is an opt-in extra.
Install `viam-sdk` with the `tracing` extra so the module has the OpenTelemetry packages it needs:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[tracing]'
```

Add this extra to your module's dependencies (for example, in `requirements.txt`) so it is present wherever the module runs.

The extra is the only change your module needs.
With the extra installed and tracing enabled in the machine config, each component and service method your module implements emits a span, and the module sends those spans to `viam-server`.
Without the extra installed, tracing stays off and your module runs unchanged.

To trace a section of your own code inside a method, open a child span with the OpenTelemetry API the extra installs.
The span nests under the automatic span for that method call:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class MySensor(Sensor):
    async def get_readings(self, **kwargs):
        with tracer.start_as_current_span("readings implementation") as span:
            span.set_attribute("multiplier", self.multiplier)  # attach structured context
            span.add_event("computing signal")
            return {"signal": self.multiplier}
```

Mark a failure on the span with `span.record_exception(error)` and `span.set_status(...)`.
When tracing is off, `start_as_current_span` returns a non-recording span, so the same code runs unchanged.

## Enable tracing in a C++ module

C++ tracing has two requirements: you build the SDK with OpenTelemetry support, and, as with Go and Python, tracing is enabled on `viam-server` in the machine config.
Compiling with OpenTelemetry support alone records nothing until the module runs under a `viam-server` that has tracing enabled; a build without OpenTelemetry support compiles the tracing calls as no-ops.

How you enable the build support depends on how you build the SDK:

- **With Conan:** the `opentelemetry_tracing` option is on by default.
  It pulls in `opentelemetry-cpp` with the OTLP gRPC exporter and compiles tracing into the SDK.
  To build without tracing, set the option off (`-o opentelemetry_tracing=False`).
- **With CMake directly:** the `VIAMCPPSDK_OPENTELEMETRY_TRACING` option is off by default.
  Turn it on with `-DVIAMCPPSDK_OPENTELEMETRY_TRACING=ON`, and provide `opentelemetry-cpp` (built with the OTLP gRPC exporter) as a dependency.

Because tracing must be compiled in, prebuilt SDK packages and the [cloud build](/cli/build-and-deploy-modules/#cloud-builds) image do not include it.
Build the SDK from source with the option above to record spans from a C++ module.

To trace a section of your own code inside a method, create a child span with `TracingSpan` from `<viam/sdk/tracing/span.hpp>`.
The span begins when you construct it and ends when it leaves scope, so scope it to the region you want to measure:

```cpp
#include <viam/sdk/tracing/span.hpp>

ProtoStruct MySensor::get_readings(const ProtoStruct&) {
    TracingSpan span("readings implementation");
    span.set_attribute("multiplier", multiplier_);  // attach structured context
    span.add_event("computing signal");
    // your logic here
    span.set_status_ok();
    return {{"signal", multiplier_}};
}
```

`TracingSpan` also provides `set_status_error()`, `record_exception()` and `record_unknown_exception()` to mark a failure, and `end()` to end the span before it leaves scope.
You cannot copy or move a `TracingSpan`.

This span nests under the automatic `GetReadings` span for the call, and the SDK exports it over OTLP gRPC to the destination you set in the [`tracing` config block](#enable-tracing-on-a-machine).
If the SDK is built without OpenTelemetry support, every `TracingSpan` call is a no-op and the code runs unchanged.

## Use traces to find latency and failures

Because each method span nests under the request that called it, a trace shows where time goes across service boundaries.
If a `Move` request is slow, expand its trace to see whether the delay is in the arm's `GetJointPositions` span, a vision service's `GetDetections` span, or the network between them.
A method that returns an error marks its span with an error status, so a failed span points to the method and machine that returned the failure.

Retrieve and inspect traces with the `viam traces` CLI commands.
See [Traces](/monitor/troubleshoot/#traces) and [Work with traces](/cli/manage-your-fleet/#work-with-traces).
