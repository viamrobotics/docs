---
linkTitle: "Multi-machine setups"
title: "Multi-machine setups"
weight: 11
layout: "docs"
type: "docs"
no_list: true
description: "Connect multiple computers so one machine can access another's components and services."
date: "2026-04-16"
---

When you configure a machine in Viam, you're describing one computer running `viam-server` and the components attached to it.
Three situations call for reaching outside one computer:

- **The hardware lives somewhere else.**
  A depth camera is wired to a Raspberry Pi on an arm's end effector, but your control logic runs on a NUC.
  A row of cameras sits on SBCs along a conveyor, but inference happens on a GPU machine in a rack.
  The component has to be on the computer it's physically attached to.
- **Several machines need the same resource.**
  A fixed warehouse camera that every rover in the building needs to see.
  A SLAM service whose map serves three robots.
- **You want operational independence.**
  E-stopping the arm shouldn't cut the camera on its end effector.
  A crash on the main computer shouldn't take down the sensors running on another board.

Under the hood, `viam-server` on one machine opens a gRPC connection to `viam-server` on another.
The remote server's components and services join the local resource graph.
In your code they look like any other resource on the local machine: same API, same method calls, no separate client object.
Unless you configure a prefix, even the name stays the same.

Viam gives you two ways to create this connection, with different management models.

## Pick a pattern

<!-- prettier-ignore -->
| | Sub-part | Remote part |
| --- | --- | --- |
| Who writes the config | Viam cloud, through the app | You, with address + API key |
| Who sees whose resources | Main sees the sub; the sub cannot see the main | Either direction, or both, by configuring each side |
| Shared by multiple machines | No: each sub-part belongs to exactly one main | Yes: any number of machines can connect in |
| Cross-organization | No: must be in the same organization | Yes |

Three common scenarios:

- **Assembly-line cameras with central inference.**
  Five SBCs along a conveyor, each with a camera.
  A NUC runs ML inference and orchestrates.
  Configure the NUC as the main part and each SBC as a sub-part.
  The main part sees every camera stream, and the whole system shows up as one machine in the Viam app.
- **Shared warehouse camera.**
  A fixed camera over a workbench that three mobile bases need to read when they approach.
  Configure the camera's host machine as a remote part on each base.
  The camera belongs to one machine and is borrowed by the others.
- **Arm with an instrumented end effector.**
  The arm's main computer runs planning and control.
  A second small computer on the end effector hosts a camera and gripper.
  If the arm only needs to call the end-effector components, a sub-part is simpler to manage.
  If the end-effector computer also needs to read arm state directly (for vision-to-motion logic that runs there), configure each side as a remote of the other.

## Accessing remote resources in code

No special client, no new connection, no "remote" flag in your API calls.
Resources from a sub-part or remote part appear in the same resource list as your local components:

```python
my_arm = Arm.from_robot(machine, "arm-1")          # local or remote, same call
my_camera = Camera.from_robot(machine, "wrist-camera")
```

If you configured a prefix on the remote, it is prepended to every remote resource name with no separator:

```python
# Remote configured with prefix "end-effector"
gripper = Gripper.from_robot(machine, "end-effectorgripper")
```

Prefixes exist to disambiguate when two connected parts would otherwise export resources with the same name.

## What happens on disconnect

Two kinds of disconnect matter.

**A remote part goes offline.**
The connection is monitored in the background and reconnects automatically.
While the remote is down, its resources are marked unreachable and calls against them return an error.
Local resources on the main part keep running.

**A controlling client disappears.**
Every client connected to `viam-server` sends a periodic session heartbeat.
If the client goes silent (network loss, crashed process), any resource it most recently commanded gets `Stop()` called automatically.
A rover will not keep driving, an arm will not keep moving, and a gripper will not keep closing when the commanding process vanishes.
This applies equally to local and remote resources.

## Next steps

{{< cards >}}
{{% card link="/hardware/multi-machine/add-a-sub-part/" %}}
{{% card link="/hardware/multi-machine/add-a-remote-part/" %}}
{{% card link="/hardware/multi-machine/cross-machine-frames/" %}}
{{< /cards >}}

For the lower-level details of how machines communicate, see [Machine-to-machine communication](/operate/reference/architecture/machine-to-machine-comms/).
