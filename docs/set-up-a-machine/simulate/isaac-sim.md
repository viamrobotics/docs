---
title: "Run an Isaac Sim simulation"
linkTitle: "Isaac Sim"
weight: 30
layout: "docs"
type: "docs"
description: "Start an Isaac Sim simulation on a Viam cloud GPU or your own RTX machine and connect your code to it."
capabilities: ["simulation", "billing"]
diataxis: how-to
date: "2026-11-24"
aliases:
  - "/set-up-a-machine/simulate-a-machine/"
---

Run a simulated robot arm and camera in NVIDIA Isaac Sim, and control them from the Viam app and your own code like any other machine.
You can run the simulation on a GPU in Viam's cloud, which is billed per minute, or on your own RTX Linux computer, which costs nothing extra.

## Prerequisites {#prerequisites}

- **For both:** Python 3 and the Viam Python SDK on your laptop, for step 4.
  See [Install the Python SDK](/reference/sdks/python/python-venv/).
- **In the cloud:** a Viam account and an organization you can create machines in.
  If you don't see the simulate option, simulation isn't turned on for your organization yet.
- **On your own GPU:** a computer with Ubuntu 22.04 or 24.04 on x86_64, an RTX-capable NVIDIA GPU with 8GB or more of VRAM, 32GB or more of RAM, and about 60GB of free disk.
  See NVIDIA's [Isaac Sim requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html).
  - An NVIDIA driver from the 580 branch, or no driver yet, in which case the module installs one.
    Newer branches crash Isaac Sim's renderer on startup.
  - `viam-server` installed and running as root, with the machine online in the Viam app.
    See [Set up your first machine](/set-up-a-machine/first-machine/).

## How Isaac Sim runs on a Viam machine {#how-isaac-sim-runs-on-a-viam-machine}

The Isaac Sim module runs Isaac Sim inside your machine's `viam-server`.
Its `world` component starts Isaac Sim and steps the simulation, and each simulated arm or camera names that world and appears in it.

In the cloud, Viam starts a container on a GPU-enabled machine that runs `viam-server` as your machine's part, from its saved configuration, with Isaac Sim already installed.
It's billed per minute after any monthly cloud credit your organization has, and it stops after an hour in which no component moves.
On your own GPU, the module installs Isaac Sim the first time it runs.
Either way, Isaac Sim takes minutes to boot the first time.

For how simulation fits into Viam and how Isaac Sim compares to MuJoCo, see [How simulation works](/set-up-a-machine/simulate/how-simulation-works/).

## 1. Start the machine {#start-the-machine}

{{< tabs >}}
{{% tab name="Cloud" %}}

