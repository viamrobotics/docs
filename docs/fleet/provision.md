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

The provisioning subsystem is a feature of [`viam-agent`](/configure/agent/), which you can install as part of your manufacturing process.
`agent-provisioning` will then perform the rest of the first-time setup for your machine once an [end user sets up the machine](#end-user-experience).

Consider a company that sells machines that monitor weather conditions on a maritime craft and provide navigation advice based on those readings.
Such a machine might use Viam to regularly capture and upload a stream of sensor readings, for example.
To parse the readings and provide tailored guidance to a ship's captain, the company writes their own proprietary application which includes live analytics and speech generation for conveying advice to the captain.

Using `agent-provisioning`, this company can ship their machines directly to customers with `viam-agent` installed.
When a customer sets up their machine, the provisioning subsystem installs `viam-server`.
By having the end customer set up the machine, the company:

- eliminates per-device setup and individualization at the factory
- allows for tailored configurations per customer as needed
- allows customer to provide their own WiFi credentials

{{< alert title="Support Notice" color="note" >}}

Provisioning is supported and tested only on Debian 11 (Bullseye), and 12 (Bookworm) but should work on most distros using NetworkManager v1.42 (or newer) as well.
For Bullseye, the installation of `viam-agent` changes the network configuration to use NetworkManager.

{{< /alert >}}

## End user experience

End users receive a machine, and use either a captive web portal or mobile app to complete the machine setup.

One option is to use the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app).
The Viam mobile app allows end users to create a new machine in the app, and `agent-provisioning` will then install `viam-server` and run it with a provided configuration.

