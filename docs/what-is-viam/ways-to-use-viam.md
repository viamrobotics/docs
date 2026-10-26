---
linkTitle: "Ways to use Viam"
title: "Ways to use Viam"
weight: 20
layout: "docs"
type: "docs"
description: "The ways to work with Viam, from the Viam web app to the CLI, SDKs, and MCP server, and which one to use for what."
capabilities: ["docs"]
diataxis: overview
---

You can work with Viam through a web app, a mobile app, a command-line tool, code libraries, and an AI-facing server.
They all talk to the same platform, so a machine you set up in one is available in the others.
Most people start in the Viam web app and add the others as their needs grow.
You can also ask an AI assistant to use several of them for you.

## The Viam web app

The Viam web app, at [app.viam.com](https://app.viam.com), is the home base for everything you do with Viam.
It runs in any browser, and it's the one place that does a bit of everything, so it's where you'll spend your first hours with the platform.
Your account, your organizations, and every machine you've created live here.

Use it to set up and configure machines, test them, and see what they're doing, all without writing code.
It's the best place to start, and the only place for some tasks, such as the 3D scene.

Here is what you'll find:

- **Your fleet.** Organizations contain locations, and locations contain machines. The fleet view shows each machine's status, and from it you open any machine's page.
- **A page for each machine.** It has a tab for each kind of work: **CONFIGURE** to describe the hardware and software the machine runs, **CONTROL** to test components and drive the machine, **3D SCENE** to see the machine and the space around it, **DATA** to browse what it has captured, **LOGS** to see what it has reported, and **CONNECT** for code samples and connection details.
- **Data and dashboards.** Browse captured data, group it into datasets, train ML models on it, and chart live sensor readings across machines.
- **The registry.** Browse modules and ML models published by Viam and the community, and add them to your machines.
- **Organization settings.** Manage who has access, API keys, and billing.

{{< cards >}}
{{% card link="/set-up-a-machine/first-machine/" noimage="true" %}}
{{% card link="/hardware/machine-configuration/" noimage="true" %}}
{{% card link="/visualization/3d-scene/" noimage="true" %}}
{{% card link="/monitor/" noimage="true" %}}
{{< /cards >}}

## The Viam mobile app

The Viam mobile app, available in the App Store and Google Play, is a companion to the web app for use away from your desk.
Its documented job is setting up a device: you sign in, pick an organization and location, and connect the device to WiFi over Bluetooth.

- Use it when you're handing a Viam-powered device to someone who isn't at a computer.
- It's best for getting a device online, not for configuring it. Switch to the web app for that.

## The Viam CLI

The `viam` command-line tool covers most of what the web app does, in a form you can script.
It adds things the web app doesn't do, such as publishing modules and calling a machine's API methods one at a time.

- Use it to automate repeated work, run operations from a script or CI, or work from a terminal.
- It's best once you know what you want to do and want to do it quickly or many times.

To get started, see the [CLI overview](/cli/overview/).

## The Viam SDKs

The SDKs are libraries for writing your own code that controls machines and talks to the Viam cloud.
They're available for [Python](/reference/sdks/python/), [Go](/reference/sdks/go/), and [C++](/reference/sdks/cpp/) (backend), [TypeScript](/reference/sdks/typescript/) (browser), and [Flutter](/reference/sdks/flutter/) (mobile).

- Use them to write control logic, read and use captured data in your own code, or build a custom web or mobile app for your users.
- They're best when you need behavior that the other interfaces can't express, such as a loop, a decision, or a custom interface.

To build an app for your own users, see [Build apps](/build-apps/overview/).

## The Viam MCP server

The Viam MCP server lets an AI assistant that supports the Model Context Protocol work with your fleet.
Once you connect it, the assistant can look up your machines, read and edit their configuration, and call their API methods, within the permissions your account already has.

- Use it to configure or inspect machines in conversation instead of in the web app.
- It's best for configuration and fleet lookups. It doesn't include tools for querying captured data.

To connect an assistant, see the [MCP server](/reference/mcp/).

{{% alert title="Ask an AI assistant to do it for you" color="tip" %}}
An AI assistant isn't a separate interface to Viam, but many people experience it as one.
An assistant that can run the CLI, write code against the SDKs, and use the MCP server can do most of what this page describes on your behalf.
Describe what you want, such as "add a camera to my machine" or "write a script that moves the arm to the home position", and it does the work.
You'll still use the web app for the visual parts, such as the 3D scene.
See [Use Viam from an AI agent](/build-apps/use-viam-from-an-agent/).
{{% /alert %}}

{{% alert title="Review what an assistant does to a machine" color="caution" %}}
An assistant that can move hardware can also cause damage.
Before you let one drive a machine, read the safety guidance in [Use Viam from an AI agent](/build-apps/use-viam-from-an-agent/).
{{% /alert %}}

## What each interface can do

| To do this | Web app | Mobile app | CLI | SDKs | MCP server |
| --- | --- | --- | --- | --- | --- |
| See the 3D scene | Yes | No | No | No | No |
| Write control code | No. Test components from the **CONTROL** tab. | No | Partly. Call one API method at a time. | Yes | Partly. Call API methods through a client. |
| Change a machine's configuration | Yes | ? | Yes | Yes | Yes |
| Manage your organization and fleet | Yes | ? | Yes | Yes. Through the fleet API. | Partly. Look up machines and create them. |
| Build a web or mobile app | No | No | No | Yes | No |
| Deploy a module to a machine | Yes. Add it from the registry. | No | Yes. Also publish modules. | No. Write modules; publish with the CLI. | No |
| Browse the registry | Yes | ? | ? | No | Partly. Look up items. |
| Query captured data | Yes | ? | Yes | Yes | No |
