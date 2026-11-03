---
title: "Phase 6: Deploy the policy"
linkTitle: "6. Deploy the policy"
type: "docs"
slug: "deploy-the-policy"
weight: 60
description: "Deploy your trained ACT policy with the policy and controller services, then watch the xArm stack a block on its own."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 6
phase_total: 7
time_estimate: "60 minutes"
prev: "/tutorials/xarm-act-stacking/train-a-policy/"
next: "/tutorials/xarm-act-stacking/evaluate-and-iterate/"
languages: ["python"]
capabilities: ["ml-models", "hw-arm", "module-registry", "docs"]
diataxis: tutorial
draft: true
---

You have a trained `xarm-stacking` model. Now you put it in the loop. You add two services: one that runs the model, and one that reads the cameras, asks the model what to do, and moves the arm. This is the second milestone. When you finish, you press start and the xArm stacks the red block on the blue one with no human input.

This phase is the most exacting in the workshop. The controller must feed the policy exactly what it saw in training: the same cameras, the same joint order, the same units, and the same gripper scale. Most failures here come from one of those not matching.

## Two services, one loop

The `viam-labs:vla` module provides two services:

- `act-policy` (`viam-labs:vla:policy`) runs the model. It knows nothing about the robot. You send it images, joint state, and a task string, and it returns a chunk of actions.
- `act-controller` (`viam-labs:vla:controller`) runs the loop. It reads the cameras and joints, asks the policy for a chunk of actions, clamps them, and moves the arm.

They're split so you can test the policy with no robot attached, and develop the control loop with no GPU.

## Stop teleop first

Only one thing can drive the xArm at a time, so turn teleop off before you start the controller.

1. Open the `teleop` service's DoCommand test panel and send `{"command": "stop"}`.
2. Open the **CONTROL** tab and set `follower-home` to position 2 ("go to") to home the xArm.
3. Move the leader arm out of the workspace. The policy only sees the follower, but you don't want to knock the leader while the xArm moves.

## Add the policy

Add the `viam-labs:vla` module and the `act-policy` service. The service points at your trained model through a registry package.

1. Add the module and pin its version:

   <!-- TODO(dep): pinned viam-labs:vla version that matches the training container's LeRobot commit -->

   ```json
   {
     "type": "registry",
     "name": "viam-labs_vla",
     "module_id": "viam-labs:vla",
     "version": "<pinned-version>"
   }
   ```

   Pin the version rather than using `latest`. The policy loads a LeRobot checkpoint, and the module's LeRobot version has to match the one that trained your model.

2. Add the model as a package, pinned to the version your training job produced. In your machine's JSON config, add a `packages` entry:

   ```json
   {
     "packages": [
       {
         "name": "xarm-stacking",
         "package": "<org-id>/xarm-stacking",
         "version": "<model-version>",
         "type": "ml_model"
       }
     ]
   }
   ```

   Replace `<org-id>` with your organization ID and `<model-version>` with the version from Phase 5. For how packages resolve, see [Configure a vision service](/vision/configure/).

3. Add the policy service:

   ```json
   {
     "name": "act-policy",
     "api": "rdk:service:generic",
     "model": "viam-labs:vla:policy",
     "attributes": {
       "model_path": "${packages.ml_model.xarm-stacking}",
       "device": "auto"
     }
   }
   ```

   viam-server replaces `${packages.ml_model.xarm-stacking}` with the real path to the downloaded model before the module sees the config. `device` defaults to `auto`, which tries `cuda`, then `mps`, then `cpu`. Leave it on `auto` unless you need to force one. Set it to `cuda`, `mps`, or `cpu` to pick a device yourself.

4. Save. The model downloads and loads in the background. In the `act-policy` DoCommand test panel, send this until `state` is `ready`:

   ```json
   { "command": "status" }
   ```

   ```json
   { "state": "ready", "error": "" }
   ```

   `state` is one of `idle`, `loading`, `ready`, or `failed`. If it's `failed`, `error` says why.

## Ask what the policy needs

The policy knows what it was trained on. Ask it:

```json
{ "command": "specs" }
```

The response is long. These fields matter for the controller:

```json
{
  "policy_type": "act",
  "action_dim": 7,
  "state_dim": 7,
  "image_feature_keys": [
    "observation.images.<key-1>",
    "observation.images.<key-2>"
  ],
  "n_action_steps": 100
}
```

