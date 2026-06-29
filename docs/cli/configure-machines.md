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
The machine is not connected to any hardware until you [install `viam-server`](/set-up-a-machine/) on a device and configure it with this machine's credentials.

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

Add a resource to a machine part by specifying its model and the resource subtype it implements.
For built-in resources (such as a webcam camera or GPIO motor), pass the subtype with `--resource-subtype`:

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource \
  --part=<part-id> \
  --name=my-camera \
  --model-name=webcam \
  --resource-subtype=camera
```

For resources from a registry module, pass the model triplet with `--model-name` and use the same `--resource-subtype`:

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource \
  --part=<part-id> \
  --name=my-board \
  --model-name=viam:raspberry-pi:rpi5 \
  --resource-subtype=board
```

The `--resource-subtype` value is the third segment of the model's API.
The webcam camera's API is `rdk:component:camera`, so the subtype is `camera`.
The vision service's API is `rdk:service:vision`, so the subtype is `vision`.
See [Components](/reference/components/) and [Services](/reference/services/) for all standard subtypes.

Use `--api` instead of `--resource-subtype` only for a [custom resource API](/build-modules/advanced-patterns/#define-a-new-resource-api).
Pass the full triplet, for example `--api=acme:component:gizmo`.
Most third-party modules implement a standard subtype or use [generic component](/reference/components/generic/) or [generic service](/reference/services/generic/), both of which take `--resource-subtype`.

This creates a bare resource entry with no additional attributes.
Most components need attributes like pin numbers or device paths to function.
See [Update resource attributes](#update-resource-attributes) to set them from the CLI, or configure them in the [Viam app](https://app.viam.com).

Model names take one of two forms:

- **Built-in models** ship with `viam-server` and use a single name (such as `webcam`, `gpio`, `fake`). Internally they expand to `rdk:builtin:<name>`.
- **Module models** come from the registry and use a three-part triplet `<namespace>:<module>:<model>` (such as `viam:raspberry-pi:rpi5`). Browse available models in the [Viam registry](https://app.viam.com/registry).

Common model names:

| Component            | Model                    | Subtype  |
| -------------------- | ------------------------ | -------- |
| Webcam camera        | `webcam`                 | `camera` |
| GPIO motor           | `gpio`                   | `motor`  |
| Fake arm (testing)   | `fake`                   | `arm`    |
| Fake motor (testing) | `fake`                   | `motor`  |
| Raspberry Pi 5 board | `viam:raspberry-pi:rpi5` | `board`  |
| Ultrasonic sensor    | `viam:ultrasonic:sensor` | `sensor` |

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
Add a fragment to a machine part by specifying its name or ID:

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add --part=<part-id> --fragment=<fragment-name-or-id>
```

If you omit the `--fragment` flag, the CLI prompts you to select a fragment interactively.

Remove a fragment:

```sh {class="command-line" data-prompt="$"}
viam machines part fragments remove --part=<part-id> --fragment=<fragment-name-or-id>
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

## Add or delete a part

Most machines have only a main part, which is created when you create the machine.
For [multi-part machines](/hardware/multi-machine/), add additional parts to an existing machine:

```sh {class="command-line" data-prompt="$"}
viam machines part create --machine=<machine-id> --part-name=<new-part-name>
```

Delete a part from a machine:

```sh {class="command-line" data-prompt="$"}
viam machines part delete --part=<part-id>
```

## Related pages

- [Get started](/set-up-a-machine/) for setting up your first machine
- [Configure hardware](/hardware/) for component configuration with the Viam app
- [Manage your fleet with the CLI](/cli/manage-your-fleet/) for monitoring and remote access
- [CLI reference](/cli/reference/#machines-aliases-robots-robot-machine) for the complete `machines` command reference
