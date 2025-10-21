---
linkTitle: "Troubleshoot problems"
title: "Troubleshoot problems"
weight: 35
layout: "docs"
type: "docs"
description: "A guide to troubleshooting a Viam-based machine or system of machines with fixes to common problems."
date: "2025-01-07"
# updated: ""  # When the content was last entirely checked
aliases:
  - /appendix/troubleshooting/
---

If your machine is not working as expected, there are several steps you can take for debugging.
Start by checking the machine logs.
If that doesn't help, you can enable debug logs or `ssh` into the machine.

For common errors see [Common Errors](/dev/tools/common-errors/).

## Check logs

### Machine shows as offline

If your machine shows as offline on Viam, restart `viam-server` by running the command to start `viam-server` and adding the `-debug` option.

To do this, you will need to know if you installed `viam-server` with `viam-agent` (most common) or manually.
You can check this by seeing if `viam-agent` is running.
Run the following command:

```sh {class="command-line" data-prompt="$" data-output="2"}
ps aux | grep viam-agent
root      566431  0.5  0.2 1247148 20336 ?       Ssl  11:24   0:00 /opt/viam/bin/viam-agent --config /etc/viam.json
```

If you see a process running viam-agent, then you used `viam-agent` to install `viam-server`.
If not follow the steps for the standalone version.

{{< tabs >}}
{{% tab name="Installed with viam-agent" %}}

On Linux, you can query your logs with `journalctl`:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
sudo journalctl --unit=viam-agent
```

Alternatively you can restart `viam-server` manually and write logs to a log file:

1. First check where the `viam-server` binary is and where the machine cloud credentials file for your machine is:

   ```sh {class="command-line" data-prompt="$" data-output="2"}
   ps aux | grep viam-server
   root      566219 83.6  1.1 1966984 88896 ?       Sl   11:17   0:02 /opt/viam/bin/viam-server -config /etc/viam.json
   ```

2. Stop `viam-agent`:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   sudo systemctl stop viam-agent
   ```

3. Then run `viam-server` with the `-debug` option and pass in your machine cloud credentials file:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   /opt/viam/bin/viam-server -debug -config /etc/viam.json -log-file logs.txt
   ```

4. Then check the logs file <FILE>logs.txt</FILE>.

{{% /tab %}}
{{% tab name="Manual" %}}

{{< tabs >}}
{{% tab name="Linux" %}}

On Linux, you can query your logs with `journalctl`:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
sudo journalctl --unit=viam-server
```

Alternatively you can restart `viam-server` and write logs to a log file by stopping the running `viam-server` instance, and restarting it with the `-logfile` option:

1. First check where the `viam-server` binary is and where the machine cloud credentials file for your machine is:

   ```sh {class="command-line" data-prompt="$" data-output="2"}
   ps aux | grep viam-server
   root       865  1.6  0.2  11612  2428 ?        Ssl  11:42   0:56 /usr/local/bin/viam-server -config /etc/viam.json
   ```

1. Stop the system service running `viam-server`:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   sudo systemctl stop viam-server
   ```

1. Then run `viam-server` with the `-debug` and `-log-file` options and pass in your machine cloud credentials file:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   sudo /usr/local/bin/viam-server -debug -config /etc/viam.json -log-file logs.txt
   ```

1. Then check the logs file <FILE>logs.txt</FILE>.

{{% /tab %}}
{{% tab name="macOS" %}}

By default, `viam-server` writes logs to STDOUT and does not store them in a file on your machine.
If you want to store your logs in a file, stop the running `viam-server` instance, and restart it with the `-logfile` option.

1. First check where the `viam-server` binary is and where the machine cloud credentials file for your machine is:

   ```sh {class="command-line" data-prompt="$" data-output="2-3"}
   ps aux | grep viam-server
   naomi             8738   1.1  0.3 412233296  50720 s000  S+    5:24pm   0:00.40 viam-server -config /Users/naomi/Downloads/viam-mac-main.json
   ```

