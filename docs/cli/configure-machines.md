---
linkTitle: "Configure machines"
title: "Configure machines with the CLI"
weight: 10
layout: "docs"
type: "docs"
description: "Create machines, add components and services, and manage fragments from the command line."
---

Create and configure machines, add and remove components and services, and apply configuration fragments from the command line.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI overview](/cli/overview/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

Many commands on this page require an organization ID, location ID, machine ID, or part ID.

A machine can have one or more **parts**, each running a separate instance of `viam-server`.
Most machines have a single part.
Multi-part machines are used when one logical machine runs across multiple computers.
Every machine has at least one part (the main part), which is created automatically when you create the machine.
When you add resources, apply fragments, or restart, you target a specific part.

Find your organization ID and location ID:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

```sh {class="command-line" data-prompt="$"}
viam locations list
```

Find machine IDs and part IDs.
The `machines list` command prints each machine's ID and its main part ID.
Use `machines part list` to see all parts for a machine:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --location=<location-id>
```

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine=<machine-id>
```

## Create a machine

```sh {class="command-line" data-prompt="$"}
viam machines create --name=my-machine --location=<location-id>
```

This creates the machine in the Viam app.
The machine is not connected to any hardware until you [install `viam-server`](/foundation/) on a device and configure it with this machine's credentials.

On success, the CLI prints the new machine's ID:

```sh {class="command-line" data-prompt="$" data-output="1"}
created new machine with id abc12345-1234-abcd-5678-ef1234567890
```

Save this ID for subsequent commands.

## List machines

List all machines in a location:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --location=<location-id>
```

List all machines across your entire organization:

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --all
```

## Add a component or service

Add a resource to a machine part using its model triplet:

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource \
  --part=<part-id> \
  --name=my-camera \
  --model-name=viam:camera:webcam
```

This creates a bare resource entry with no additional attributes.
Most components need attributes like pin numbers or device paths to function.
See [Update resource attributes](#update-resource-attributes) to set them from the CLI, or configure them in the [Viam app](https://app.viam.com).

The model triplet follows the format `namespace:module-name:model-name`.
You can browse available models in the [Viam registry](https://app.viam.com/registry).
Common model triplets:

| Component            | Model triplet            |
| -------------------- | ------------------------ |
| Webcam camera        | `viam:camera:webcam`     |
| GPIO motor           | `viam:motor:gpio`        |
| Raspberry Pi 5 board | `viam:raspberry-pi:rpi5` |
| Ultrasonic sensor    | `viam:ultrasonic:sensor` |
| Fake arm (testing)   | `viam:arm:fake`          |
| Fake motor (testing) | `viam:motor:fake`        |

## Remove a component or service

```sh {class="command-line" data-prompt="$"}
viam machines part remove-resource \
  --part=<part-id> \
  --name=my-camera
```

Connected machines pick up configuration changes automatically.
You do not need to restart the machine after adding or removing a resource.

## Manage resources

### Update resource attributes

After adding a resource, use `viam resource update` to set its attributes.
The `--config` flag accepts inline JSON or a path to a JSON file:

```sh {class="command-line" data-prompt="$"}
viam resource update --part=<part-id> \
  --resource-name=my-sensor --config '{"pin": "38"}'
```

To load attributes from a file:

```sh {class="command-line" data-prompt="$"}
viam resource update --part=<part-id> \
  --resource-name=my-sensor --config ./sensor-config.json
```

{{< alert title="Caution" color="caution" >}}
The `--config` flag replaces all existing attributes on the resource.
To modify a single attribute, include the full attribute set in your JSON.
Passing an empty value for an attribute deletes it.
{{< /alert >}}

### Enable and disable resources

Disable a resource to stop it without removing it from the configuration.
This is useful for temporarily taking a component offline or debugging issues with a specific resource.

```sh {class="command-line" data-prompt="$"}
viam resource disable --part=<part-id> --resource-name=my-sensor
```

Re-enable it:

```sh {class="command-line" data-prompt="$"}
viam resource enable --part=<part-id> --resource-name=my-sensor
```

You can enable or disable multiple resources in a single command:

```sh {class="command-line" data-prompt="$"}
viam resource disable --part=<part-id> \
  --resource-name=my-sensor --resource-name=arm-1
```

## Apply a fragment

Fragments are reusable configuration blocks that can define a set of components, services, and their attributes.
Apply the same fragment across multiple machines to keep their configuration consistent.
Add a fragment to a machine part by specifying its fragment ID:

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add --part=<part-id> --fragment=<fragment-id>
```

If you omit the `--fragment` flag, the CLI prompts you to select a fragment interactively.

Remove a fragment:

```sh {class="command-line" data-prompt="$"}
viam machines part fragments remove --part=<part-id> --fragment=<fragment-id>
```

See [Reuse machine configuration](/fleet/reuse-configuration/) for details on creating and managing fragments.

## Rename or move a machine

```sh {class="command-line" data-prompt="$"}
viam machines update \
  --machine=<machine-id> \
  --new-name=updated-name \
  --new-location=<new-location-id>
```

Moving a machine to a different location may affect access if your API keys or permissions are scoped to a specific location.

## Delete a machine

{{< alert title="Caution" color="caution" >}}
Deleting a machine removes it and all of its configuration permanently.
This cannot be undone.
{{< /alert >}}

```sh {class="command-line" data-prompt="$"}
viam machines delete --machine=<machine-id>
```

## Restart a machine part

```sh {class="command-line" data-prompt="$"}
viam machines part restart --part=<part-id>
```

## Related pages

- [Get started](/foundation/) for setting up your first machine
- [Configure hardware](/hardware/) for component configuration with the Viam app
- [Manage your fleet with the CLI](/cli/manage-your-fleet/) for monitoring and remote access
- [CLI reference](/dev/tools/cli/#machines-alias-robots-and-machine) for the complete `machines` command reference
