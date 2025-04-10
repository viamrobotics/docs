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

If your machine shows as offline in the Viam app, restart `viam-server` by running the command to start `viam-server` and adding the `-debug` option.

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

1. First check where the `viam-server` binary is and where the config for your machine is:

   ```sh {class="command-line" data-prompt="$" data-output="2"}
   ps aux | grep viam-server
   root      566219 83.6  1.1 1966984 88896 ?       Sl   11:17   0:02 /opt/viam/bin/viam-server -config /etc/viam.json
   ```

2. Stop `viam-agent`:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   sudo systemctl stop viam-agent
   ```

3. Then run `viam-server` with the `-debug` option and pass in your configuration file:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   /opt/viam/bin/viam-server -debug -config /etc/viam.json -log-file logs.txt
   ```

4. Then check the logs file <FILE>logs.txt</FILE>.

{{% /tab %}}
{{% tab name="Manual" %}}

{{< tabs >}}
{{% tab name="Linux" %}}

1. First check where the `viam-server` binary is and where the config for your machine is:

   ```sh {class="command-line" data-prompt="$" data-output="2"}
   ps aux | grep viam-server
   root       865  1.6  0.2  11612  2428 ?        Ssl  11:42   0:56 /usr/local/bin/viam-server -config /etc/viam.json
   ```

2. Stop the system service running `viam-server`:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   sudo systemctl stop viam-server
   ```

3. Then run `viam-server` with the `-debug` option and pass in your configuration file:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   /usr/local/bin/viam-server -debug -config /etc/viam.json -log-file logs.txt
   ```

4. Then check the logs file <FILE>logs.txt</FILE>.

{{% /tab %}}
{{% tab name="macOS" %}}

1. Kill the running `viam-server` instance.
2. Then run `viam-server` with the `-debug` option and pass in your configuration file:

   ```sh {class="command-line" data-prompt="$" data-output=""}
   viam-server -config ~/Downloads/viam.json -debug
   ```

   You can check the exact command by consulting the setup instructions for your machine in the Viam app.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
Be aware that while your machine is not able to connect to the Viam app, any changes to the machine's configuration that you make in the Viam app will not reach your machine.
{{< /alert >}}

### Check for errors on the CONFIGURE page

Go to your machine's **CONFIGURE** page and check whether any configured components have a red exclamation symbol on their configuration card.
If so click on the symbol or expand the **ERROR LOGS** panel.
The expanded panel shows you errors produced by that resource.

### Check logs on the LOGS tab

If your machine shows as online in the Viam app, go to the **LOGS** tab and check for errors or other information relevant to the issue.

{{<gif webm_src="/fleet/log-filtering.webm" mp4_src="/fleet/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can filter your logs by keyword, log levels and time.

The default log level for `viam-server` and any running resources is `"Info"`.
If you are not seeing helpful logs, you can try changing the log level to `"Debug"`.

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

To access logs from the commandline, use [`viam machines logs`](/dev/tools/cli/#machines-alias-robots) on the command line or the [Machines API](/dev/reference/apis/robot/).

## Remote shell on the machine

To remotely access your machine from your terminal:

1. Add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json) to your machine.
1. Once you have added the fragment, you can use the [Viam CLI](/dev/tools/cli/) to open a shell on the machine.

   ```sh {class="command-line" data-prompt="$" data-output="2-10"}
   viam machines part shell --organization=<org name> --location=<location name> --machine=<machine id>
   ```

1. You can [access the local log file](/operate/reference/viam-server/manage-viam-server/#view-viam-server-logs) on your machine if needed.

1. If you need to copy files from your machine, use the [`viam machine part cp`](/dev/tools/cli/#machines-alias-robots) command.

## Restart your machine

1. Navigate to the app's **CONFIGURE** tab in **Builder** mode.
1. Click the **...** menu on the right side of the machine part's card, and select **Restart part**.

It takes a few minutes for the server to shut down and restart.

## Revert to earlier configuration

The Viam app keeps a record of your configuration changes, allowing you to revert to earlier configurations if needed.
To see the history of the configuration of a machine part, click on **History** on the **CONFIGURE** tab.

{{<imgproc src="build/configure/history.png" resize="800x" declaredimensions=true alt="Configuration history for a machine part" class="shadow">}}

To restore to an earlier version of your configuration, click the **Restore version** button next to the desired configuration.

## Share a location with Viam support

If you have additional questions on debugging your machine, reach out to us on our [Community Discord](https://discord.gg/viam).
Please post the error message you received along with the steps you took that caused the issue and we'll see if we can help.

If you request support, you may be asked to share your location with the Viam Support team.
To do so, navigate to the location you need support with and click, **Add Viam support**.

Once you have received support, you can remove Viam Support from your location by clicking **Remove Viam support**.
