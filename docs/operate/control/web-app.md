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

## Example usage

The following tutorial uses the Viam TypeScript SDK to query data that has been uploaded to the Viam cloud from a sensor, and display it in a web dashboard.

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}

## Set up authentication

Viam uses [FusionAuth](FusionAuth) for authentication and authorization.

Use the [Viam CLI `auth-app` command](/dev/tools/cli/#auth-app) to register your application with FusionAuth so that you or your users can log into your app with the same credentials they use to log into the [Viam app](https://app.viam.com).
