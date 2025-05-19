---
title: "Debug Endpoints"
linkTitle: "Debug Endpoints"
weight: 130
type: "docs"
description: "Advanced debugging endpoints available in viam-server for troubleshooting and development."
date: "2025-05-19"
---

The RDK (Robot Development Kit) that powers `viam-server` includes several debug endpoints that expose server internals. These endpoints can be helpful during development or when troubleshooting complex issues.

## `/debug/graph`

The `/debug/graph` endpoint shows a graphical representation of the machine resources managed by the RDK. The graph is created using [graphviz](https://graphviz.org/).

You can access this endpoint by navigating to `https://localhost:8080/debug/graph` in your browser when connected to a machine running `viam-server`.

### Layout Options

You can specify different [layouts](https://graphviz.org/docs/layouts/) by passing in the query parameter `?layout=LAYOUT`. The default and best supported layout is `dot`.

For example:
```
https://localhost:8080/debug/graph?layout=circo
```

Available layout options include:
- `dot` (default) - Hierarchical layout
- `neato` - Spring model layout
- `fdp` - Force-directed layout
- `sfdp` - Multiscale version of fdp for large graphs
- `circo` - Circular layout
- `twopi` - Radial layout
- `osage` - Array-based layout

### Raw DOT Format

To get the raw [DOT](https://graphviz.org/doc/info/lang.html) text of the graph, pass in the query parameter `?layout=text`. This can be useful if you want to display the graph using a 3rd-party service or tool.

For example:
```
https://localhost:8080/debug/graph?layout=text
```

## `/debug/pprof/`

Setting `enable_web_profile` to `true` in your machine configuration will allow you to visualize runtime profiling data in the localhost browser via [pprof](https://pkg.go.dev/net/http/pprof).

### Configuration

To enable the pprof endpoints, add the following to your machine configuration:

{{< tabs >}}
{{% tab name="Builder UI" %}}

1. Navigate to the **CONFIGURE** tab of your machine in the Viam app
2. Click on the **...** menu next to your machine part in the left-hand menu
3. Select **Edit JSON**
4. Add the `enable_web_profile` field at the root level of your configuration:

```json
{
  "components": [...],
  "services": [...],
  "enable_web_profile": true
}
```

5. Click **Save**

{{% /tab %}}
{{% tab name="JSON" %}}

Add the `enable_web_profile` field at the root level of your configuration:

```json
{
  "components": [...],
  "services": [...],
  "enable_web_profile": true
}
```

{{% /tab %}}
{{< /tabs >}}

### Available Endpoints

Once enabled, you can access the pprof interface by navigating to `https://localhost:8080/debug/pprof/` in your browser.

The following pprof routes are available:

1. `/debug/pprof/cmdline` - Command line arguments used to start the process
2. `/debug/pprof/profile` - CPU profile data (30-second sample by default)
3. `/debug/pprof/symbol` - Symbol lookup for program counters
4. `/debug/pprof/trace` - Execution trace data

### Using pprof

The pprof tool provides valuable insights into your application's performance, including:

- CPU usage
- Memory allocation
- Goroutine blocking
- Execution tracing

This information can be particularly useful when:
- Diagnosing performance bottlenecks
- Investigating memory leaks
- Understanding resource usage patterns
- Troubleshooting high CPU or memory usage

For more detailed information on using pprof, refer to the [Go pprof documentation](https://pkg.go.dev/net/http/pprof).

## Security Considerations

{{< alert title="Caution" color="caution" >}}
The debug endpoints expose internal details about your machine's configuration and runtime behavior. Only enable these endpoints in development or controlled environments. In production environments, these endpoints should be disabled or properly secured.
{{< /alert >}}

When using these debug endpoints:

1. Ensure your machine is not exposed to untrusted networks
2. Disable the endpoints when not actively debugging
3. Consider using a secure tunnel or VPN when accessing these endpoints remotely
4. Be aware that the data exposed may include sensitive information about your machine's configuration

## Next Steps

{{< cards >}}
{{% card link="/manage/troubleshoot/troubleshoot/" %}}
{{% card link="/operate/reference/viam-server/manage-viam-server/" %}}
{{% card link="/dev/tools/common-errors/" %}}
{{< /cards >}}