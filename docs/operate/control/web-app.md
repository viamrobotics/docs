---
linkTitle: "Create a web app"
title: "Create a web app"
weight: 10
layout: "docs"
type: "docs"
no_list: true
description: "Create a custom user interface for interacting with machines from a browser."
---

You can use Viam's [TypeScript SDK](https://ts.viam.dev/) to create a custom web application to interact with your devices.
The TypeScript SDK includes:

- Implementation of the standard component and service APIs to control your hardware and software
- Authentication tools so users can log in securely

## Install the TypeScript SDK

Run the following command in your terminal to install the Viam TypeScript SDK:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
```

## Connect to your machine

You can find sample connection code on each machine's **CONNECT** tab in the [Viam app](https://app.viam.com).
Select **TypeScript** to display a code snippet, with connection code as well as some calls to the APIs of the resources you've configured on your machine.

You can use the toggle to include the machine API key and API key ID, though we strongly recommend storing your API keys in environment variables to reduce the risk of accidentally sharing your API key and granting access to your machines.

## Write your app

Refer to the [Viam TypeScript SDK](https://ts.viam.dev/) documentation for available methods.

### Example usage

For an example using Vite to connect to a machine, see [Viam's vanilla TypeScript quickstart example on GitHub](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples/vanilla).

The following tutorial uses the Viam TypeScript SDK to query data that has been uploaded to the Viam cloud from a sensor, and display it in a web dashboard.

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}

## Test your app

You can run your app directly on the machine's single-board computer (SBC) if applicable, or you can run it from a separate computer connected to the internet or to the same local network as your machine's SBC or microcontroller.
The connection code will establish communication with your machine over LAN or WAN.

You can also host your app on a server or hosting service of your choice.

## Set up user authentication

Viam uses [FusionAuth](FusionAuth) for authentication and authorization.

Use the [Viam CLI `auth-app` command](/dev/tools/cli/#auth-app) to register your application with FusionAuth so that you or your users can log into your app with the same credentials they use to log into the [Viam app](https://app.viam.com).

For support building apps with custom login flows, [contact us](mailto:support@viam.com).