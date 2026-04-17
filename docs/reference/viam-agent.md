---
linkTitle: "viam-agent"
title: "viam-agent reference"
weight: 5
layout: "docs"
type: "docs"
description: "Reference for viam-agent: installation, subsystems, version control, advanced settings, system configuration, and network management."
date: "2026-04-17"
aliases:
  - /manage/reference/viam-agent/
  - /manage/reference/viam-agent/manage-viam-agent/
  - /configure/agent/
  - /dev/reference/glossary/viam-agent/
---

`viam-agent` is the on-device service manager for Viam. It runs as a systemd service on Linux machines and handles four responsibilities:

- **Managing `viam-server`**: downloading, installing, starting, and restarting `viam-server` as versions change.
- **Provisioning**: creating a WiFi hotspot or Bluetooth service on first boot so end users can provide network credentials and connect the machine to Viam Cloud.
- **System configuration**: managing OS-level settings like automatic package updates and log forwarding.
- **Network management**: configuring WiFi networks, monitoring connectivity, and re-entering provisioning mode when connectivity is lost.

`viam-agent` polls Viam Cloud on a regular interval (minimum 5 seconds, configurable by the cloud) for configuration updates. When the cloud sends new settings, `viam-agent` applies them locally.

## Installation

The Viam app generates a machine-specific install command on each machine's setup page. The command downloads `viam-agent`, registers the machine with Viam Cloud, and configures the systemd service:

