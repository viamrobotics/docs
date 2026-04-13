---
linkTitle: "System settings"
title: "System settings"
weight: 60
layout: "docs"
type: "docs"
description: "Configure network connections, OS updates, tunneling, TLS, and log forwarding for deployed machines."
---

Configure system-level settings for deployed machines. These settings are managed by `viam-agent` and configured in your machine's JSON configuration under the agent config section. You can configure them directly on a machine or deploy them fleet-wide through a fragment.

## Agent version control

Control which versions of `viam-agent` and `viam-server` run on the machine.

In the machine settings card, open **Settings** and expand **Software Updates**:

| Field         | Type   | Default    | Description                                                                                            |
| ------------- | ------ | ---------- | ------------------------------------------------------------------------------------------------------ |
| `agent`       | string | `"stable"` | Version of viam-agent. Options: a semver string (`"5.6.77"`), `"stable"`, or a URL to a custom binary. |
| `viam-server` | string | `"stable"` | Version of viam-server. Same options as agent.                                                         |

## Agent advanced settings

In the machine settings card, open **Settings** and expand **Advanced**:

| Field                               | Type    | Default | Description                                                                 |
| ----------------------------------- | ------- | ------- | --------------------------------------------------------------------------- |
| `debug`                             | boolean | `false` | Enable debug logging for viam-agent.                                        |
| `disable_network_configuration`     | boolean | `false` | Disable viam-agent's network and hotspot management.                        |
| `disable_system_configuration`      | boolean | `false` | Disable viam-agent's system configuration management.                       |
| `disable_viam_server`               | boolean | `false` | Prevent viam-agent from starting viam-server. For development use.          |
| `viam_server_env`                   | object  | `{}`    | Environment variables passed to viam-server and all modules.                |
| `viam_server_start_timeout_minutes` | integer | `10`    | Minutes to wait before restarting an unresponsive viam-server.              |
| `wait_for_update_check`             | boolean | `false` | Wait for a network connection and update check before starting viam-server. |

## Configure additional networks

Add WiFi or wired networks that the machine can connect to. Each network is a named entry with connection parameters.

In the machine settings card, open **Settings** and expand **Known Networks**. Click **Add another network** and configure:

| Field               | Type    | Default  | Description                                                                                |
| ------------------- | ------- | -------- | ------------------------------------------------------------------------------------------ |
| `type`              | string  | —        | **Required.** `"wifi"` or `"wired"`.                                                       |
| `ssid`              | string  | —        | WiFi network name. Only for WiFi networks.                                                 |
| `psk`               | string  | —        | Network password or pre-shared key.                                                        |
| `priority`          | integer | `0`      | Network selection priority. Higher values are preferred. Range: -999 to 999.               |
| `interface`         | string  | —        | Network interface name (for example, `"wlan0"`, `"eth0"`).                                 |
| `ipv4_address`      | string  | `"auto"` | Static IPv4 address in CIDR notation (for example, `"192.168.0.10/24"`).                   |
| `ipv4_dns`          | array   | `[]`     | DNS server addresses.                                                                      |
| `ipv4_gateway`      | string  | —        | IPv4 gateway address.                                                                      |
| `ipv4_route_metric` | integer | `0`      | Route metric. Lower values are preferred. `0` defaults to 100 for wired, 600 for wireless. |

## Configure tunneling

Allow secure port forwarding from a local machine to a remote machine through Viam's cloud connection. You must list allowed ports in the machine configuration.

```json
{
  "network": {
    "traffic_tunnel_endpoints": [
      {
        "port": 8080,
        "connection_timeout": "30s"
      }
    ]
  }
}
```

| Field                | Type    | Description                                                                           |
| -------------------- | ------- | ------------------------------------------------------------------------------------- |
| `port`               | integer | The port on the machine to expose for tunneling.                                      |
| `connection_timeout` | string  | Timeout for establishing the tunnel connection. Go duration format. Default: `"10s"`. |

To connect through the tunnel, use the CLI:

```sh {class="command-line" data-prompt="$"}
viam machines part tunnel --part=<part-id> --local-port=8080 --destination-port=8080
```

## Disable TLS

By default, `viam-server` uses TLS for all connections. To disable TLS (for development or isolated networks only):

```json
{
  "network": {
    "no_tls": true
  }
}
```

## Configure bind address and port

By default, `viam-server` listens on `localhost:8080`. To change the bind address:

```json
{
  "network": {
    "bind_address": "0.0.0.0:8081"
  }
}
```

## Configure OS package updates

Control automatic operating system package updates on the machine.

In the machine settings card, open **Settings** and expand **System**. Set `os_auto_upgrade_type`:

| Value        | Description                                                              |
| ------------ | ------------------------------------------------------------------------ |
| `"all"`      | Install all available OS package updates.                                |
| `"security"` | Install security updates only.                                           |
| `"disable"`  | Disable automatic OS updates.                                            |
| `""` (empty) | Do not change the system's current update settings. This is the default. |

## Configure OS log forwarding

Forward operating system logs from the machine to Viam's cloud log viewer.

In the machine settings card, open **Settings** and expand **System**:

| Field                                        | Type    | Default | Description                                                             |
| -------------------------------------------- | ------- | ------- | ----------------------------------------------------------------------- |
| `forward_system_logs`                        | string  | `""`    | Which system logs to forward. Empty string disables forwarding.         |
| `logging_journald_runtime_max_use_megabytes` | integer | `512`   | Maximum temporary log storage in MB. Set to `-1` to disable the limit.  |
| `logging_journald_system_max_use_megabytes`  | integer | `512`   | Maximum persistent log storage in MB. Set to `-1` to disable the limit. |

### Log forwarding filter syntax

The `forward_system_logs` field accepts:

- `"all"`: forward all system logs
- A comma-separated list of service identifiers: forward only those services (for example, `"kernel,NetworkManager,tailscaled"`)
- Prefix a service with `-` to exclude it: `"all,-gdm,-tailscaled"` forwards everything except gdm and tailscaled

## Verify settings changes

After updating system settings:

1. Click **Save** on the **CONFIGURE** tab.
1. Wait for the machine to sync the new configuration (up to one minute).
1. Check the **LOGS** tab for any errors related to the changed settings.
1. For network changes, verify the machine remains online in the fleet dashboard.

## Related pages

- [Change network](/fleet/change-network/) for changing a machine's WiFi after deployment
- [Provision devices](/fleet/provision-devices/) for configuring initial network settings during provisioning
