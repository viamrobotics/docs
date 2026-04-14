---
linkTitle: "Troubleshoot problems"
title: "Troubleshoot problems"
weight: 40
layout: "docs"
type: "docs"
description: "Debug a misbehaving machine using logs, remote shell access, debug endpoints, and configuration history."
aliases:
  - /manage/troubleshoot/troubleshoot/
  - /appendix/troubleshooting/
  - /dev/tools/common-errors/
---

When a machine is not working as expected, follow this debugging workflow: check logs, enable debug logging if needed, access the machine remotely, and if necessary use advanced diagnostics.

For common errors and their solutions, see [Common Errors](/monitor/troubleshoot/).

## Check logs

### Machine shows as offline

If your machine shows as offline in the Viam app, you need to check logs on the machine itself.

First determine whether `viam-server` was installed with `viam-agent` (most common) or manually:

```sh {class="command-line" data-prompt="$" data-output="2"}
ps aux | grep viam-agent
root      566431  0.5  0.2 1247148 20336 ?       Ssl  11:24   0:00 /opt/viam/bin/viam-agent --config /etc/viam.json
```

If you see a `viam-agent` process, you used `viam-agent` to install.

{{< tabs >}}
{{% tab name="Installed with viam-agent" %}}

Query logs with `journalctl`:

```sh {class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-agent
```

Or restart `viam-server` manually with debug logging to a file:

1. Find the `viam-server` binary and config file paths:

   ```sh {class="command-line" data-prompt="$" data-output="2"}
   ps aux | grep viam-server
   root      566219 83.6  1.1 1966984 88896 ?       Sl   11:17   0:02 /opt/viam/bin/viam-server -config /etc/viam.json
   ```

1. Stop `viam-agent`:

   ```sh {class="command-line" data-prompt="$"}
   sudo systemctl stop viam-agent
   ```

1. Run `viam-server` with debug logging:

   ```sh {class="command-line" data-prompt="$"}
   /opt/viam/bin/viam-server -debug -config /etc/viam.json -log-file logs.txt
   ```

1. Check the log file for errors.

{{% /tab %}}
{{% tab name="Manual install (Linux)" %}}

Query logs with `journalctl`:

```sh {class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-server
```

Or restart with debug logging:

1. Stop the system service:

   ```sh {class="command-line" data-prompt="$"}
   sudo systemctl stop viam-server
   ```

1. Run with debug logging:

   ```sh {class="command-line" data-prompt="$"}
   sudo /usr/local/bin/viam-server -debug -config /etc/viam.json -log-file logs.txt
   ```

1. Check the log file for errors.

{{% /tab %}}
{{% tab name="Manual install (macOS)" %}}

By default, `viam-server` writes logs to STDOUT.
To capture logs to a file:

1. Stop the running `viam-server` instance.
1. Restart with debug logging:

   ```sh {class="command-line" data-prompt="$"}
   viam-server -config ~/Downloads/viam.json -debug -log-file logs.txt
   ```

1. Check the log file for errors.

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
While your machine cannot connect to Viam, configuration changes you make in the app will not reach the machine.
{{< /alert >}}

### Machine shows as online

#### Check for errors on the CONFIGURE page

Go to your machine's **CONFIGURE** page and look for a red exclamation icon on any resource card.
Click the icon or expand the **ERROR LOGS** panel to see resource-specific errors.

#### Check logs on the LOGS tab

Go to the **LOGS** tab and look for errors.

You can filter logs by:

- **Level**: Error, Warn, Info, Debug
- **Keyword**: full text search (supports regular expressions)
- **Time range**: set start and end times, or use live mode to stream logs in real time
- **Resource**: filter by a specific component or service name

The default log level is `Info`.
If you are not seeing helpful logs, enable debug logging.

#### Enable debug logging

**For all resources on the machine**, add `"debug": true` to the JSON configuration:

```json
{
  "debug": true,
  "components": [{ ... }]
}
```

**For individual resources**, click the **...** menu on the resource's configuration card and select **Enable debug logs**.

**For resources matching a pattern**, configure the `log` field in the machine configuration:

```json
"log": [
  {
    "pattern": "rdk.components.arm",
    "level": "debug"
  },
  {
    "pattern": "rdk.services.*",
    "level": "debug"
  }
]
```