The values above are what you should expect. Your keys and numbers come from your checkpoint.

- `image_feature_keys` lists the cameras the policy expects. You have two: the scene camera and the wrist camera. The controller refuses to start unless you map every key.
- `state_dim` is the length of the state the policy reads. For this workshop it's 7: six joints plus the gripper.
- `action_dim` is the length of the action the policy emits. It's 7 as well.

<!-- TODO(dep): confirm specs output for the xarm-stacking checkpoint: image_feature_keys names, state_dim 7, action_dim 7 -->

The keys depend on how your training job named its cameras, and the policy doesn't say which physical camera each key held. In the `xarm-stacking` training, the first camera was `scene-cam` and the second was `wrist-cam`, so map the keys in that order. If the key names don't make the order obvious, a swapped mapping produces confident but wrong motion: the arm moves smoothly in the wrong direction. If you see that, swap the two entries in `cameras`.

## Add the controller

Add the controller service. Replace each `<...-key>` with a key from `image_feature_keys`:

<!-- TODO(dep): xArm gripper open/closed native values, verified on hardware -->

```json
{
  "name": "act-controller",
  "api": "rdk:service:generic",
  "model": "viam-labs:vla:controller",
  "attributes": {
    "policy_service": "act-policy",
    "arm": "xarm",
    "cameras": {
      "<scene-key>": "scene-cam",
      "<wrist-key>": "wrist-cam"
    },
    "state_joint_indices": [0, 1, 2, 3, 4, 5],
    "gripper": {
      "type": "do_command",
      "name": "xarm-gripper",
      "read_key": "pos",
      "open_value": 840.0,
      "closed_value": 2.0
    },
    "task": "stack the red block on the blue block",
    "fps": 10.0,
    "mode": "async",
    "actions_per_chunk": 12,
    "state_units": "degrees",
    "action_units": "degrees",
    "safety": {
      "max_vel_degs_per_sec": 60.0,
      "max_start_delta_degs": 15.0,
      "stop_on_error": true
    }
  }
}
```

What each field does:

- `policy_service` and `arm` name the policy and the xArm.
- `cameras` maps each image feature key from `specs` to a camera. Every key must be covered.
- `state_joint_indices` maps the arm's joints, base to wrist, onto the state positions the checkpoint expects. These are indices, not names. The six xArm joints are `0` to `5`.
- `gripper` adds the seventh channel. `read_key`, `open_value`, and `closed_value` must match what you used in training. The controller turns the reading into a value from `0.0` (open) to `1.0` (closed), the same scale training used. Use the open and closed values from Phase 5. The values above are the ones from Phase 5's table, so if you changed them there, change them here.
- `task` is the instruction. It must match the `task:` tag you recorded, exactly. You can override it per run with `{"command": "start", "task": "..."}`.
- `fps` is the loop rate. Keep it at `10.0` to match training.
- `mode` and `actions_per_chunk` are covered in the next section.
- `state_units` and `action_units` are the units the checkpoint was trained in. Viam arms always report and accept degrees. This checkpoint trained on the xArm's joint values in degrees, so `"degrees"` is right. Both default to `"degrees"`, so they're shown here to make the choice visible. Set them to `"radians"` only if your training data was in radians.
- `safety.max_vel_degs_per_sec` caps joint speed. The controller derives a per-tick limit from it: `60.0 / 10.0 = 6` degrees per tick. `max_start_delta_degs` makes `start` refuse if the policy's first action is more than 15 degrees from where the arm is now. `stop_on_error` halts the loop if a camera read or the policy call fails.

<!-- TODO(dep): confirm xArm joint units in training data are degrees, and per-joint safety.joint_limits_degs for the xArm6 -->

`safety.joint_limits_degs` is optional. Without it, the controller logs a warning at start and relies on the xArm driver for joint limits.

## Why `actions_per_chunk` matters

ACT predicts 100 actions per chunk by default. At 10 Hz, that's about 10 seconds of motion with no new camera input. The arm would execute a long plan blind, and the end of the chunk is the least accurate part.

`actions_per_chunk` executes only the first few actions of each chunk, then asks again. The arm reacts to what the cameras see every second or so instead of every 10 seconds. Some points to know:

