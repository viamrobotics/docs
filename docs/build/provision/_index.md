---
title: "Provision Machines Using the Viam Agent"
linkTitle: "Provision Machines"
weight: 70
type: "docs"
description: "Flexibly provision new machines using the Viam Agent."
tags: ["fleet management", "viam-server", "viam-agent"]
# SME: James Otting
---

{{<gif webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with the Viam Agent" class="alignright" max-width="400px">}}

You can use the _Viam Agent_ to provision a machine as it first comes online with a pre-defined configuration.
This is useful when deploying a fleet of machines directly from the factory to a customer, or when bundling proprietary software on your Viam machine.
You can install the Viam Agent on your machines as part of your build process, and then have the Viam Agent perform the rest of the first-time setup for your machine once deployed to a customer, or to the field.

The Viam Agent:

- Automatically connects to a pre-configured WiFi network, or creates its own wireless hotspot if no pre-configured WiFi network is detected.
- Installs `viam-server` as a static binary, removing the need to perform any library linking or dependency installation during first-time setup.
  You can also use a custom build of `viam-server`, if needed.
- Provides automatic updates for `viam-server`, the agent itself, and any configured subsystems (such as the Agent Provisioning subsystem).
- Allows control of deployed software versions through the Viam app.

Consider a company that sells machines that monitor weather conditions on a maritime craft and provide navigation advice based on those readings.
Such a machine might use Viam to interface between a [sensor component](/components/sensor/) that takes weather measurements, and the [data management service](/data/) to regularly upload a stream of readings, for example.
However, to then parse the readings and provide tailored guidance to a ship's captain, the company has written their own proprietary application which includes live analytics and speech generation for conveying advice to the captain.

Using the Viam Agent, this company could ship their machines directly to customers and have each machine provision `viam-server` as it comes online for each user, eliminating factory setup time and allowing for tailored configurations per customer as needed.

The example video shows using the [Viam mobile application](/fleet/#the-viam-mobile-app) to connect to the Viam Agent on a newly-deployed machine and completing network setup.

## Install the Viam Agent

You can install the Viam Agent using either an existing machine's part ID and API key, or using an existing <file>/etc/viam.json</file> configuration file.

{{< alert title="Important" color="note" >}}
The Viam Agent supports the Linux `x86_64` and `arm64` architectures only.
Your machine must have `curl` available in order to install the Viam Agent.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Install using a part ID" %}}

If you want to install the Viam Agent on a machine that you have already configured in the Viam app, follow these steps:

1. Determine your machine's [Part ID](/build/program/apis/data-client/#find-part-id).
1. Determine your machine's [API key and API key ID](/build/program/#authenticate).
   If you haven't already, you can [use the CLI to create a new API key and API key ID](/fleet/cli/#create-an-organization-api-key).
1. Run the following command, replacing `<KEYID>`, `<KEY>`, and `<PARTID>` with your machine's values as determined from the steps above:

   ```sh {class="command-line" data-prompt="$"}
   sudo /bin/sh -c "VIAM_API_KEY_ID=<KEYID> VIAM_API_KEY=<KEY> VIAM_PART_ID=<PARTID>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
   ```

{{% /tab %}}
{{% tab name="Install using a configuration file" %}}

If you want to install the Viam Agent on a machine that you have not yet created in the Viam app, follow these steps:

1. Create a configuration file with the desired configuration for your machine. You can:

   - You can [create a new machine in the Viam app](/fleet/machines/#add-a-new-machine) and configure it as desired, then switch to **Raw JSON** mode and copy the configuration shown into a new file on your machine.
   - You can base your configuration on the [example configuration file](/internals/local-configuration-file/#example-json-configuration-file), and adjust as needed.
   - You can use an existing configuration file from a deployed machine, or adapt such a file as needed to fit the specifications of your new machine.

1. Place this file in the following location on the machine you wish to install the Viam Agent to: <file>/etc/viam.json</file>

1. Run the following command to install the Viam Agent on your machine:

   ```sh {class="command-line" data-prompt="$"}
   sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
   ```

{{% /tab %}}
{{< /tabs >}}

### Update the Viam Agent and `viam-server`

The Viam Agent automatically updates both itself and `viam-server` as new updates are released.
You can also configure update behavior for the Agent and `viam-server` using the [Viam app](https://app.viam.com/).

{{< alert title="Important" color="note" >}}
When the Viam Agent updates either itself or `viam-server`, you must restart these services in order to use the new version.
When you stop or restart the Viam Agent, the agent will stop or restart `viam-server` as well.
{{< /alert >}}

### Manage the Viam Agent

The Viam Agent is installed as a `systemd` service named `viam-agent`.

- To start the Viam Agent:

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl start viam-agent
  ```

- To stop the Viam Agent:

  {{< alert title="Alert" color="note" >}}
  When you stop the Viam Agent, the agent will stop `viam-server` as well.
  {{< /alert >}}

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl stop viam-agent
  ```

- To restart the Viam Agent:

  {{< alert title="Alert" color="note" >}}
  When you restart the Viam Agent, the agent will restart `viam-server` as well.
  {{< /alert >}}

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl restart viam-agent
  ```

- To completely uninstall the Viam Agent and `viam-server`, run the following command:

  ```sh {class="command-line" data-prompt="$"}
  sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/uninstall.sh)"
  ```

  This command uninstalls Viam Agent, `viam-server`, the machine configuration file (<file>/etc/viam.json</file>), and the provisioning configuration file (<file>/etc/viam-provisioning.json</file>).

## Provision a new machine

With the Viam Agent installed, your machine will either connect to a local WiFi network or will create its own WiFi hotspot, depending on your configuration.

- If you include a `viam-server` configuration file on your machine, located at <file>/etc/viam.json</file>, which includes a WiFi network and password to connect to, the Viam Agent will connect to the network automatically when in range.
- If you did not include this file, or the configured WiFi network is not available when your machine comes online, the Viam agent will create its own WiFi hotspot.

### Connect to an existing network

If you specify a WiFi network to connect to in your configuration file, the Viam Agent will automatically connect to that network when in range.

You can configure one or more WiFi networks to connect to in the `agent_config` configuration object in your `viam-server` configuration file.
For example, to configure SSIDs and passwords for two WiFi networks named `primaryNet` and `fallbackNet`, you can use the following configuration:

```json {class="line-numbers linkable-line-numbers"}
...
"agent_config": {
    "subsystems": {
      "agent-provisioning": {
        ...
        "attributes": {
          ...
          "networks": [
            {
              "type": "wifi",
              "ssid": "primaryNet",
              "psk": "myFirstPassword",
              "priority": 30
            },
            {
              "type": "wifi",
              "ssid": "fallbackNet",
              "psk": "mySecondPassword",
              "priority": 10
            }
          ]
        }
      }
    }
}
```

You can add this configuration to the <file>/etc/viam.json</file> configuration file you deploy to your machine, or from the **Config** tab in the [Viam app](https://app.viam.com/) for your machine, using **Raw JSON** mode.
The Viam Agent will attempt to connect to the `ssid` with the highest `priority` first.
If the highest-priority network is not available, it will then attempt to connect to the next-highest `priority` network, and so on until all configured networks have been tried.
If no configured WiFi network could be connected to, the Viam Agent will instead create its own WiFI hotspot, as described in the next section.

### Create a WiFi hotspot

If you did not include a `viam-server` configuration file on your machine, or none of the configured WiFi networks are available when your machine comes online, the Viam Agent will create its own WiFi hotspot that you can connect to in order to complete provisioning.

By default, the hotspot network is named `viam-setup-HOSTNAME`, where `HOSTNAME` is replaced with the hostname of your machine.
The WiFi password for this network is `viamsetup` by default.

You can customize these values in the `agent_config` configuration object in your `viam-server` configuration file.
For example, to set the hotspot password to `acme123`, you can use the following configuration:

```json {class="line-numbers linkable-line-numbers"}
...
"agent_config": {
    "subsystems": {
      "agent-provisioning": {
        ...
        "attributes": {
          "hotspot_password": "acme123"
          ...
        }
      }
    }
}
```

You can add this configuration to the <file>/etc/viam.json</file> configuration file you deploy to your machine, or from the **Config** tab in the [Viam app](https://app.viam.com/) for your machine, using **Raw JSON** mode.

If you did not initially provide a full `viam-server` configuration in either of these methods, you will be prompted to paste one in when you connect to the WiFi hotspot.
You can copy a configured machine's configuration by navigating to the [Viam app](https://app.viam.com/), selecting the **Setup** tab for your machine, and clicking the **Copy viam-server config** button.

## Use a pre-install script

When you install the Viam Agent, either manually using the commands above or automatically as part of your fleet's build and deploy process, you can choose to run a pre-install script to perform provisioning steps before deployment to the target machine.
For example, you could use the pre-install script to configure and deploy to an SD card or other image file, which you can then use as part of your fleet deployment process.
You can also use this method to generate a local tarball containing the configured deployment, which you could then deploy later, or through a different medium (such as automation, or as the basis for further customer-specific customization).

## Use a provisioning configuration file

When you install the Viam Agent, either manually using the commands above or automatically as part of your fleet's build and deploy process, you can provide a provisioning configuration file to pre-configure how your machine behaves when it first comes online.

To provision your machine, create a <file>/etc/viam-provisioning.json</file> configuration file, resembling the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "Skywalker",
  "model": "C-3PO",
  "fragment_id": "2567c87d-7aef-41bc-b82c-d363f9874663",
  "disable_dns_redirect": true,
  "hotspot_prefix": "skywalker-setup",
  "hotspot_password": "skywalker123"
}
```

This file configures some basic metadata, specifies a [fragment](/fleet/configure-a-fleet/) to use to configure the machine, and provides the WiFi network name and password to allow your machine to connect automatically on startup.

## Use the Viam mobile app

You can also use the [Viam mobile application](/fleet/#the-viam-mobile-app), available for download from the [Apple](https://apps.apple.com/us/app/viam-robotics/id6451424162) and [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US) app stores, to connect to the Viam Agent on deployed machines.

Once you are logged in using the Viam mobile app, select your organization, then location, then tap **Add new smart machine** and follow the instructions in the mobile app.