For more on log configuration, see [Logging](/reference/).

By default, `viam-server` deduplicates log messages that repeat within a one-minute window.
To disable this, see [Disable log deduplication](/reference/).

#### Access logs from the command line

```sh {class="command-line" data-prompt="$"}
viam machines logs --machine <machine-name-or-id> --levels error,warn
```

Stream logs in real time:

```sh {class="command-line" data-prompt="$"}
viam machines part logs --part <part-name-or-id> --tail
```

Filter by keyword and time range:

```sh {class="command-line" data-prompt="$"}
viam machines logs --machine <machine-name-or-id> --keyword "motor" --start 2026-04-07T10:00:00Z --end 2026-04-07T11:00:00Z
```

## Remote shell access

Access a terminal on the machine without setting up SSH tunnels:

1. Add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json) to your machine.
1. Open a shell:

   ```sh {class="command-line" data-prompt="$"}
   viam machines part shell --part <part-name-or-id>
   ```

1. Copy files from the machine:

   ```sh {class="command-line" data-prompt="$"}
   viam machines part cp --part <part-name-or-id> -r machine:/path/to/files ~/Downloads/
   ```

1. Tunnel to a specific port on the machine:

   ```sh {class="command-line" data-prompt="$"}
   viam machines part tunnel --part <part-name-or-id> --local-port 8080 --destination-port 8080
   ```

## Debug endpoints

For performance issues, enable pprof profiling endpoints:

```json
{
  "components": [],
  "services": [],
  "enable_web_profile": true
}
```

This exposes endpoints for CPU profiling, memory allocation analysis, goroutine blocking analysis, and execution tracing.

The `/debug/graph` endpoint renders an SVG visualization of the machine's resource dependency graph.

For details, see [Debug Endpoints](/reference/).

## Diagnostics

### FTDC

FTDC (full-time diagnostic capture) continuously records machine metrics in a compressed binary format: resource counts, WebRTC connection stats, data manager upload stats, and more.

Download FTDC data from a machine:

```sh {class="command-line" data-prompt="$"}
viam machines part get-ftdc --part <part-name-or-id> ./diagnostics/
```

Parse and analyze FTDC data locally:

```sh {class="command-line" data-prompt="$"}
viam parse-ftdc --path ./diagnostics/ftdc-data
```

### Traces

If tracing is enabled in your machine configuration, you can download and analyze OpenTelemetry traces:

```sh {class="command-line" data-prompt="$"}
viam traces get-remote --part <part-name-or-id> ./traces/
```

Print traces to the console:

```sh {class="command-line" data-prompt="$"}
viam traces print-remote --part <part-name-or-id>
```

Import traces into an OTLP-compatible tool (such as Jaeger):

```sh {class="command-line" data-prompt="$"}
viam traces import-remote --part <part-name-or-id> --endpoint localhost:4317
```

## Restart a machine

1. Navigate to your machine's page.
1. Click the part status dropdown to the right of your machine's name.
1. If your machine was installed with `viam-agent`, click **Restart**.
   Both `viam-server` and `viam-agent` will restart.

   If you do not see a **Restart** button, click the **...** menu on the machine part card and select **Restart part**.

It takes a few minutes for `viam-server` to shut down and restart.

From the command line:

```sh {class="command-line" data-prompt="$"}
viam machines part restart --part <part-name-or-id>
```

## Revert to an earlier configuration

Viam keeps a record of your configuration changes.
To see the history, click **History** on the **CONFIGURE** tab.

To restore an earlier version, click the **Restore version** button next to the desired configuration.

## Advanced debugging for Go modules

If a Go module hangs or does not shut down properly, send a SIGQUIT signal to get a stack trace:

```sh {class="command-line" data-prompt="$"}
kill -3 <PID>
```

The process dumps a stack trace to the `viam-server` logs showing all goroutines and where execution is blocked.

## Get support

If you cannot resolve the issue, reach out on the [Community Discord](https://discord.gg/viam).
Post the error message along with what you were doing when it occurred.

If asked, you can share your location with the Viam Support team by navigating to your location and clicking **Add Viam support**.
Remove access after receiving support by clicking **Remove Viam support**.
