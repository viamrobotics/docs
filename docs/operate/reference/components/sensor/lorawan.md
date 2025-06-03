---
title: "Configure a LoRaWAN network"
linkTitle: "LoRaWAN"
weight: 60
type: "docs"
description: "Configure a gateway and nodes to communicate over the LoRaWAN protocol."
tags: ["sensor", "components", "lorawan"]
icon: true
images: ["/icons/components/sensor.svg"]
---

LoRaWAN (Long Range Wide Area Network) enables sensor communication spanning kilometers with minimal power usage.

To collect LoRaWAN sensor data with Viam, use the [`lorawan`](https://app.viam.com/module/viam/lorawan) {{< glossary_tooltip term_id="module" text="module" >}}. You can find the module's source code in the [lorawan GitHub repository](https://github.com/viam-modules/lorawan).

## Hardware requirements

- a [supported LoRaWAN gateway](https://github.com/viam-modules/lorawan?tab=readme-ov-file#lorawan-gateway-models-provided)
- a [supported LoRaWAN node](https://github.com/viam-modules/lorawan?tab=readme-ov-file#lorawan-sensor-models-provided)

## Architecture

Viam supports LoRaWAN networks containing multiple gateways and multiple nodes.
Connect gateway hardware to a machine, or add a new machine that includes LoRaWAN gateway hardware.
For each physical gateway, add a gateway model to your machine in the Viam app to configure the gateway.
For each physical node, add a node model to your machine in the Viam app to connect the node to your gateways.
You can view data collected by your nodes in the **DATA** page of the Viam app.
To monitor data using visualizations on a dashboard, open **FLEET** > **TELEOP** and configure visualization widgets.

## Add a gateway

To start your network, you need a gateway.
The lorawan module supports the following varieties of gateway hardware:

- peripherals built on the SX1302 chip such as the Waveshare SX1302 Gateway HAT, which you can connect to an SBC
- dedicated machines such as the Raspberry Pi CM4-based RAK7391 WisGate Connect

If you choose the RAK7391:

1. Complete the [quickstart](https://docs.rakwireless.com/product-categories/wisgate/rak7391/quickstart/) to flash your RAK7391 with an operating system and connect it to the network.
1. [Install viam-server](https://docs.viam.com/operate/get-started/setup/).

If you choose a peripheral built on the SX1302 chip:

1. Follow our guide to [set up an SBC](/operate/get-started/setup/).
1. Follow the instructions provided by your peripheral manufacturer (for instance, the [Waveshare SX1302 LoRaWAN Gateway HAT](https://www.waveshare.com/wiki/SX1302_LoRaWAN_Gateway_HAT)) to connect your peripheral to your SBC.
   For supported models, there is no need to configure drivers and software; viam-server will handle that for you.

After setting up your gateway hardware, complete the following steps to configure your gateway:

{{< tabs >}}
{{% tab name="Builder" %}}

1. Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
1. Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
1. Select the `sensor` type, then select the `lorawan` model that matches the name of your gateway.
   If you chose a peripheral built on the SX1302 chip other than the Waveshare SX1302, choose `lorawan:sx1302-hat-generic`.
1. Click **Add module**, and enter a name for your gateway sensor.
1. Click **Create** to add the module to your machine.
1. Click **Save** in the top right to apply your changes and load your new module.

{{% /tab %}}
{{% tab name="JSON Configuration" %}}

In the `components` section of your machine configuration, add the following object:

```json
{
  "name": "sensor-1",
  "api": "rdk:component:sensor",
  "model": "viam:lorawan:<sensor-name>",
  "attributes": {
    "gateway_eui": "<gateway-eui>",
    "server_address": "<network-server-address>",
    "port": 1700
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for SX1302-based LoRaWAN gateways:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | Name of the board connected to the HAT (for example "rpi"). |
| `spi_bus` | integer | Optional | SPI bus number. |
| `region_code` | string | Optional | Frequency region ("US915" or "EU868") of your gateway. Default: "US915". |
| `reset_pin` | integer | **Required** | GPIO pin used for SX1302 reset. Not configurable for `sx1302-waveshare-hat`. |
| `power_en_pin` | integer | Optional | GPIO pin used for SX1302 power enable. Not configurable for `sx1302-waveshare-hat`. |

The following attributes are available for RAK7391 gateways:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | Name of the board connected to the HAT (for example "rpi"). |
| `region_code` | string | Optional | Frequency region ("US915" or "EU868") of your gateway. Default: "US915". |
| `pcie1` | object | optional | GPIO pin used for SX1302 reset. Not configurable for `sx1302-waveshare-hat`. |
| `pcie2` | object | Optional | GPIO pin used for SX1302 power enable. Not configurable for `sx1302-waveshare-hat`. |

In the `pcie1` and `pcie2` fields of RAK7391 gateways, you can configure the following additional attributes:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `spi_bus` | integer | Optional | Serial bus the concentrator is connected to, if connected through SPI. |
| `serial_path` | string | Optional | Serial path concentrator is mounted at, if connected through USB. |

{{% alert title="Info" color="info" %}}

To add a new gateway to an existing LoRaWAN network, also add the new gateway to the list of `gateways` in each node configuration.

{{% /alert %}}

## Add a node

Complete the following steps to configure your a node:

{{< tabs >}}
{{% tab name="Builder" %}}

1. Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
1. Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
1. Select the `sensor` type, then select the `lorawan` model that matches the name of your node.
   If the name of your sensor does not appear in the list, choose the generic `lorawan:node` option.
1. Click **Add module**, and enter a name for your node.
1. Click **Create** to add the module to your machine.
1. Click **Save** in the top right to apply your changes and load your new module.

{{% /tab %}}
{{% tab name="JSON Configuration" %}}

In the `components` section of your machine configuration, add the following object, depending on your preferred [activation protocol](#activation-protocols):

{{< tabs >}}
{{% tab name="OTAA" %}}

```json
{
  "join_type": "OTAA",
  "dev_eui": <string>,
  "app_key": <string>,
  "gateways": [<string gatewayname>]
}
```

{{% /tab %}}
{{% tab name="ABP" %}}

```json
{
  "join_type": "ABP",
  "dev_addr": <string>,
  "app_s_key": <string>,
  "network_s_key": <string>,
  "gateways": [<string gatewayname>]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for nodes:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `dev_eui` | string | **Required** | The unique 64-bit identifier for the LoRaWAN device in hexadecimal format (16 characters). Found on the hardware or in the box. |
| `join_type` | string | Optional | The [activation protocol](#activation-protocols) used to secure this network. Default: "OTAA". |
| `app_key` | string | Optional | The 128-bit AES key used for device authentication and session key derivation in hexadecimal format. Required to use the OTAA activation protocol. Found in the device datasheet. |
| `dev_addr` | string | Optional | 32-bit hexadecimal value used to identify this device in uplink messages. Found in your datasheet or in the box. Required to use the ABP activation protocol. Found in the device datasheet or in the box. |
| `app_s_key` | string | Optional | 128-bit hexadecimal value used to decrypt uplink messages. Required to use the ABP activation protocol. Found in the datasheet or in the box. |
| `network_s_key` | string | Optional | 128-bit hexadecimal value used to decrypt uplink messages. Required to use the ABP activation protocol. Found in the datasheet or in the box. |
| `gateways` | string[] | **Required** | String names of gateway sensors from your Viam configuration. |
| `uplink_interval_mins` | decimal | **Required** | Interval between uplink messages sent from the node. Found in the datasheet, but can be modified. |
| `decoder_path` | string | **Required** | Path to the payload decoder script, written in Javascript. If multiple exist, uses the Chirpstack version. |
| `fport` | string | Optional | Hexadecimal port used to send downlinks to the device. |

{{% alert title="Info" color="info" %}}

Some models, including those for Milesight CT101 and Milesight EM310-TILT nodes, provide default values for `app_key`, `network_s_key`, and `app_s_key`: `5572404C696E6B4C6F52613230313823`.
Each model also provides a default value for `uplink_interval_mins`: 10 for the CT101, 1080 for EM310-TILT.

{{% /alert %}}

milesight-ct101 milesight-em310-tilt

Default: .

## Activation protocols

LoRaWAN networks can use any of the following protocols for communication:

`join_type`

Over-The-Air Activation (OTAA) (recommended):

- dynamic keys generated at join time
- rotated session keys
- uses dev eui, app eui, and appkey

Activation By Personalization (ABP):

- static keys
- no join procedure
- manual session key management
- uses devaddr, nwkskey, and appskey

otaa best for production, ABP suffices for testing

## Receive a downlink message from a node

## Send an uplink message to a node

## View captured data

1. Navigate to the **DATA** tab in the Viam app
2. Filter by your machine and component name
3. View captured sensor readings and LoRaWAN message data
4. Use the built-in visualization tools to create charts and graphs

## Key terms

- gateway
- node
- network server
- gateway eui: 64-bit
- application eui (JoinEUI): 64-bit
- device eui: 64-bit
- application key: AES-128 key for device auth and session key generation
- device class: A (max power efficiency), B, C (continuous networking)
- data rate: 0-15, higher value means faster transmission, but shorter range
- transmission power
- transmission window?
- uplink interval
- decoder -- http link
- ADR (adaptive data rate): automatic optimization of data rate and transmission power
- RSSI (Received Signal Strength Indicator)
- SNR (Signal-to-Noise Ratio)

## Troubleshooting

- acknowledgment toggle
- change transmission interval