To add your branding, you can build your own mobile app and use the [Flutter SDK](https://flutter.viam.dev/viam_protos.provisioning.provisioning/ProvisioningServiceClient-class.html) or the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/blob/main/src/app/provisioning-client.ts) to connect to `viam-agent` and provision your machines.

If you are not using Flutter or TypeScript and would like to use provisioning, please [contact us](mailto:support@viam.com).

This is the general process for provisioning depending on whether you are using a captive web portal or a mobile app:

{{< tabs >}}
{{% tab name="Mobile app" min-height="703px" %}}

{{<video webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with viam-agent." poster="/platform/provisioning-demo.jpg" class="alignright" max-width="400px" style="margin-left: 2rem">}}

1. If the provisioning happens with a mobile app, open the app and follow any instructions there until the app directs you to turn on the machine.

   - If you are using the Viam mobile app, create a new machine and then follow the instructions.

1. When you power on the machine that has `viam-agent` installed and `agent-provisioning` configured, `agent-provisioning` creates a WiFi hotspot.

   - The [`agent-provisioning` configuration](#configuration) is at <file>/etc/viam-provisioning.json</file>.

1. You then use your mobile device or computer and connect to the WiFi hotspot.

   - By default, the hotspot network is named `viam-setup-HOSTNAME`, where `HOSTNAME` is replaced with the hostname of your machine.
     The WiFi password for this hotspot network is `viamsetup` by default.
     You can customize these values in the [`agent-provisioning` configuration](/configure/agent/#configuration).

1. If you as the end user have a provisioning mobile app, go back to the app to complete setup.
   In the mobile app, you will be prompted to provide the network information for the machine.

1. The machine will then disable the hotspot network and attempt to connect using the provided network information.
   If `viam-agent` cannot establish a connection using the provided network information, the machine will create the hotspot again and continue going through steps (2-5) until a connection is successfully established.
1. If the connection is successful, `viam-agent` installs `viam-server`.

   - `agent-provisioning` will use the provided network if it can connect, even if that network does not have internet access.
     Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
     If you want `agent-provisioning` to require that a WiFi network be connected to the internet in order to connect to it, enable roaming mode.

1. `viam-agent` then starts `viam-server` with the provided configuration and the machine becomes **live**.

{{% /tab %}}
{{% tab name="Captive web portal" %}}

1. When you, as the end user, power on the machine that has `viam-agent` installed and `agent-provisioning` configured, `agent-provisioning` creates a WiFi hotspot.

   - The [`agent-provisioning` configuration](#configuration) is at <file>/etc/viam-provisioning.json</file>.
   - If a machine already exists, a machine cloud credentials file, if provided, is at <file>/etc/viam.json</file>.

1. You as the end user then use your mobile device or computer and connect to the WiFi hotspot.

   - By default, the hotspot network is named `viam-setup-HOSTNAME`, where `HOSTNAME` is replaced with the hostname of your machine.
     The WiFi password for this hotspot network is `viamsetup` by default.
     You can customize these values in the [`agent-provisioning` configuration](/configure/agent/#configuration).

1. Once connected to the hotspot, you will be redirected to a sign-in page.
   If you are using a laptop or are not redirected, try opening [http://viam.setup/](http://viam.setup/) in a browser.

1. In the captive web portal, you will then be prompted to provide the network information for the machine.

   - If there is no machine cloud credentials file at <file>/etc/viam.json</file>, the captive portal will also require you to paste a machine cloud credentials file.
     This is the JSON object which contains your machine part secret key and cloud app address, which your machine's `viam-server` instance needs to connect to the Viam app.

     To copy a machine cloud credentials file:

     - Navigate to your machine's page on [the Viam app](https://app.viam.com).
     - Select the part status dropdown to the right of your machine's name on the top of the page.
       {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="machine cloud credentials button on the machine part info dropdown">}}
     - Click the copy icon next to **Machine cloud credentials**.
     - Paste the machine cloud credentials when prompted.

1. The machine will then disable the hotspot network and attempt to connect using the provided network information.
   If `viam-agent` cannot establish a connection using the provided network information, the machine will create the hotspot again and continue going through steps (2-5) until a connection is successfully established.
1. If the connection is successful, `viam-agent` installs `viam-server`.

   - `agent-provisioning` will use the provided network if it can connect, even if that network does not have internet access.
     Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
     If you want `agent-provisioning` to require that a WiFi network be connected to the internet in order to connect to it, enable roaming mode.

1. `viam-agent` then starts `viam-server` with the provided configuration and the machine becomes **live**.

{{% /tab %}}
{{< /tabs >}}

## Configuration

When you [install `viam-agent`](/configure/agent/#installation), you may optionally provide a provisioning configuration file to customize the experience at <file>/etc/viam-provisioning.json</file> with the following format:

{{< tabs >}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "manufacturer": "<NAME>",
  "model": "<NAME>",
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
| `manufacturer` | string | Optional | Purely informative. May be displayed on captive portal or provisioning app. Default: `"viam"`. |
| `model` | string | Optional | Purely informative. May be displayed on captive portal or provisioning app. Default: `"custom"`. |
| `fragment_id` | string | Optional | The `fragment_id` of the fragment to configure machines with. Required when using the Viam mobile app for provisioning. The Viam mobile app uses the fragment to configure the machine. |
| `hotspot_prefix` | string | Optional | Viam agent will prepend this to the hostname of the device and use the resulting string for the provisioning hotspot SSID. Default: `"viam-setup"`. |
| `disable_dns_redirect` | boolean | Optional | By default, ALL DNS lookups using the provisioning hotspot will redirect to the device. This causes most phones/mobile devices to automatically redirect the user to the captive portal as a "sign in" screen. When disabled, only domains ending in .setup (ex: viam.setup) will be redirected. This generally avoids displaying the portal to users and is mainly used in conjunction with a mobile provisioning application workflow. Default: `false`. |
| `hotspot_password` | string | Optional | The Wifi password for the provisioning hotspot. Default: `"viamsetup"`. |
| `roaming_mode` | boolean | Optional | By default, the device will only attempt to connect to a single wifi network (the one with the highest priority), provided during initial provisioning/setup using the provisioning mobile app or captive web portal. Wifi connection alone is enough to consider the device as "online" even if the global internet is not reachable. If the primary network configured during provisioning cannot be connected to and roaming mode is enabled, the device will attempt connections to all configured networks in `networks`, and only consider the device online if the internet is reachable. Default: `false`. |
| `offline_timeout` | boolean | Optional | Will only enter provisioning mode (hotspot) after being disconnected longer than this time. Useful on flaky connections, or when part of a system where the device may start quickly, but the wifi/router may take longer to be available. Default: `"2m"` (2 minutes). |
| `user_timeout` | boolean | Optional | Amount of time before considering a user (using the captive web portal or provisioning app) idle, and resuming normal behavior. Used to avoid interrupting provisioning mode (for example for network tests/retries) when a user might be busy entering details. Default: `"5m"` (5 minutes). |
| `fallback_timeout` | boolean | Optional | Provisioning mode will exit after this time, to allow other unmanaged (for example wired) or manually configured connections to be tried. Provisioning mode will restart if the connection/online status doesn't change. Default: `"10m"` (10 minutes). |
| `networks` | boolean | Optional | Add additional networks the machine can connect to for provisioning. We recommend that you add WiFi settings in the operating system (for example, directly in NetworkManager) rather than in this file, or in the corresponding machine config in the Viam app, if networks aren't needed until after initial provisioning. See [Networks](/configure/agent/#networks). Default: `[]`. |

#### Networks

During the provisioning process, a machine connects to a network to install `viam-server`.
If an end user uses an app to provision the machine, they will generally provide network details through that app.

If you know in advance which other networks a machine should be able to connect to, we recomment that you add WiFi settings in the operating system (for example, directly in NetworkManager).

However, if you want to add additional networks to the provisioning configuration you can add them to the `networks` field value.

{{< alert title="Important" color="note" >}}
You must enable `roaming_mode` in the [`agent-provisioning` configuration](#configuration) to allow the machine to connect to the specified networks.
{{< /alert >}}

If `roaming_mode` is enabled, `agent-provisioning` will try to connect to each specified network in order of `priority` from highest to lowest.

<!-- prettier-ignore -->
| Name       | Type   | Description |
| ---------- | ------ | ----------- |
| `type`     | string | The type of the network. Options: `"wifi"`|
| `ssid`     | string | The network's SSID. |
| `psk`      | string | The network pass key. |
| `priority` | int    | Priority to choose the network with. Values between -999 and 999. Default: `0`. |

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`:

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
  "fallback_timeout": "15m",
  "roaming_mode": true,
  "networks": [
    {
      "type": "wifi",
      "ssid": "otherNetworkOne",
      "psk": "myFirstPassword",
      "priority": 30
    },
    {
      "type": "wifi",
      "ssid": "otherNetworkTwo",
      "psk": "mySecondPassword",
      "priority": 10
    }
  ]
}
```