- It only works under `mode: "async"`. In `async` mode, the next chunk is inferred while the current one runs. Under `sequential` mode, the arm stops and waits for every inference.
- Its floor is `ceil(avg_latency_s × fps)`. If inference takes 1 second at 10 Hz, the floor is 10. Below the floor, the queue empties before the next chunk arrives and the arm holds still.
- The checkpoint's `n_action_steps` doesn't shorten the executed chunk. The controller asks for a whole chunk regardless, so you need `actions_per_chunk` to shorten it.
- Leave `queue_threshold` unset. The controller derives it from `actions_per_chunk`.

To tune it:

1. Start with `12`.
2. Run for a minute and read `avg_latency_s` and `starved_ticks` from `status`.
3. If `starved_ticks` keeps rising, raise `actions_per_chunk` toward `ceil(avg_latency_s × fps)` or above, or lower the latency.
4. If the arm seems to act on old information, lower it, but not below the floor.

<!-- TODO(dep): recommended actions_per_chunk for ACT on the workshop GPU, measured -->

## Run it

First, learn the way out. This command halts the loop, and the arm stays where it is:

```json
{ "command": "stop" }
```

Send it to `act-controller` any time something looks wrong. The xArm also has a physical emergency stop. Keep it within reach for every run, and use it before the arm hits anything.

Now run it.

1. Reset the blocks into one of your mat zones, with the red and blue blocks in the starting positions you used when recording.
2. Make sure the arm is at home and nothing is in its path.
3. In the `act-controller` DoCommand test panel, send:

   ```json
   { "command": "start" }
   ```

   `start` returns immediately. It doesn't wait for the arm to move, so watch the arm and poll `status` to see what happened.

4. Watch the arm. Keep a hand near the emergency stop.

## Read `status`

While the loop runs, send `{"command": "status"}` to `act-controller`. These fields matter:

| Field           | What it tells you                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `state`         | `idle`, `waiting_for_policy`, `running`, `stopped`, or `error`.                                                                |
| `measured_fps`  | The actual loop rate. It should track `fps`. Well below it means inference isn't keeping up.                                   |
| `avg_latency_s` | How long one policy call takes. Use it to set the floor for `actions_per_chunk`.                                               |
| `clamp_counts`  | How many times the safety limits trimmed an action, split into `delta`, `limit`, and `gripper`. Non-zero counts mean trimming. |
| `starved_ticks` | Ticks where the arm held still with an empty queue. A steadily rising value means the next chunk isn't arriving in time.       |
| `last_error`    | The last failed tick's error. It stays set even if the loop kept going.                                                        |

Check `clamp_counts` first. It should stay near zero. A count that keeps climbing almost always means wrong units or wrong joint order, not a safety margin doing its job.

{{< checkpoint >}}
From a fresh block layout, send `{"command": "start"}` to `act-controller`. The xArm stacks the red block on the blue one with no human input.
{{< /checkpoint >}}

## Troubleshooting

<!-- TODO(dep): remove or reword when the ufactory gripper gets non-blocking writes -->

| Symptom                                            | Likely cause                                                                                                            | Fix                                                                                                                                       |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| The arm moves the wrong way or by the wrong amount | Wrong units. A mismatch usually shows up as a climbing `clamp_counts.delta`.                                            | Set `state_units` and `action_units` to match the training data, then check `state_joint_indices`.                                        |
| The gripper never closes                           | `open_value` and `closed_value` are reversed, or don't match training.                                                  | Set them to the values from Phase 5. Check `gripper` in `clamp_counts`.                                                                   |
| Jerky motion                                       | `measured_fps` is below `fps`, so inference or image handling is too slow.                                              | Check `measured_fps` and `avg_latency_s`. Confirm `mode` is `async`, `device` isn't `cpu`, and `actions_per_chunk` isn't below its floor. |
| The arm freezes for seconds at a grasp             | The xArm gripper's `set` blocks until the jaw settles, up to about 10 seconds. A 10 Hz loop can't opt out of that wait. | Expect a pause at each grasp for now.                                                                                                     |
| It works only from one start zone                  | The demonstrations didn't vary enough.                                                                                  | Record more varied starts in [Phase 7](/tutorials/xarm-act-stacking/evaluate-and-iterate/).                                               |

{{< workshop-nav >}}
