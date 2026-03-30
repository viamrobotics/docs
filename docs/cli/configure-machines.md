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
See [Viam CLI](/cli/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

Many commands on this page require an organization ID, location ID, machine ID, or part ID.

A machine can have one or more **parts**, each running a separate instance of `viam-server`.
Every machine has at least one part (the main part), which is created automatically when you create the machine.
When you add resources, apply fragments, or restart, you target a specific part.

Find your organization ID and location ID:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

```sh {class="command-line" data-prompt="$"}
viam locations list
```

Find machine IDs and part IDs:

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

The model triplet follows the format `namespace:type:model`.
Common model triplets:

| Component             | Model triplet                            |
| --------------------- | ---------------------------------------- |
| Webcam camera         | `viam:camera:webcam`                     |
| GPIO motor            | `viam:motor:gpio`                        |
| Linux board           | `viam:board:pi`                          |
| Movement sensor (GPS) | `viam:movement-sensor:gps-nmea-rtk-pmtk` |
| Ultrasonic sensor     | `viam:sensor:ultrasonic`                 |
| Fake arm (testing)    | `viam:arm:fake`                          |
| Fake motor (testing)  | `viam:motor:fake`                        |

## Remove a component or service

```sh {class="command-line" data-prompt="$"}
viam machines part remove-resource \
  --part=<part-id> \
  --name=my-camera
```

## Apply a fragment

Fragments are reusable configuration blocks.
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

## Delete a machine

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
