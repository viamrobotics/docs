---
title: "Phase 3: Record demonstrations"
linkTitle: "3. Record demonstrations"
type: "docs"
slug: "record-demonstrations"
weight: 30
description: "Add a capture control sensor, open the capture-control webapp, and record about 50 teleoperated stacking demonstrations as data sequences."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 3
phase_total: 7
time_estimate: "90 minutes"
prev: "/tutorials/xarm-act-stacking/configure-the-cell/"
next: "/tutorials/xarm-act-stacking/review-and-build-a-dataset/"
languages: ["python"]
capabilities: ["data-capture", "sequences", "teleop", "viam-apps", "docs"]
diataxis: tutorial
draft: true
---

In this phase you teach by showing. You teleoperate the xArm6 through about 50 stacks, and the capture-control webapp records each one as an episode. Each episode becomes one data sequence of the follower's joints, gripper, and both cameras. You set up capture first, then practice, then record.

## Add the capture control sensor

A capture control sensor tells the data management service what to capture and when. Add a sensor named `demo-capture` to your machine config. It's a sensor from the `viam:capture-control` module, model `viam:capture-control:capture-control-sensor`. It lists the four things the policy learns from:

```json
{
  "name": "demo-capture",
  "api": "rdk:component:sensor",
  "model": "viam:capture-control:capture-control-sensor",
  "attributes": {
    "resources": [
      { "resource_name": "xarm", "method": "JointPositions" },
      { "resource_name": "xarm-gripper", "method": "DoCommand" },
      { "resource_name": "wrist-cam", "method": "GetImages" },
      { "resource_name": "scene-cam", "method": "GetImages" }
    ]
  }
}
```

A capture control entry can't carry an input, so the gripper's `DoCommand` needs its own capture config. Add this to the `xarm-gripper` component, and keep the sensor entry above:

```json
{
  "name": "xarm-gripper",
  "api": "rdk:component:gripper",
  ...,
  "service_configs": [
    {
      "type": "data_manager",
      "attributes": {
        "capture_methods": [
          {
            "method": "DoCommand",
            "capture_frequency_hz": 10,
            "additional_params": { "docommand_input": { "get": true } }
          }
        ]
      }
    }
  ]
}
```

The input `{"get": true}` returns the gripper's state. For the capture config fields, see the [data capture reference](/data/reference/#capture-and-sync-configuration).

<!-- TODO(dep): confirm the sensor override keeps the gripper's additional_params docommand_input -->

Every listed resource runs at the same 10 Hz rate, because training rejects sequences with mixed rates. While the sensor lists a component, the sensor's frequency overrides that component's own capture frequency. It leaves the rest of your component configuration unchanged. The webapp sends the rate from its **FPS** (frames per second) session setting, which defaults to 10. Leave **FPS** at 10. Don't set `default_capture_frequency_hz` on the sensor. A nonzero default captures continuously, even between episodes.

For every attribute and command, see [Start and stop capture on demand](/data/capture-sync/capture-on-demand/).

## Connect it to the data manager

Your machine has no data management service yet, so add one. Point it at the sensor with `capture_control_sensor`, and add the sensor to its `depends_on`:

```json
{
  "name": "data-manager",
  "api": "rdk:service:data_manager",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "capture_control_sensor": { "name": "demo-capture", "key": "overrides" }
  },
  "depends_on": ["demo-capture"]
}
```

The module turns capture off between recordings, so nothing is captured outside an episode.

## Open the capture-control webapp

The webapp is how you start and stop episodes. Use either option:

- Serve it from the machine. Add the `viam-labs:capture-control-webapp` module, then add a `generic` service named `capture-app` with the model `viam-labs:capture-control:webapp`. It serves on port 8888 by default, so open `http://<machine-ip>:8888`.
- Open the hosted app at `https://capture-control-webapp_viam-labs.viamapplications.com`.

  <!-- TODO(dep): confirm the hosted URL is live -->

The app always signals through `app.viam.com`, so the machine and your browser need internet access.

Under **Robot setup**, choose the home set: `follower-home` and `leader-home`. The app finds the teleop service on its own. It uses any generic service that answers `{"command": "status"}` with a boolean `running`, and it needs exactly one. Your `teleop` service from Phase 2 qualifies.

{{< checkpoint >}}
Under **Robot setup**, the app lists `teleop` as the teleop service, and pressing **T** starts and stops teleop. If the app finds no teleop service, or more than one, check that exactly one generic service answers `status`.
{{< /checkpoint >}}

## Add the task

Add the task `stack the red block on the blue block` as task 1. The number keys 1 to 9 pick the task for the next episode.

Each episode is tagged `task:<task>`, `session:<id>`, and `fps:<fps>`. The `<task>` is whichever task was active when the episode started. Training reads the `task:` tag as the instruction the policy learns to follow.

## Practice before you record

Before you record, do three or four stacks with teleop on and no session running. Repeat until your motion is smooth. Nothing is captured outside an episode, so practice leaves no data. Don't press **Enter** yet.

## What makes a good demonstration

The policy copies what you show it, so consistency matters more than speed. For every episode:

- Use one strategy: approach from above, grasp, lift, move, lower, release.
- Move smoothly and steadily, with no pauses or hesitation.
- Start every episode from home.
- Vary the block start positions across the mat's zones, about evenly.
- Keep people and extra objects out of the scene camera's view.
- Discard a botched episode rather than "fixing" it mid-stack.

## Record about 50 episodes

The webapp's default session size is already 10 episodes. Record in sessions of that size, with a break between sessions. Use these keys:

| Key       | Action                                                                |
| --------- | --------------------------------------------------------------------- |
| **Enter** | Start the session.                                                    |
| **Space** | End the episode and start the next one.                               |
| **H**     | Home both arms between episodes. It doesn't work while recording.     |
| **T**     | Toggle teleop. While recording, it stops teleop and ends the episode. |
| **Esc**   | Stop the session.                                                     |

After **H**, teleop stays off, and the next episode waits for **Space**. Take hold of the leader, then press **T** once your hand is on it.

<!-- ASSET webapp-recording (SCREENSHOT): the capture-control webapp mid-session, showing the active task, the episode counter, and the live scene-cam view -->

{{< checkpoint >}}
On the Viam app's **DATA** page, the machine shows about 50 sequences tagged `task:stack the red block on the blue block`. To view sequences, see [Sequences](/data/sequences/#view-sequences).
{{< /checkpoint >}}

{{< workshop-nav >}}