1. Kill the running `viam-server` instance.
1. Then run `viam-server` with the `-debug` and `-log-file` options and pass in your machine cloud credentials file:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   viam-server -config ~/Downloads/viam.json -debug -log-file logs.txt
   ```

1. Then check the logs file <FILE>logs.txt</FILE>.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
Be aware that while your machine is not able to connect to Viam, any changes to the machine's configuration that you make in the web UI will not reach your machine.
{{< /alert >}}

### Machine shows as online

#### Check for errors on the CONFIGURE page

Go to your machine's **CONFIGURE** page and check whether any configured components have a red exclamation symbol on their configuration card.
If so click on the symbol or expand the **ERROR LOGS** panel.
The expanded panel shows you errors produced by that resource.

#### Check logs on the LOGS tab

If your machine shows as online, go to the **LOGS** tab and check for errors or other information relevant to the issue.

{{<gif webm_src="/fleet/log-filtering.webm" mp4_src="/fleet/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can filter your logs by keyword, log levels and time.
You can use a regular expression as your keyword.

The default log level for `viam-server` and any running resources is `Info`.
If you are not seeing helpful logs, you can try changing the log level to `Debug`.

You can enable debug logs for all resources on a machine by adding `"debug": true` to the machine's JSON configuration:

```json
{
  "debug": true,
  "components": [{ ... }]
}
```

If this produces too many logs, you can instead **enable debug logs** for individual resources using the **...** menu on each resource.
You can also set the log level by configuring the `log` attribute in the machine configuration to match on patterns that capture the resources you are interested in.
For example:

```json
"components": [ ... ]
"log": [
    {
    "pattern": "rdk.components.arm",
    "level": "debug",
    }, {
    "pattern": "rdk.services.*",
    "level": "debug",
    }, {
    "pattern": "<module-name>",
    "level": "debug",
    }
]
```

For more information on setting log levels see, [Logging](/operate/reference/viam-server/#logging).

You may also find that not all logs you are expecting are displayed.
By default, `viam-server` deduplicates log messages that are deemed noisy.
To disable this behavior, see [Disable log deduplication](/operate/reference/viam-server/).

To access logs from the commandline, use [`viam machines logs`](/dev/tools/cli/#machines-alias-robots-and-machine) on the command line or the [Machines API](/dev/reference/apis/robot/).

### Advanced debugging for Go modules

If you have a Go module that doesn't shut down properly or hangs during operation, you can get more information by sending a SIGQUIT signal to the process.
Run the following command, replacing `<PID>` with your module's process identifier:

```sh {class="command-line" data-prompt="$"}
kill -3 <PID>
```

The process will dump a stack trace, visible in the `viam-server` logs, that shows:

- All currently running goroutines and their states
- Where execution is blocked or deadlocked
- Internal state information that might not appear in regular logs

{{% hiddencontent %}}

### Verify module startup completion

To verify if a module has successfully started, check the machine logs for specific startup messages:

1. Go to your machine's **LOGS** tab.

1. Look for log messages related to your module.
1. You can filter the logs by typing the module name in the search box to focus only on messages related to your specific module.
   When a module starts successfully, you'll see a sequence of log messages similar to:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   info rdk.module.manager           module/manager.go:XXX        Starting up module         module <module-name>
   info rdk.module.manager           module/manager.go:XXX        Module successfully added  module <module-name>
   info rdk.modmanager               modmanager/manager.go:xxx    Modules successfully added modules [<module-name>]
   info rdk.resource_manager         impl/resource_manager.go:xxx Now configuring resource   resource <api-triplet>/<model-name>
   info rdk.modmanager.<module-name> modmanager/manager.go:xxx    Adding resource to module  resource <model-name> module <module-name>
   ```

1. If you don't see a "successfully added" message or "adding resource to module," look for error messages that might indicate why the module failed to start completely.

{{% /hiddencontent %}}

## Capture machine telemetry data

Some issues are due to overall system health.
To rule out machine health as the root cause of your issues, [add a machine telemetry sensor](/manage/troubleshoot/alert/#add-performance-sensor) and [capture machine telemetry data with the data management service](/manage/troubleshoot/alert/#configure-data-management).

## Use `viam-server` debug endpoints

You can use [`pprof`](https://pkg.go.dev/net/http/pprof) to:

- diagnose performance bottlenecks
- investigate memory leaks
- understand resource usage patterns
- troubleshoot high CPU or memory usage

To enable the pprof endpoints, set `enable_web_profile` to `true` in your machine configuration:

```json
{
  "components": [...],
  "services": [...],
  "enable_web_profile": true
}
```

For more information on advanced debugging endpoints, see [Advanced debug endpoints](/operate/reference/viam-server/debug-endpoints/).

## Remote shell on the machine

To remotely access your machine from your terminal:

1. Add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json) to your machine.
1. Once you have added the fragment, you can use the [Viam CLI](/dev/tools/cli/) to open a shell on the machine.

   ```sh {class="command-line" data-prompt="$" data-output="2-10"}
   viam machines part shell --organization=<org name> --location=<location name> --machine=<machine id>
   ```

1. You can [access the local log file](/operate/reference/viam-server/manage-viam-server/#view-viam-server-logs) on your machine if needed.

1. If you need to copy files from your machine, use the [`viam machine part cp`](/dev/tools/cli/#machines-alias-robots-and-machine) command.

## Restart your machine

1. Navigate to your machine's page.
1. Select the part status dropdown to the right of your machine's name on the top of the page.
   {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="machine cloud credentials button on the machine part info dropdown" class="shadow" >}}
1. If you installed `viam-server` with `viam-agent` you will see a **Restart** button. Click it.
   If you do not see the **Restart** button, click the **...** menu on the right side of the machine part's card, and select **Restart part**.
   If restarting the machine part does not resolve the issue, ssh into the machine and [stop and restart viam-server manually](/operate/reference/viam-server/manage-viam-server/#run-viam-server).

It takes a few minutes for `viam-server` to shut down and restart.

## Revert to earlier configuration

Viam keeps a record of your configuration changes, allowing you to revert to earlier configurations if needed.
To see the history of the configuration of a machine part, click on **History** on the **CONFIGURE** tab.

{{<imgproc src="build/configure/history.png" resize="800x" declaredimensions=true alt="Configuration history for a machine part" class="shadow">}}

To restore to an earlier version of your configuration, click the **Restore version** button next to the desired configuration.

## Share a location with Viam support

If you have additional questions on debugging your machine, reach out to us on our [Community Discord](https://discord.gg/viam).
Please post the error message you received along with the steps you took that caused the issue and we'll see if we can help.

If you request support, you may be asked to share your location with the Viam Support team.
To do so, navigate to the location you need support with and click, **Add Viam support**.

Once you have received support, you can remove Viam Support from your location by clicking **Remove Viam support**.