```sh {class="command-line" data-prompt="$"}
sudo /bin/sh -c "VIAM_API_KEY_ID=<KEYID> VIAM_API_KEY=<KEY> VIAM_PART_ID=<PARTID>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

Copy this command from the **CONNECT** tab on your machine's page in the Viam app. Do not construct it by hand.

For manufacturing and fleet provisioning (installing onto device images before first boot), use the preinstall script instead. See [Provision devices](/fleet/provision-devices/) for the full workflow.

## How updates work

When the cloud sends a new version for `viam-agent` or `viam-server`, the agent:

1. Downloads the new binary to a local cache directory.
2. Validates the download against the expected SHA-256 checksum.
3. Swaps the running binary using an atomic symlink operation. The old binary remains cached for 30 days.

If power is lost during download, `viam-agent` discards the incomplete file and re-downloads on the next check cycle. The currently running binary is never interrupted during the download or validation steps.

`viam-agent` does not automatically roll back to a previous version if the new version fails to start. If a deployed version crashes on startup, `viam-agent` will keep retrying that version until you change the cloud config to pin an older one.

## Version control

Control which versions of `viam-agent` and `viam-server` run on the machine.

In the machine settings card in the Viam app, open **Settings** and expand **Software Updates**:

- **Agent version**: choose `stable` (the default, tracks the latest stable release), a specific semver release such as `5.6.77`, or a URL to a custom binary.
- **viam-server version**: same options as agent.

When you change a version, the cloud sends an update instruction to `viam-agent` on the machine's next check cycle. The agent downloads and installs the new binary using the atomic swap mechanism described above.

Changing the `viam-server` version takes effect on the next maintenance window (if configured) or immediately. Changing the `viam-agent` version requires restarting `viam-agent` to take effect. See [Restart viam-agent](#restart-viam-agent).

To control when updates are applied, configure a [maintenance window](/fleet/manage-versions/#maintenance-windows). To stage rollouts across a fleet, use [fragment tags](/fleet/manage-versions/#staged-rollouts-with-fragment-tags).

## Advanced settings

In the machine settings card, open **Settings** and expand **Advanced**:

| Field                               | Type    | Default | Description                                                                                                                        |
| ----------------------------------- | ------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `debug`                             | boolean | `false` | Enable debug logging for `viam-agent`.                                                                                             |
| `wait_for_update_check`             | boolean | `false` | Wait for a network connection and update check before starting `viam-server`. Useful for ensuring the latest version runs on boot. |
| `disable_viam_server`               | boolean | `false` | Prevent `viam-agent` from starting `viam-server`. For development use.                                                             |
| `disable_network_configuration`     | boolean | `false` | Disable `viam-agent`'s network and hotspot management.                                                                             |
| `disable_system_configuration`      | boolean | `false` | Disable `viam-agent`'s system configuration management (OS updates, log forwarding).                                               |
| `viam_server_start_timeout_minutes` | integer | `10`    | Minutes to wait before restarting an unresponsive `viam-server`.                                                                   |
| `viam_server_env`                   | object  | `{}`    | Environment variables passed to `viam-server` and all modules.                                                                     |

## System configuration

In the machine settings card, open **Settings** and expand **System**:

### OS package updates

| Field                  | Type   | Default | Description                                                                                                                                                                                        |
| ---------------------- | ------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `os_auto_upgrade_type` | string | `""`    | Controls automatic OS package updates. Options: `"all"` (upgrade all packages), `"security"` (security updates only), `"disable"` (no automatic updates), `""` (do not manage, leave OS defaults). |

### Log forwarding

| Field                                        | Type    | Default | Description                                                                                                                                                                                                                                                                                                         |
| -------------------------------------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `forward_system_logs`                        | string  | `""`    | Forward operating system logs to Viam's cloud log viewer. Options: `"all"` (forward all system logs), a comma-separated list of service identifiers (forward only those services), or prefix a service with `-` to exclude it. For example, `"all,-gdm,-tailscaled"` forwards everything except gdm and tailscaled. |
| `logging_journald_system_max_use_megabytes`  | integer | `512`   | Maximum disk space for persistent system journal logs, in megabytes. Set to `-1` to disable the limit.                                                                                                                                                                                                              |
| `logging_journald_runtime_max_use_megabytes` | integer | `512`   | Maximum disk space for runtime (volatile) journal logs, in megabytes. Set to `-1` to disable the limit.                                                                                                                                                                                                             |
| `logging_journald_storage`                   | string  | `""`    | Controls journal log persistence. Options: `"volatile"` (RAM only, lost on reboot), `"persistent"` (written to disk), `"auto"` (persistent if `/var/log/journal` exists), `"none"` (disable journal logging). Empty string means do not manage this setting.                                                        |

## Additional networks {#additional_networks}

Add WiFi or wired networks that the machine can connect to. Each network has a name and connection settings you configure individually.

In the machine settings card, open **Settings** and expand **Known Networks**. Click **Add another network** and configure:

| Field               | Type    | Default  | Description                                                                                                                                              |
| ------------------- | ------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`              | string  |          | `"wifi"`, `"wired"`, or `"bluetooth"` (for Bluetooth tethering connections).                                                                             |
| `ssid`              | string  |          | The WiFi network name. Required for WiFi networks.                                                                                                       |
| `psk`               | string  |          | The WiFi password.                                                                                                                                       |
| `priority`          | integer | `0`      | Network selection priority. Higher values win. Set higher than the current network's priority if you want the machine to prefer this one.                |
| `interface`         | string  |          | The network interface to use (for example, `wlan0`, `eth0`). Leave empty to use the default.                                                             |
| `ipv4_address`      | string  | `"auto"` | Static IPv4 address in CIDR notation, or `"auto"` for DHCP.                                                                                              |
| `ipv4_gateway`      | string  |          | Gateway address for static IP configuration.                                                                                                             |
| `ipv4_dns`          | array   | `[]`     | DNS server addresses for static IP configuration.                                                                                                        |
| `ipv4_route_metric` | integer | `0`      | Route metric for this network. Lower values are preferred. When set to `0`, the OS applies its own defaults (typically 100 for wired, 600 for wireless). |

For provisioning-time network setup, add networks to the `additional_networks` section of the defaults file. See [Provision devices](/fleet/provision-devices/).

## Restart viam-agent

After changing the `viam-agent` version or modifying settings that require a restart, restart the service:

```sh {class="command-line" data-prompt="$"}
sudo systemctl restart viam-agent
```

To check whether `viam-agent` is running:

```sh {class="command-line" data-prompt="$"}
sudo systemctl status viam-agent
```

To view `viam-agent` logs:

```sh {class="command-line" data-prompt="$"}
sudo journalctl -u viam-agent -f
```

When you restart `viam-agent`, `viam-server` also restarts. Rebooting the machine has the same effect.

## Related pages

- [System settings](/fleet/system-settings/) for configuring these settings through the Viam app.
- [Provision devices](/fleet/provision-devices/) for the manufacturing-side provisioning workflow.
- [Manage versions and rollouts](/fleet/manage-versions/) for version pinning, maintenance windows, and staged rollouts.
- [Change network](/fleet/change-network/) for changing a deployed machine's WiFi.
