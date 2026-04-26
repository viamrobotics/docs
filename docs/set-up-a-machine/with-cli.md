---
linkTitle: "Set up machines with the CLI"
title: "Set up machines with the CLI"
weight: 2
layout: "docs"
type: "docs"
description: "Create and connect machines from the command line."
aliases:
  - /set-up-a-machine/as-code/
---

Create and connect a machine to the Viam platform from the command line, instead of clicking through the Viam app.

You'll need:

- An organization and a location in the Viam app. New to Viam? Use [Set up your first machine](/set-up-a-machine/first-machine/) to create them, then come back.
- An API key for the CLI. See [Manage API keys](/cli/administer-your-organization/#manage-api-keys).
- A Linux or macOS device to run `viam-agent`. For Windows or ESP32, use [Set up your first machine](/set-up-a-machine/first-machine/).

## 1. Install and authenticate the CLI

{{< readfile "/static/include/how-to/install-cli.md" >}}

In a script, authenticate with an API key:

```sh {class="command-line" data-prompt="$"}
viam login api-key --key-id=<key-id> --key=<key>
```

## 2. Create the machine

```sh {class="command-line" data-prompt="$"}
viam machines create --name=my-first-machine --location=<location-id>
```

The CLI prints the new machine's ID:

```sh {class="command-line" data-prompt="$" data-output="1"}
created new machine with id abc12345-1234-abcd-5678-ef1234567890
```

To find your location ID:

```sh {class="command-line" data-prompt="$"}
viam locations list
```

## 3. Get the part ID

Every machine has at least one part. To install `viam-agent` on the device, you need the part ID:

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine=<machine-id>
```

## 4. Install viam-agent on the device

On the compute device that will run the machine, run:

```sh {class="command-line" data-prompt="$"}
sudo /bin/sh -c "VIAM_API_KEY_ID=<key-id> VIAM_API_KEY=<key> VIAM_PART_ID=<part-id>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

The install script downloads `viam-agent`, fetches the machine's cloud config to `/etc/viam.json` using the credentials above, and starts the agent service.

## 5. Verify the machine is online

```sh {class="command-line" data-prompt="$"}
viam machines status --machine=<machine-id>
```

If the machine is connected, the CLI prints its part list and status. If not, see the troubleshooting tips on [Set up your first machine](/set-up-a-machine/first-machine/#troubleshooting).

## 6. Apply a baseline configuration (optional)

If you have a fragment defining your standard component setup, attach it to the machine's main part:

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add --part=<part-id> --fragment=<fragment-id>
```

See [Reuse machine configuration](/fleet/reuse-configuration/) for the fragment authoring workflow.

## Set up multiple machines

The pattern above handles one machine. To do this for many machines, wrap steps 2-6 in a script. See [Automate with scripts](/cli/automate-with-scripts/#provisioning-create-and-configure-a-machine) for a complete provisioning script.

## What's next

- [Configure hardware](/hardware/configure-hardware/) to add components and services.
- [Reuse machine configuration](/fleet/reuse-configuration/) to author the fragments your machines apply.
- [Automate with scripts](/cli/automate-with-scripts/) for bulk operations and CI/CD.