1. In the [Viam app](https://app.viam.com), create a machine.
1. In the setup wizard, choose **No hardware yet • Simulate it**.
1. Read the notes about billing and limits, then click **Start simulation**.
   The notes show your organization's per-minute rate.

The wizard shows two statuses: **Simulation container** and `viam-server`.
Most simulations are ready in a few minutes.
When many simulations start at once, waiting for a GPU can take 10 to 20 minutes, and Viam keeps trying for up to an hour.
You can leave the page: if the container takes longer than a warm start, Viam emails you when it's up.
When `viam-server` comes online, the machine shows as live.

If a simulation is already running for the machine, the wizard offers **View running simulation** instead of starting a second one.

{{% /tab %}}
{{% tab name="Your own GPU" %}}

The module's first run installs the system libraries Isaac Sim needs, an NVIDIA driver if none is present, and Isaac Sim itself.
The Isaac Sim download is over 10GB, so give the first run more time than `viam-server`'s default of 1 hour.

1. In the [Viam app](https://app.viam.com), open your machine's **CONFIGURE** tab and switch to **JSON** mode.
1. Add the module to the `modules` array, with a longer first-run timeout:

   ```json
   {
     "type": "registry",
     "name": "viam-labs_isaac-sim",
     "module_id": "viam-labs:isaac-sim",
     "version": "latest",
     "first_run_timeout": "2h0m0s"
   }
   ```

   If Isaac Sim is already installed on the computer, add `"env": { "ISAAC_SIM_PATH": "<isaac-sim-directory>" }` to the entry instead, where `<isaac-sim-directory>` contains `python.sh`.
   The first run then skips the install.

1. Click **Save**, and wait for the first run to finish in the machine's logs.
1. If the first run installed an NVIDIA driver, reboot the computer before you go on.

{{% /tab %}}
{{< /tabs >}}

## 2. Add the Isaac Sim world and a starter cell {#add-the-isaac-sim-world-and-a-starter-cell}

The starter cell is a world, a UR20 arm at the origin, and a camera that looks at the arm.

1. On the machine's **CONFIGURE** tab, switch to **JSON** mode.
1. Add these components to the `components` array:

   ```json
   {
     "name": "sim-world",
     "api": "rdk:component:generic",
     "model": "viam-labs:isaac-sim:world",
     "attributes": {
       "headless": true
     }
   },
   {
     "name": "my-arm",
     "api": "rdk:component:arm",
     "model": "viam-labs:isaac-sim:arm",
     "frame": { "parent": "world" },
     "attributes": {
       "world": "sim-world",
       "asset": "ur20"
     }
   },
   {
     "name": "scene-cam",
     "api": "rdk:component:camera",
     "model": "viam-labs:isaac-sim:camera",
     "frame": {
       "parent": "world",
       "translation": { "x": 2000, "y": 2000, "z": 2000 }
     },
     "attributes": {
       "world": "sim-world",
       "target": [0, 0, 0.5],
       "width": 1280,
       "height": 720
     }
   }
   ```

   Each component's `frame` places it in the scene, in millimeters from the world origin.
   The camera's `target` is the point it looks at, in meters.

1. In the cloud, also add the module to the `modules` array.
   If you added it in step 1, skip this.

   ```json
   {
     "type": "registry",
     "name": "viam-labs_isaac-sim",
     "module_id": "viam-labs:isaac-sim",
     "version": "latest"
   }
   ```

1. Click **Save**.

For every attribute and the other models, such as grippers, depth cameras, and bases, see the [Isaac Sim module README](https://github.com/viam-modules/viam-isaac-sim#readme).
To change the scene, see [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/).

## 3. Wait for the world to start {#wait-for-the-world-to-start}

The world starts Isaac Sim when you save, and the arm and camera wait for it.
The first boot can take several minutes while Isaac Sim builds its caches.

1. Open the machine's **LOGS** tab.
1. Look for `booting isaac sim` from the module, followed by `isaac sim world ready`.

Until `isaac sim world ready` appears, the arm and camera aren't ready, and their cards on the **CONTROL** tab may show errors.

## 4. Connect your code {#connect-your-code}

1. On the machine's **CONNECT** tab, select **Python** and copy the code sample.
   It includes the machine's address and an API key.
1. Save it on your laptop as `connect.py` and run it:

   ```sh {class="command-line" data-prompt="$"}
   python3 connect.py
   ```

The sample prints the machine's resources, including `my-arm` and `scene-cam`.

## 5. Verify the cell {#verify-the-cell}

1. On the machine's **CONTROL** tab, open the `scene-cam` card.
   The camera shows the UR20 arm on the ground plane.
1. On your laptop, save this script as `move_arm.py`.
   Replace `<machine-address>`, `<api-key>`, and `<api-key-id>` with the values from the **CONNECT** tab.

   ```python
   import asyncio

   from viam.components.arm import Arm, JointPositions
   from viam.robot.client import RobotClient


   async def main():
       opts = RobotClient.Options.with_api_key(
           api_key="<api-key>", api_key_id="<api-key-id>"
       )
       machine = await RobotClient.at_address("<machine-address>", opts)
       arm = Arm.from_robot(machine, "my-arm")

       joints = await arm.get_joint_positions()
       print("before:", list(joints.values))

       # Rotate the base joint 45 degrees.
       values = list(joints.values)
       values[0] += 45
       await arm.move_to_joint_positions(JointPositions(values=values))

       joints = await arm.get_joint_positions()
       print("after:", list(joints.values))
       await machine.close()


   asyncio.run(main())
   ```

1. Run it:

   ```sh {class="command-line" data-prompt="$"}
   python3 move_arm.py
   ```

The script prints the joint positions before and after the move, with the first joint 45 degrees further around, and the arm turns in the `scene-cam` image.

## Manage a cloud simulation {#manage-a-cloud-simulation}

A cloud simulation keeps running, and billing, until you stop it or it sits idle for an hour.
A lifetime limit doesn't always apply, so stop a simulation when you're done with it.

### Check a simulation's status {#check-a-simulations-status}

On the machine's page, open the status menu at the top.
It shows the simulation's state, such as **Simulation provisioning**, **Simulation starting up**, **Simulation started**, or **Simulation terminated**, and why a stopped simulation stopped.

### Stop a simulation {#stop-a-simulation}

On the machine's page, click **Stop sim**.
The status changes to **Simulation terminated**, and the per-minute charges stop.
On a machine with more than one simulated part, the button is **Stop all sims**; to stop one part, use **Stop sim** in that part's actions menu.

Deleting the machine also ends its simulation.

### Restart a simulation {#restart-a-simulation}

After a simulation stops, click **Restart sim** on the machine's page.
The simulation starts again from the machine's saved configuration, billed per minute, and the status moves through **Simulation provisioning** to **Simulation started**.

You can also check, start, and stop a simulation from the Config AI assistant or the Viam MCP server.
See the simulation tools in [MCP server](/reference/mcp/#simulation-tools).

## Troubleshooting {#troubleshooting}

{{% expand "The simulation fails to start" %}}

The wizard shows **Couldn't start the simulation** with the reason, and a **Try again** button.
Common reasons:

- No GPU capacity is available right now, or no GPU-enabled machine was found within an hour.
  Click **Try again** in a few minutes.
- Your organization has reached its limit of active simulations.
  Stop a simulation on another machine, then try again.

{{% /expand %}}

{{% expand "\"Simulation environments are not enabled for this organization\"" %}}

The Config AI assistant or the MCP server returns this when cloud simulation isn't available to the machine's organization.
If you don't see the simulate option, simulation isn't turned on for your organization yet.

{{% /expand %}}

{{% expand "Isaac Sim crashes on startup with a librtx error" %}}

On your own GPU, an NVIDIA driver from the 590 branch or newer crashes Isaac Sim's RTX renderer on startup, with an error from `librtx.scenedb.plugin.so`.
Install the 580 driver and reboot:

```sh {class="command-line" data-prompt="$"}
sudo apt-get install -y nvidia-driver-580 && sudo reboot
```

{{% /expand %}}

{{% expand "The module times out on first run" %}}

On your own GPU, the Isaac Sim download is over 10GB, and the first run can take longer than `viam-server`'s default first-run timeout of 1 hour.
Set `"first_run_timeout": "2h0m0s"` on the module's entry in `modules`, as in [step 1](#start-the-machine), and save.

If the logs instead show `isaac sim did not boot within`, Isaac Sim installed but took longer to boot than the world allows.
Raise `boot_timeout_sec` on the world component; it defaults to 300 seconds.

{{% /expand %}}

{{% expand "The simulation stopped on its own" %}}

A cloud simulation stops automatically after an hour in which no component moves, to stop the charges.
It can also be shut down by its cloud host, for example after a maximum run time.
The status menu says which happened.
Click **Restart sim** to start it again.

{{% /expand %}}

## Advanced: View the Isaac Sim viewport {#advanced-view-the-isaac-sim-viewport}

On your own GPU, you can watch the full Isaac Sim viewport instead of a camera.
The world streams it by default when `headless` is `true`.

1. Install NVIDIA's [Isaac Sim WebRTC Streaming Client](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html) on your laptop.
1. Make sure your laptop can reach the simulation computer on TCP port 49100 and UDP port 47998.
   The streaming client uses these ports, and you can't change them.
1. In the client, enter the simulation computer's IP address, without a port.

If the computer has more than one network interface, set `livestream_public_ip` on the world component to the address your laptop can reach.

## What's next {#whats-next}

- [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/): add objects and cameras, use your own robot, and reload the scene after edits.
- [How simulation works](/set-up-a-machine/simulate/how-simulation-works/): understand what changes between a simulated machine and a real one.
- [Move a simulated machine to real hardware](/set-up-a-machine/simulate/move-to-real-hardware/): run the code you wrote here on your real robot.
