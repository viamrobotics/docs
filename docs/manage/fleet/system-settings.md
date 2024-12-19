---
linkTitle: "Configure machine settings"
title: "Configure machine operating system settings"
weight: 50
layout: "docs"
type: "docs"
description: "Configure network settings, operating system package updates and logging defaults."
---

The `viam-agent` configuration allows you to configure:

- [settings for package updates for the host operating system](#configure-os-package-updates)
- [networks a machine can connect to](#configure-networks)
- [parameters for operating system logging](#configure-operating-system-logging)

## Configure OS package updates

By default, the configuration in <FILE>/etc/apt/apt.conf.d/</FILE> determines the behavior for updating operating system packages.
To adjust these settings update the `"agent"` value in the machine's JSON configuration.

For complete reference information, see [viam-agent](/configure/agent/#agent-syscfg).

### Automatically upgrade all packages

When set, `viam-agent` will install the `unattended-upgrades` package and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE> with an Origins-Pattern list generated automatically from configured repositories on the system.
Custom repos installed on the system at the time the setting is enabled will be included.

To set automatic upgrades for all packages, add the `upgrades` field to the `agent-syscfg`'s `attributes` object as following.
You may need to add the `agent-syscfg` object to the `agent` object if it doesn't already exist.


```json
"agent": {
    "agent-syscfg": {
        "release_channel": "stable",
        "attributes": {
            "upgrades": {
                "type": "all"
            }
        }
    }
}
```

### Automatically upgrade security packages

When set, `viam-agent` will install the `unattended-upgrades` package and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE> with an Origins-Pattern list generated automatically from configured repositories on the system.
Custom repos installed on the system at the time the setting is enabled will be included.

To set automatic upgrades for packages containing `"security"` in their codename (for example `bookworm-security`), add the `upgrades` field to the `agent-syscfg`'s `attributes` object as following.
You may need to add the `agent-syscfg` object to the `agent` object if it doesn't already exist.

```json
"agent": {
    "agent-syscfg": {
        "release_channel": "stable",
        "attributes": {
            "upgrades": {
                "type": "security"
            }
        }
    }
}
```

### Disable automatic upgrades

When set, `viam-agent` will install the `unattended-upgrades` package and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE> with an Origins-Pattern list generated automatically from configured repositories on the system.
Custom repos installed on the system at the time the setting is enabled will be included.

To set automatic upgrades, add the `upgrades` field to the `agent-syscfg`'s `attributes` object.
You may need to add the `agent-syscfg` object to the `agent` object if it doesn't already exist.

```json
"agent": {
    "agent-syscfg": {
        "release_channel": "stable",
        "attributes": {
            "upgrades": {
                "type": "disabled"
            }
        }
    }
}
```

## Configure networks

By default, your machine can connect to networks added at the operating system level, for example, directly in NetworkManager.

For an already-online device, you can add new WiFi networks by updating the `"agent"` value in the machine's JSON configuration.
This is primarily useful for a machine that moves between different networks, so the machine can automatically connect when moved between locations.

To add networks, add the `networks` field to the `agent-provisioning`'s `attributes` object and set `"roaming_mode": true`.
You may need to add the `agent-provisioning` object to the `agent` object if it doesn't already exist.

{{< alert title="Note" color="note" >}}
If you are using the Viam app to add networks to a machine’s configuration, the machine will need to be connected to the internet to retrieve the configuration information containing the network credentials before it can use them.
{{< /alert >}}

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`.
`viam-agent` will try to connect to `fallbackNetOne` first, since its priority is highest.
If the `fallbackNetOne` is not available or the machine can connect but internet is not available, `viam-agent` will then attempt to connect to `fallbackNetTwo`.

```json
"agent": {
    "agent-provisioning": {
        ...
        "attributes": {
            "roaming_mode": true,
            "networks": [
                {
                "type": "wifi",
                "ssid": "fallbackNetOne",
                "psk": "myFirstPassword",
                "priority": 30
                },
                {
                "type": "wifi",
                "ssid": "fallbackNetTwo",
                "psk": "mySecondPassword",
                "priority": 10
                }
            ]
        }
    }
}
```

For complete reference information, see [viam-agent](/configure/agent/#networks).

## Configure operating system logging

By default, the operating system defaults determine the disk space that `journald` uses to persist logs.
To adjust these settings update the `"agent"` value in the machine's JSON configuration.

For complete reference information, see [viam-agent](/configure/agent/#agent-syscfg).

### Set the maximum disk space

To set the maximum disk space `journald` will use to persist logs, add the `system_max_use` field to the `agent-syscfg`'s `attributes` object.
You may need to add the `agent-syscfg` object to the `agent` object if it doesn't already exist.

The configured values will take precedence over operating system defaults.

```json
"agent": {
    "agent-syscfg": {
        "release_channel": "stable",
        "attributes": {
            "logging": {
                "system_max_use": "512M"
            }
        }
    }
}
```

### Set the runtime space limit space

To set the temporary space limit for logs, add the `runtime_max_use` field to the `agent-syscfg`'s `attributes` object.
You may need to add the `agent-syscfg` object to the `agent` object if it doesn't already exist.

The configured values will take precedence over operating system defaults.

```json
"agent": {
    "agent-syscfg": {
        "release_channel": "stable",
        "attributes": {
            "logging": {
                "runtime_max_use": "512M"
            }
        }
    }
}
```

### Use the default operating system settings

This configuration does not modify the OS-level logging configuration.
The operating system defaults will be used:

```json
"agent": {
    "agent-syscfg": {
        "release_channel": "stable",
        "attributes": {
            "logging": {
                "disable": true
            }
        }
    }
}
```
