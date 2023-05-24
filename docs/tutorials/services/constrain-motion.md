---
title: "Add Constraints to a Motion Plan"
linkTitle: "Add Motion Constraints"
weight: 25
type: "docs"
description: "Use constraints with the Motion Service to move robot components in specific ways."
webmSrc: "/tutorials/videos/motion_armmoving.webm"
mp4Src: "/tutorials/videos/motion_armmoving.mp4"
videoAlt: "An arm moving in a plane with the Motion Service"
tags: ["arm", "gripper", "motion", "services"]
# SMEs: William S.
---

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
{{< /alert >}}

If you followed along in [part 2 of the Motion Service tutorial series](../plan-motion-with-arm-gripper), you used the [Motion Service](/services/motion) to move a robot arm and end effector to desired positions.
This tutorial builds on that and shows you how to use [constraints](/services/motion/constraints) to control the way your robot moves between its start and end position.

In this tutorial, you will learn to move an object (such as a cup of water) across a table without hitting another object, and while remaining upright.

{{< alert title="Note" color="note" >}}
Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6), but you can use any [arm model](/components/arm/).
The [full tutorial code](#full-tutorial-code) is available at the end of this page.
{{< /alert >}}

## Prerequisites

Before starting this tutorial, make sure you have the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) installed.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

Familiarize yourself with the concepts outlined in the second Motion tutorial, [Plan Motion with an Arm and a Gripper](../plan-motion-with-arm-gripper/), before continuing.
This tutorial picks up right where **Plan Motion with an Arm and a Gripper** stops, so further examples depend on having a connected robot, client and service access, and other infrastructure in place.
This also helps simplify and shorten the code examples presented below.

For a helpful recap of the code we previously added, look at [the full code sample from the prior tutorial](../plan-motion-with-arm-gripper/#full-tutorial-code).

## Configure your robot

Use the robot configuration from [the previous tutorial](../plan-motion-with-arm-gripper) for this tutorial, including the [arm](../../../components/arm/) and [gripper](../../../components/gripper/) components with [frames](../../../services/frame-system/) configured.

The Motion Service is one of the "built-in" services, so you don't need to do anything to enable it on your robot.

{{% expand "Click for an example raw JSON config." %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myArm",
      "type": "arm",
      "model": "xArm6",
      "attributes": {
        "host": "<ip-address>",
        "port": 0,
        "speed_degs_per_sec": 15,
        "acceleration_degs_per_sec_per_sec": 0
      },
      "depends_on": [],
      "frame": {
        "parent": "world",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 0
        },
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "x": 0,
            "y": 0,
            "z": 1,
            "th": 0
          }
        }
      }
    },
    {
      "name": "myGripper",
      "type": "gripper",
      "model": "fake",
      "attributes": {},
      "depends_on": [
        "myArm"
      ],
      "frame": {
        "parent": "myArm",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 90
        },
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "x": 0,
            "y": 0,
            "z": 1,
            "th": 0
          }
        },
        "geometry": {
          "x": 73,
          "y": 73,
          "z": 90,
          "translation": {
            "x": 0,
            "y": 0,
            "z": 0
          }
        }
      }
    }
  ]
}
```

{{% /expand %}}

## Configure your table

In the [previous tutorial](../plan-motion-with-arm-gripper/) you created a representation of a table in your client code.
This time, you will configure one in your robot's config.
This way, you can visualize it in the **Frame System** subtab of your robot's **Config** tab.

### Use a transform to represent a drinking cup



## Full tutorial code
