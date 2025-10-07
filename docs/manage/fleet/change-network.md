---
title: "Connect a machine to a new network"
linkTitle: "Connect to new network"
weight: 55
type: "docs"
description: "Connect a machine to a new WiFi network."
date: "2025-10-07"
---

This page will guide you to connect your machine to a new WiFi network.

## Prerequisites

Your machine must have `viam-agent` installed to be able to configure network settings.

## Connect to a different WiFi network

As your machine boots, `viam-agent` checks for known networks, if none can be found, `viam-agent` automatically enters provisioning mode.

Follow the instructions to [complete end-user setup for a machine](/manage/fleet/provision/end-user-setup/) and configure the new network settings.

## Force provisioning mode

If you want to change the WiFi network or the network credentials on a device that is already setup and can still connect to the current network, you can enter provisioning using the force provisioning mode.

If you can manually `SSH` into a machine you can follow these steps:

1. Add the [ViamShellDanger fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json).
   The `ViamShellDanger` fragment contains the latest version of the shell service, which you must add to your machine before you can use the `viam machines part shell` command.

1. Open a shell on your machine:

   ```sh {class="command-line" data-prompt="$" data-output="2-10"}
   viam machines part shell --part <PART-ID>
   ```

1. On the machine, create an empty file at <FILE>/opt/viam/etc/force_provisioning_mode</FILE>:

   ```sh {class="command-line" data-prompt="$" data-output="3-10"}
   touch /opt/viam/etc/force_provisioning_mode
   ```

1. The machine will immediately enter provisioning mode until the machine receives the new credentials or the `retry_connection_timeout_minutes` limit, by default 10 minutes, expires.

If you created a provisioning app, program it to add an empty file at <FILE>/opt/viam/etc/force_provisioning_mode</FILE>.

Follow the instructions to [complete end-user setup for a machine](/manage/fleet/provision/end-user-setup/) and configure the new network settings.

## Connect to multiple networks

If your machine frequently moves between different WiFi networks, you can [add the credentials for additional networks in the machine settings](/manage/fleet/system-settings/#configure-networks).
Your machine must still be internet-connected for this configuration to take effect.
