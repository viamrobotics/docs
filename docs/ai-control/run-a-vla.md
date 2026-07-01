---
linkTitle: "Run a VLA model"
title: "Run a vision-language-action model"
weight: 20
layout: "docs"
type: "docs"
description: "Build a control loop that feeds a camera frame and a language prompt to a vision-language-action model, then maps the model's output to arm, base, or gripper commands with the Viam APIs."
---

A vision-language-action (VLA) model takes an image and a natural-language
instruction, such as "pick up the red block," and returns an action for a robot
to take.
Viam does not ship a built-in VLA model.
Instead, you bring your own model, either an open-weights VLA you run yourself or
a hosted foundation-model API, and connect it to your hardware through Viam.

This page shows how to assemble the control loop: capture a camera frame, send
the frame and a prompt to the model, and translate the model's output into
component commands.
The reader is expected to know the [Viam basics](/build-modules/) and to have a
machine with a camera and at least one actuator, such as an arm, base, or
gripper, already configured.

A related capability is **open-vocabulary** (or **zero-shot**) detection: a
vision model detects objects named by a text prompt, such as "coffee mug," with
no task-specific training.
Viam does not ship an open-vocabulary detector; as with the VLA model, you
deploy one yourself, typically as a vision-service module. The
[vision service](/reference/services/vision/) is then the interface that returns
its bounding boxes, which you can use either as a standalone perception step or
as an input to the VLA loop below.

## Prerequisites

{{% expand "A configured machine with a camera and an actuator" %}}

See [Supported hardware](/hardware/) to add a camera and an arm, base, or
gripper.

{{% /expand %}}

## Steps

### 1. Choose where the model runs

The model runs in one of two places, and the choice sets your control rate:

- **On the edge**, in a module on the machine or on a nearby GPU host. Edge
  inference avoids a network round trip, so it suits fast loops such as
  closed-loop base or arm control. Larger VLA models need a capable local GPU.
- **In the cloud**, behind a hosted foundation-model API. A cloud API gives you
  access to large models without local GPU hardware, at the cost of network
  latency on every call.

Weigh latency against model size for your target action rate: a 1 Hz "observe,
plan, act" loop tolerates cloud latency, while a 10 Hz visual servoing loop
needs edge inference.
For a fuller treatment of this tradeoff, see
[Inference latency](/concepts/inference-latency/).

### 2. Wrap the model as a module, or call a hosted API

Package the model so your control code can call it through a stable interface:

- **Self-hosted model:** build a [module](/build-modules/) that runs the model.
  If the model returns tensors, implement it as an
  [ML model service](/train/deploy-a-model/). If it returns structured actions or
  text, implement a
  [generic service](/reference/services/generic/) and expose the model
  through [`DoCommand`](/reference/apis/services/generic/#docommand).
- **Hosted API:** call the provider's API directly from your control code, or
  wrap that call in a generic service so the rest of your system stays
  provider-agnostic.

A generic service keeps the model behind one method:

```python {class="line-numbers linkable-line-numbers"}
from viam.services.generic import Generic

vla = Generic.from_robot(machine, "vla-model")

# Send an image and a prompt, receive a structured action.
result = await vla.do_command({
    "image": encoded_frame,     # base64 or bytes, per your module's contract
    "prompt": "pick up the red block",
})
action = result["action"]       # your module defines this shape
```

### 3. Capture a camera frame

Read the current frame from the [camera API](/reference/apis/components/camera/):

```python {class="line-numbers linkable-line-numbers"}
from viam.components.camera import Camera

camera = Camera.from_robot(machine, "camera")
frame = await camera.get_image()
```

Encode the frame in whatever format your module or API expects, such as JPEG
bytes or a base64 string.

### 4. Pass the frame and prompt to the model

Send the encoded frame together with the language instruction, using the call
from step 2.
Keep the prompt specific and stable across the loop so the model's output stays
consistent:

```python {class="line-numbers linkable-line-numbers"}
result = await vla.do_command({
    "image": encoded_frame,
    "prompt": "move the gripper above the red block and grasp it",
})
action = result["action"]
```

### 5. Map the model output to a component command

Define the mapping from the model's output to a Viam API call. The shape of the
output depends on your model, so decide on a contract and translate it
explicitly.

For an [arm](/reference/apis/components/arm/), move to a target pose:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.arm import Arm
from viam.proto.common import Pose

arm = Arm.from_robot(machine, "arm")
p = action["pose"]                       # your model output
target = Pose(x=p["x"], y=p["y"], z=p["z"],
              o_x=p["ox"], o_y=p["oy"], o_z=p["oz"], theta=p["theta"])
await arm.move_to_position(target)
```

To move the arm while avoiding obstacles, plan the motion with the
[motion service](/reference/apis/services/motion/) instead of commanding the arm
directly.

For a [base](/reference/apis/components/base/), command a velocity:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.base import Base
from viam.proto.common import Vector3

base = Base.from_robot(machine, "base")
v = action["velocity"]                   # your model output, in mm/s and deg/s
await base.set_velocity(
    linear=Vector3(x=0, y=v["forward"], z=0),
    angular=Vector3(x=0, y=0, z=v["turn"]),
)
```

For a [gripper](/reference/apis/components/gripper/), open or grasp:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper

gripper = Gripper.from_robot(machine, "gripper")
if action["grasp"]:
    await gripper.grab()
else:
    await gripper.open()
```

### 6. Mind the loop rate

Run steps 3 through 5 in a loop. Match the loop period to your model's inference
latency plus the time each command takes to execute, and leave margin so
commands do not queue up.
When inference is slower than your target action rate, either move the model to
the edge, choose a smaller model, or slow the loop to match.
See [Inference latency](/concepts/inference-latency/) for how latency shapes a
control loop.

## Next steps

- [Deploy an ML model service](/train/deploy-a-model/)
- [Run inference with the vision service](/reference/services/vision/)
- [Create a module](/build-modules/)
- [Plan motion with the motion service](/reference/apis/services/motion/)
