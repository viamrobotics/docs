---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake gripper model. Fake gripper."
tags: ["gripper", "components"]
icon: true
images: ["/icons/components/gripper.svg"]
aliases:
  - "/operate/reference/components/gripper/fake/"
  - "/components/gripper/fake/"
  - "/reference/components/gripper/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: Rand
---

Configure a `fake` gripper to test implementing a gripper on your machine without any physical hardware:

{{< tabs name="Configure a Fake Gripper" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gripper-name>",
  "model": "fake",
  "api": "rdk:component:gripper",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

No attributes are available for fake grippers.
See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gripper/fake/gripper.go) for API call return specifications.

## Configure physical properties through the frame

The `fake` gripper has no attribute for length or collision volume. The motion
planner reads both from the component's `frame` field. Set `frame.translation.z`
to the offset from the arm's tool flange to the tool center point (TCP) you
want the planner to drive to, and `frame.geometry` to the collision shape.

For a typical 120 mm parallel-jaw gripper bolted directly to the arm flange:

```json
{
  "name": "my-fake-gripper",
  "model": "fake",
  "api": "rdk:component:gripper",
  "attributes": {},
  "frame": {
    "parent": "my-arm",
    "translation": { "x": 0, "y": 0, "z": 120 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    },
    "geometry": {
      "type": "box",
      "x": 80,
      "y": 80,
      "z": 120,
      "translation": { "x": 0, "y": 0, "z": -60 }
    }
  }
}
```

`frame.translation.z: 120` puts the frame origin at the TCP, 120 mm out from
the arm flange. `geometry.translation.z: -60` sits the box's center halfway
back toward the flange, so the box covers the gripper body from the flange to
the TCP.

Why this matters: motion planning, reachability checks, and approach and
retract poses all drive the TCP, not the tool flange, to a target pose. With
no `frame`, the planner has no TCP defined and treats the gripper as a
zero-volume point at the flange.

Symptoms if wrong: motion plans validate, then the physical gripper tip lands
short or long of the target, or the planner returns "outside workspace" for
poses the arm can clearly reach.

For the broader pattern and worked examples for cameras and IMUs, see
[When the model has no physical-extent attribute](/motion-planning/frame-system/overview/#when-the-model-has-no-physical-extent-attribute).

{{< readfile "/static/include/components/test-control/gripper-control.md" >}}
