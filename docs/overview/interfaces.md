---
linkTitle: "Interfaces"
title: "Interfaces"
weight: 2
layout: "docs"
type: "docs"
description: "The ways to work with Viam, from the Viam web app to the CLI, SDKs, and MCP server, and which one to use for what."
capabilities: ["docs"]
diataxis: overview
---

You can work with Viam through a web app, a mobile app, a command-line tool, code libraries, and an AI-facing server.
They all talk to the same platform, so a machine you set up in one is available in the others.

Most people start in the Viam web app and use the other tools as their needs grow.

## The Viam web app

The Viam web app, at [app.viam.com](https://app.viam.com), is the home base for everything you do with Viam.
It runs in any browser, and it's where you'll spend your first hours with the platform.
Your account, your organizations, and every machine you've created are managed here.

Use it to set up and configure machines, test them, and monitor them through the user interface and the 3D scene.

Here is what you'll find:

- **Your fleet.** Organizations contain locations, and locations contain machines. The fleet view shows each machine's status, and from it you open any machine's page.
- **A page for each machine.** It has a tab for each kind of work: **CONFIGURE** to describe the hardware and software the machine runs, **CONTROL** to test components and drive the machine, **LOGS** to see what it has reported, and **CONNECT** for code samples and connection details.
- **The 3D scene.** The **3D SCENE** tab shows your machine and the spatial data around it, including frames, geometry, point clouds, and motion plans. It's the quickest way to catch a misplaced frame or obstacle.
- **Data and dashboards.** Browse captured data, group it into datasets, train ML models on it, and chart live sensor readings across machines.
- **The registry.** Browse modules and ML models published by Viam and the community, and add them to your machines.
- **Organization settings.** Manage who has access, API keys, and billing.
- **An in-app assistant.** On any tab of a machine's page, ask in plain language for what you need. The assistant reads your machine's configuration, status, and logs, can stage configuration changes, and can propose diagnostic commands. Nothing takes effect until you review and approve it.

{{< cards >}}
{{% card link="/set-up-a-machine/first-machine/" noimage="true" %}}
{{% card link="/monitor/" noimage="true" %}}
{{% card link="/visualization/3d-scene/" noimage="true" %}}
{{< /cards >}}

## The Viam mobile app

The Viam mobile app, available in the App Store and Google Play, is a companion to the web app. It lets you see which machines are online, watch camera feeds, adjust components, and check logs.
It can also move an arm by moving your phone and upload photos to the cloud.

- Use it to check on or operate a machine when you're away from a computer.
- It's best for operating machines, not for setting them up. Switch to the web app to change a machine's configuration.

To learn more, see [the Viam mobile app](/monitor/default-interface/#viam-mobile-app).

## The Viam CLI

The `viam` command-line tool covers most of what the web app does, in a form you can script.
It adds things the web app doesn't do, such as publishing modules and calling a machine's API methods one at a time.

- Use it to automate repeated work, run operations from a script or CI, or work from a terminal.
- It's best once you know what you want to do and want to do it quickly or many times.

To get started, see the [CLI overview](/cli/overview/).

## The Viam SDKs

The SDKs are libraries for writing your own code that controls machines and talks to the Viam cloud.
They're available for [Python](/reference/sdks/python/), [Go](/reference/sdks/go/), and [C++](/reference/sdks/cpp/) (backend), [TypeScript](/reference/sdks/typescript/) (browser), and [Flutter](/reference/sdks/flutter/) (mobile).

- Use them to write modules that add hardware drivers or logic to a machine, to write control code that runs outside the machine, or to build a web or mobile app for your users.
- They're best when you need behavior that the other interfaces can't express, such as a loop, a decision, or a custom interface.

To write a module, in Python, Go, or C++, see [Build and deploy modules](/build-modules/overview/). To build an app for your own users, see [Build apps](/build-apps/overview/).

## The Viam MCP server

The Viam MCP server lets an AI assistant that supports the Model Context Protocol work with your fleet.
Once you connect it, the assistant can look up your machines, read and edit their configuration, and call their API methods, within the permissions your account already has.

- Use it to configure or inspect machines in conversation instead of in the web app.
- It's best for configuration and fleet lookups. It doesn't include tools for querying captured data.

To connect an assistant, see the [MCP server](/reference/mcp/).

{{% alert title="Ask an AI assistant to do it for you" color="tip" %}}
An assistant that can run the CLI, write code against the SDKs, and use the MCP server can perform most Viam tasks on your behalf.
Describe what you want, such as "add a camera to my machine" or "write a script that moves the arm to the home position", and it does the work.
You'll still use the web app for some administration tasks and to access visual tools such as the 3D scene.
See [Use Viam from an AI agent](/build-apps/use-viam-from-an-agent/).
{{% /alert %}}

{{% alert title="Review what an assistant does to a machine" color="caution" %}}
An assistant that can move hardware can also cause damage.
Before you let one drive a machine, read the safety guidance in [Use Viam from an AI agent](/build-apps/use-viam-from-an-agent/).
{{% /alert %}}

## What each interface can do

A check mark means the interface can do this. A blank cell means it can't.

| To do this                         | Web app | Mobile app | CLI | SDKs | MCP server |
| ---------------------------------- | ------- | ---------- | --- | ---- | ---------- |
| See the 3D scene                   | ✓       |            |     |      |            |
| Monitor and operate a machine      | ✓       | ✓          | ✓   | ✓    | ✓          |
| Write control code                 | ✓       |            | ✓   | ✓    | ✓          |
| Change a machine's configuration   | ✓       |            | ✓   | ✓    | ✓          |
| Manage your organization and fleet | ✓       |            | ✓   | ✓    | ✓          |
| Build a web or mobile app          |         |            |     | ✓    |            |
| Write a module                     | ✓       |            | ✓   | ✓    |            |
| Add a module to a machine          | ✓       |            | ✓   | ✓    | ✓          |
| Query captured data                | ✓       | ✓          | ✓   | ✓    |            |
