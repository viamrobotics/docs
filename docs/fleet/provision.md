---
title: "Provision machines using viam-agent"
linkTitle: "Provisioning Machines"
weight: 70
type: "docs"
description: "Flexibly provision new machines using viam-agent."
images: ["/platform/provisioning-demo.gif"]
videos: ["/platform/provisioning-demo.webm", "/platform/provisioning-demo.mp4"]
tags: ["fleet management", "viam-server", "viam-agent"]
# SMEs: James, Ale
aliases:
  - "/build/provision/"
  - "/fleet/provision/"
---

You can use Viam's software provisioning manager (`agent-provisioning`), to provision a machine as it first comes online with a pre-defined configuration.
This is useful when deploying a fleet of machines directly from the factory to a customer, or when bundling proprietary software on your Viam machine.

The provisioning subsystem is a feature of [`viam-agent`](/configure/agent/), which you can install as part of your build process.
`agent-provisioning` will then perform the rest of the first-time setup for your machine once an [end user sets up the machine](#how-an-end-user-would-use-it).

Consider a company that sells machines that monitor weather conditions on a maritime craft and provide navigation advice based on those readings.
Such a machine might use Viam to regularly capture and upload a stream of sensor readings, for example.
To parse the readings and provide tailored guidance to a ship's captain, the company writes their own proprietary application which includes live analytics and speech generation for conveying advice to the captain.

Using `agent-provisioning`, this company can ship their machines directly to customers with `viam-agent` installed.
When a customer sets up their machine, the provisioning subsystem installs `viam-server`.
By having the end customer set up the machine, the company:

- eliminates factory setup time
- allows for tailored configurations per customer as needed

{{< alert title="Support Notice" color="note" >}}

Provisioning works on Bullseye, Debian Bookworm or newer.
For Bullseye, the installation of `viam-agent` changes the network configuration to use NetworkManager.

{{< /alert >}}

## How an end user would use it

End users that receive a machine, use either a captive portal through a browser or a web or mobile app to complete the machine setup.

One option is to use the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app).
The Viam mobile app allows end users to create a new machine in the app, and `agent-provisioning` will then install `viam-server` and run it with a provided configuration.

To add your branding, you can build your own web or mobile app and use one of Viam's SDKs to connect to `viam-agent` and provision your machines:

- For mobile applications (existing or new) use the [Flutter SDK](https://flutter.viam.dev/viam_protos.provisioning.provisioning/ProvisioningServiceClient-class.html)
- For web applications, use the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/src/app/provisioning-client.ts).

If you are not using Flutter or TypeScript and would like to use provisioning, please [contact us](mailto:support@viam.com).

Regardless whether provisioning happens with a web or mobile or app, the process generally follows the same pattern:

{{< tabs >}}
{{% tab name="Without pre-configured network" min-height="703px" %}}

