---
title: "Debug Endpoints"
linkTitle: "Debug Endpoints"
weight: 130
type: "docs"
description: "Advanced debugging endpoints available in viam-server for troubleshooting and development."
date: "2025-05-19"
---

The RDK (Robot Development Kit) that powers `viam-server` includes several debug endpoints that expose server internals.
These endpoints can be helpful during development or when troubleshooting complex issues:

- [`pprof`](#pprof)
- [`graph`](#graph)

## `pprof`

Setting `enable_web_profile` to `true` in your machine configuration allows you to visualize runtime profiling data by opening a locally hosted webpage that displays profiling data.
The pprof tool provides the following information about machine performance:

- CPU usage
- Memory allocation
- Goroutine blocking
- Execution tracing

For more detailed information on using pprof, refer to the [Go pprof documentation](https://pkg.go.dev/net/http/pprof).

### Configuration

To enable the pprof endpoints, set `enable_web_profile` to `true` in your machine configuration:

1. Navigate to the **CONFIGURE** tab of your machine in the Viam app
1. Click on the **...** menu next to your machine part in the left-hand menu
1. Select **Edit JSON**
1. Add the `enable_web_profile` field at the root level of your configuration:

```json
{
  "components": [...],
  "services": [...],
  "enable_web_profile": true
}
```

{{< alert title="Caution" color="caution" >}}
The debug endpoints expose internal details about your machine's configuration and runtime behavior.
Only enable these endpoints in development environments.
{{< /alert >}}

### Available Endpoints

Once enabled, you can access the pprof interface by navigating to `https://localhost:8080/debug/pprof/` in your browser.

The following pprof routes are available:

- `/debug/pprof/cmdline`: Command line arguments used to start the process
- `/debug/pprof/profile`: CPU profile data (30-second sample by default)
- `/debug/pprof/symbol`: Symbol lookup for program counters
- `/debug/pprof/trace`: Execution trace data

## `graph`

The `/debug/graph` endpoint shows a graphical representation of the machine resources managed by the RDK.

To access this endpoint, visit `https://localhost:8080/debug/graph` on the machine.

### Layout Options

To view different [layouts](https://graphviz.org/docs/layouts/), use the `layout` query parameter:

The following example URL specifies the `circo` layout:

```txt
https://localhost:8080/debug/graph?layout=circo
```

Available layout options include:

- `dot` (default): Hierarchical layout
- `neato`: Spring model layout
- `fdp`: Force-directed layout
- `sfdp`: Multiscale version of fdp for large graphs
- `circo`: Circular layout
- `twopi`: Radial layout
- `osage`: Array-based layout
- `text`: raw [DOT](https://graphviz.org/doc/info/lang.html) text of the graph, for use with external tools

## Next Steps

{{< cards >}}
{{% card link="/manage/troubleshoot/troubleshoot/" %}}
{{% card link="/operate/reference/viam-server/manage-viam-server/" %}}
{{% card link="/dev/tools/common-errors/" %}}
{{< /cards >}}
