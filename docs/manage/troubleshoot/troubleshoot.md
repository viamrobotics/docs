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
Start by [checking the machine logs].
If that doesn't help, you can enable debug logs or `ssh` into the machine.

For common errors see [Common Errors](/dev/tools/common-errors/).

## Check logs

### Check for errors on the CONFIGURE page

Go to your machine's **CONFIGURE** page and check whether any configured components have a red exclamation symbol on their configuration card.
If so click on the symbol or expand the **ERROR LOGS** panel.
The expanded panel shows you errors produced by that resource.

### Check logs on the LOGS tab

Go to the **LOGS** tab and check for errors or other information relevant to the issue.

{{<gif webm_src="/fleet/log-filtering.webm" mp4_src="/fleet/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can filter your logs by keyword, log levels and time.

The default log level for `viam-server` and any running resources is `"Info"`.
If you are not seeing helpful logs, you can try changing the log level to `"Debug"`.

To enable debug logs for all resources on a machine add `"debug": true` to the machine's JSON configuration:

```json
{
  "debug": true,
  "components": [{ ... }]
}
```

If this produces too many logs, you can instead set the log level to debug for individual resources or by matching on a pattern that captures the resources you are interested in.
For example:

```json
"log": [
    {
    "pattern": "rdk.components.arm",
    "level": "debug",
    },{
    "pattern": "rdk.services.*",
    "level": "debug",
    }
]
```

For more information on setting log levels see, [Logging](/manage/troubleshoot/troubleshoot/#check-logs).

You may also find that not all logs you are expecting are displayed.
By default, `viam-server` deduplicates log messages that are deemed noisy.
To disable this behavior, see [Disable log deduplication](/operate/reference/viam-server/).

To access logs from the commandline, use [`viam machines logs`](/dev/tools/cli/#machines-alias-robots) on the command line or the [Machines API](/dev/reference/apis/robot/).

## Remote shell on the machine

To remotely access your machine from your terminal, add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json) to your machine.

Once you have added the fragment, you can use the [Viam CLI](/dev/tools/cli/) to open a shell on the machine.

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam machines part shell --organization=<org name> --location=<location name> --machine=<machine id>
```

You can [access the local log file](/operate/reference/viam-server/manage-viam-server/#view-viam-server-logs) on your machine if needed.

If you need to copy files from your machine, use the [`viam machine part cp`](/dev/tools/cli/#machines-alias-robots) command.

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