{{<video webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with viam-agent." poster="/platform/provisioning-demo.jpg" class="alignright" max-width="400px">}}

1. When a machine that has `viam-agent` installed and `agent-provisioning` configured comes online, `agent-provisioning` creates a WiFi hotspot.

   - The [`agent-provisioning` configuration](#configuration) is at <file>/etc/viam-provisioning.json</file.
   - The [`viam-agent` configuration](/configure/agent/#configuration), if provided, is at <file>/etc/viam.json</file> alongside the rest of the machine configuration, including which fragments to use (if any).

1. The end user uses their mobile device or computer and connects to the WiFi hotspot.

   - By default, the hotspot network is named `viam-setup-HOSTNAME`, where `HOSTNAME` is replaced with the hostname of your machine.
     The WiFi password for this hotspot network is `viamsetup` by default.
     You can customize these values in the machine's or fragment's [`viam-agent` configuration](/configure/agent/#configuration).

1. If the end user has a provisioning web or mobile app, they should now open that app to complete setup.
   Alternatively, you will be redirected to a sign-in page.
   If you are using a laptop or are not redirected, try opening [http://viam.setup/](http://viam.setup/) in a browser.

1. In the browser or web or mobile app, the user will be prompted to provide the network information for the machine, that is the primary network for the machine.

   - If there is no machine configuration at <file>/etc/viam.json</file>, the provisioning app or captive portal will also require the user to paste an app configuration file.
     This is the JSON object which contains your machine part secret key and cloud app address, which your machine's `viam-server` instance needs to connect to the Viam app.

     To copy a machine's `viam-server` app configuration:

     - Navigate to your machine's page on [the Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
     - Select the part status dropdown to the right of your machine's name on the top of the page:
       {{<imgproc src="/build/micro-rdk/part-dropdown.png" resize="x600" style="max-width: 500px" declaredimensions=true alt="The part status dropdown of an offline machine.">}}
     - Click the copy icon underneath **Viam server configuration** to copy the `viam-server` app JSON configuration.
     - Paste the `viam-server` app config when prompted.

1. The machine will then disable the hotspot network and attempt to connected using the provided network information.
   If `viam-agent` cannot establish a connection using the provided network information, the machine will create the hotspot again and continue going through steps (2-5) until a connection is successfully established.
1. If the connection is successful, `viam-agent` installs `viam-server`.

   - `agent-provisioning` will use the provided network if it can connect, even if that network does not have internet access.
     Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
     If you want `agent-provisioning` to require that a WiFi network be connected to the internet in order to connect to it, enable roaming mode **and** do not provide a primary network.

1. `viam-agent` then starts `viam-server` with a provided configuration and the machine comes **live**.
   {{% /tab %}}

{{% tab name="With pre-configured network (Roaming mode)" %}}

Roaming mode allows you to specify multiple WiFi networks **in the machine's or fragment's [`viam-agent` configuration](/configure/agent/#configuration)**, each with their own priority, and `agent-provisioning` will try to connect to each specified network in order of priority from highest to lowest.

You must enable `roaming_mode` in the [`agent-provisioning` configuration](#configuration) to use roaming mode.
Additionally, the end user must either **not** provide a primary network or there must be an issue with the connection to the primary network, for `agent-provisioning` to enter roaming mode.
`agent-provisioning` will enter roaming mode only when `roaming_mode` is enabled and no connection can be established to a primary network.

1. When a machine that has `viam-agent` installed and `agent-provisioning` configured comes online, `agent-provisioning` enters roaming mode:

   - The [`agent-provisioning` configuration](#configuration) is at <file>/etc/viam-provisioning.json</file.
   - The [`viam-agent` configuration](/configure/agent/#configuration), is at <file>/etc/viam.json</file> alongside the rest of the machine configuration, including which fragments to use (if any).

1. In roaming mode, the machine attempts to connect to one or more pre-configured networks specified in the [`viam-agent` configuration](/configure/agent/#configuration) file in order of highest `priority`.

   - If none of the configured WiFi networks could be connected to, `agent-provisioning` will instead create its own WiFi hotspot and follow the flow for machines without pre-configured network.
     Consult the other tab for more information.
     You can configure how long `viam-agent` waits for connections and the timeout before it creates a hotspot in the [`agent-provisioning` configuration](#configuration).

1. If the connection is successful, `viam-agent` installs `viam-server`.
1. `viam-agent` then starts `viam-server` with a provided configuration and the machine comes **live**.

{{% /tab %}}
{{< /tabs >}}

## Configuration

When you [install `viam-agent`](/configure/agent/#installation), provide a provisioning configuration file at <file>/etc/viam-provisioning.json</file> with the following format:

{{< tabs >}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "<NAME>",
  "model": "NAME",
  "fragment_id": "<ID>",
  "hotspot_prefix": "<PREFIX>",
  "disable_dns_redirect": true,
  "hotspot_password": "<PASSWORD>",
  "roaming_mode": false,
  "offline_timeout": "0m00s",
  "user_timeout": "0m00s",
  "fallback_timeout": "0m00s"
}
```

{{% /tab %}}
{{% tab name="Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "Skywalker",
  "model": "C-3PO",
  "fragment_id": "2567c87d-7aef-41bc-b82c-d363f9874663",
  "hotspot_prefix": "skywalker-setup",
  "disable_dns_redirect": true,
  "hotspot_password": "skywalker123",
  "roaming_mode": false,
  "offline_timeout": "3m30s",
  "user_timeout": "2m30s",
  "fallback_timeout": "15m"
}
```

This file configures some basic metadata, specifies a [fragment](/fleet/fragments/) to use to configure the machine, and provides the WiFi hotspot network name and password to use on startup.
It also configures timeouts to control how long `viam-agent` waits for a valid local WiFi network to come online before creating its hotspot network, and how long to keep the hotspot active before terminating it.

{{% /tab %}}
{{< /tabs >}}

### Attributes

<!-- prettier-ignore -->
| Name       | Type   | Required? | Description |
| ---------- | ------ | --------- | ----------- |
| `manufacturer` | string | Optional | Purely informative. May be displayed on captive portal and/or mobile app. Default: `"viam"`. |
| `model` | string | Optional | Purely informative. May be displayed on captive portal and/or mobile app. Default: `"custom"`. |
| `fragment_id` | string | Optional | The `fragment_id` of the fragment to configure machines with. If present, the Viam mobile app can pre-configure a robot for a user by using this [TODO: and otherwise it can't??]. |
| `hotspot_prefix` | string | Optional | Viam agent will prepend this to the hostname of the device append and use the resulting string for the provisioning hotspot SSID. Default: `"viam-setup"`. |
| `disable_dns_redirect` | boolean | Optional | By default, ALL DNS lookups using the provisioning hotspot will redirect to the device. This causes most phones/mobile devices to automatically redirect the user to the captive portal as a "sign in" screen. When disabled, only domains ending in .setup (ex: viam.setup) will be redirected. This generally avoids displaying the portal to users and is mainly used in conjunction with a mobile provisioning application workflow. Default: `false`. |
| `hotspot_password` | string | Optional | The Wifi password for provisioning hotspot. Default: `"viamsetup"`. |
| `roaming_mode` | boolean | Optional | By default, the device will only attempt to connect to a single wifi network (the one with the highest priority), usually provided during initial provisioning/setup using the Viam app or the Viam mobile app. Wifi connection alone is enough to consider the device as "online" even if the global internet is not reachable. When enabled, the device will attempt connections to all configured networks, and only considers the device online if the internet is reachable. See [roaming mode](#how-an-end-user-would-use-it). Default: `false`. |
| `offline_timeout` | boolean | Optional | Will only enter provisioning mode (hotspot) after being disconnected longer than this time. Useful on flaky connections, or when part of a system where the device may start quickly, but the wifi/router may take longer to be available. Default: `"2m"` (2 minutes). |
| `user_timeout` | boolean | Optional | Amount of time before considering a user (using the provisioning portal using web or mobile app) idle, and resuming normal behavior. Used to avoid interrupting provisioning mode (for example for network tests/retries) when a user might be busy entering details. Default: `"5m"` (5 minutes). |
| `fallback_timeout` | boolean | Optional | Provisioning mode will exit after this time, to allow other unmanaged (for example wired) or manually configured connections to be tried. Provisioning mode will restart if the connection/online status doesn't change. Default: `"10m"` (10 minutes). |
| `networks` | boolean | Optional | The type of the network. See [Networks](/configure/agent/#networks). Default: `[]`. |
