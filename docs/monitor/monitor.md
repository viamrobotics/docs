---
linkTitle: "Monitor machine status"
title: "Monitor machine status"
weight: 10
layout: "docs"
type: "docs"
description: "Check which machines are online, view part status, and inspect machine health across your fleet."
aliases:
  - /manage/troubleshoot/monitor/
---

Check the status of your machines from the Viam app, the mobile app, or the command line.

## Check fleet status

Navigate to the [**FLEET** page](https://app.viam.com/fleet/machines) and click the **machines** tab.
The machines table shows every machine in your organization with its current status:

- **Online** (green): the machine is connected and running.
- **Offline** (red): the machine is not connected. The table shows when it was last online.
- **Awaiting setup**: the machine has been created but has not yet connected to Viam.

You can also see the amount of binary and tabular data your fleet has synced in the last 48 hours from this dashboard.

## Inspect a specific machine

Click a machine name to open its page.
At the top of the page, the status indicator shows whether the machine is online or offline.

Click the **status** dropdown to see details about each {{< glossary_tooltip term_id="part" text="part" >}} of your machine:

- Operating system and architecture
- Host information
- `viam-server` version
- IP addresses
- Last online time (if offline) or remote address (if online)

## Check resource health

On a machine's **CONFIGURE** page, look for a red exclamation icon on any resource card.
Click the icon or expand the **ERROR LOGS** panel to see errors produced by that resource.

For more detailed debugging, see [Troubleshoot problems](/monitor/troubleshoot/).

## Test a machine remotely

On the [**CONTROL** tab](/monitor/default-interface/), you can remotely operate the machine and test each configured resource without writing code.

## Use the command line

Check machine status from the CLI:

```sh {class="command-line" data-prompt="$"}
viam machines status --machine <machine-name-or-id>
```

Check a specific part:

```sh {class="command-line" data-prompt="$"}
viam machines part status --part <part-name-or-id>
```

List all parts on a machine:

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine <machine-name-or-id>
```

Replace the placeholder values with your machine name or ID.
You can find the machine name on the machine's page in the Viam app.
To find the machine ID, click the **...** menu on the machine's page and select **Copy machine ID**.

## Set up offline alerts

To receive an email or webhook notification when a machine goes offline, configure a trigger.
See [Set up alerts](/monitor/alert/).

## Use the mobile app

The [Viam mobile app](/monitor/default-interface/#viam-mobile-app) shows machine status from your phone.
You can see which machines are online, view logs, and remotely operate components.

The mobile app is available on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).
