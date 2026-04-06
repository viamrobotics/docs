---
linkTitle: "Change network"
title: "Change a machine's network"
weight: 70
layout: "docs"
type: "docs"
description: "Connect a deployed machine to a different WiFi network."
---

Change the WiFi network on a machine that has already been provisioned and deployed. There are three approaches depending on your situation.

## Option 1: Move to a new WiFi network using provisioning mode

If the machine's current network is no longer available (for example, you moved the machine to a new facility), force the machine back into provisioning mode:

1. Connect to the machine with a shell (if possible):

   ```sh {class="command-line" data-prompt="$"}
   viam machines part shell --part=<part-id>
   ```

1. Create a file that forces provisioning mode on next boot:

   ```sh {class="command-line" data-prompt="$"}
   sudo touch /opt/viam/etc/force_provisioning_mode
   ```

1. Reboot the machine. On boot, `viam-agent` enters provisioning mode and creates a WiFi hotspot.

1. Follow the [end-user device setup](/fleet/end-user-setup/) instructions to connect the machine to the new network.

If you cannot shell into the machine, power cycle it. If the current network is truly unavailable, `viam-agent` enters provisioning mode automatically after the configured timeout (`retry_connection_timeout_minutes`, default 10 minutes).

## Option 2: Add a new network while keeping the current one

If the machine is still connected to its current network and you want to add a second network (for example, when moving between locations):

1. Add the new network credentials in the machine's system settings. See [configure additional networks](/fleet/system-settings/#configure-additional-networks).
1. Set the `priority` value higher than the current network if you want the machine to prefer the new one.
1. Save the configuration. The machine picks up the new network on its next config sync.

## Option 3: Pre-configure multiple networks during provisioning

If you know the machine will need to connect to multiple networks, add them to the `additional_networks` section of the `viam-defaults.json` file before provisioning. See [provision additional networks](/fleet/provision-devices/#provision-additional-networks).

## Verify the network change

After changing the network:

1. In the Viam app, navigate to the fleet dashboard or the machine's page.
1. Confirm the machine shows as **Live**.
1. If the machine does not come back online within a few minutes, it may not have connected to the new network. Power cycle the device to restart provisioning mode.
