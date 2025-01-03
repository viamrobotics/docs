---
linkTitle: "Start a new machine"
title: "Start a new machine"
weight: 10
layout: "docs"
type: "docs"
no_list: true
description: "Install the software that drives hardware and connects your device to the cloud."
---

Get started by installing the open-source software that drives your hardware and connects your device to the cloud.
The easiest way to do this is through the Viam app, so that your machines are automatically connected to configuration and remote operation tools.

## Quickstart

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices as well as viewing data.
1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ in the app.
   A machine represents your device.
1. From your machine's page in the Viam app, follow the setup instructions to install `viam-server` on your device and connect it to the cloud.
   `viam-server` is the executable binary that runs on your device and manages hardware drivers, software, and data capture and sync.
1. Use the **+** button on your machine's **CONFIGURE** tab to add [supported hardware components](/operate/get-started/supported-hardware/) so that `viam-server` can control your specific hardware.
1. Use this same **+** button to configure software services such as [data capture and sync](/data-ai/capture-data/capture-sync/).

As soon as you configure each component and save the configuration, you can use the **TEST** panel of the component's config card to, for example, view your camera's stream or turn your motor.

## Concepts

### What is a machine?

A _machine_ is a computer (often a single-board computer like a Raspberry Pi or Jetson) or microcontroller and all the hardware attached to it, as well as the software running on it.
You can think of one machine as representing one device, or one robot.

When you create a new machine in the Viam app, Viam generates a unique set of credentials for that machine that connect the physical machine to its instance in the Viam app.

### How the configuration works

The machine setup steps displayed in the Viam app copy your machine's credentials to your machine.
When you turn on your machine, `viam-server` starts up and uses the provided credentials to fetch its configuration from the Viam app.
Once the machine has a configuration, it caches it locally and can use the config for up to 60 days.
Since the configuration is cached locally, your machine does not need to stay connected to the Viam app after it has obtained its configuration file.

If it is online, the machine checks for new configurations every 15 seconds and changes its config automatically when a new config is available.
All communication happens securely over HTTPS using secret tokens that are in the machine's config.

If your machine will never connect to the internet, you can also create a [local configuration file](/operate/reference/local-configuration-file/) on the machine itself.
