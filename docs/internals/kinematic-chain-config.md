---
title: "Configure Complex Kinematic Chains"
linkTitle: "Complex Kinematic Chains"
weight: 70
type: "docs"
description: "How to write files defining kinematic parameters to configure intermediate reference frames for components with complex kinematic chains."
tags: ["slam", "services"]
# SMEs: Motion
---

Many components have complex kinematic chains and require an additional set of intermediate reference frames to use Viam's [Motion service](/machine/services/motion/).

- For example, an [arm](/machine/components/arm/) has a reference frame originating where the arm is attached to a surface, but it also has links and joints whose frames of reference matter when attempting to move the arm to a [pose](/internals/orientation-vector/) with [`MoveToPosition()`](/machine/components/arm/#movetoposition).

If you want to implement a component with a complex kinematic chain that is not already built into the RDK, you need to add a file to your driver that details the attachment of the intermediate reference frames on the component.

This file can be a <file>.json</file> file in the [same format as Viam's built-in arm drivers](https://github.com/viamrobotics/rdk/blob/main/machine/components/arm/xarm/xarm6_kinematics.json), or an [<file>.URDF</file> file](https://industrial-training-master.readthedocs.io/en/melodic/_source/session3/Intro-to-URDF.html).

## Kinematic parameters

Viam supports two formats for supplying kinematic parameters to configure intermediate reference frames for a kinematic chain, defined as `"kinematic_param_type"`:

1. [Spatial Vector Algebra (SVA)](https://drake.mit.edu/doxygen_cxx/group__multibody__spatial__vectors.html): supplying reference frame information for each `link` and each `joint`.
2. [Denavit-Hartenberg (DH)](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters) parameters.

{{% alert title="Info" color="info" %}}

Of the two methods, we prefer Spacial Vector Algebra over Denavit-Hartenberg because it allows you to specify link frames arbitrarily, which DH parameters are unable to guarantee.
Additionally, if you are making your own robot and defining new drivers, incorrect SVA parameters are easier to troubleshoot than incorrect DH parameters.

{{% /alert %}}

This is an example <file>.json</file> configuration as used by Viam's [Universal Robots](https://www.universal-robots.com/) [arm driver](https://github.com/viamrobotics/rdk/blob/main/machine/components/arm/universalrobots/ur5e.json):

{{< tabs name="Kinematic Parameter Types" >}}
{{% tab name="SVA" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "UR5e",
  "kinematic_param_type": "SVA",
  "links": [
    {
      "id": "base_link",
      "parent": "world",
      "translation": {
        "x": 0,
        "y": 0,
        "z": 162.5
      },
      "geometry": {
        "x": 120,
        "y": 120,
        "z": 260,
        "translation": {
          "x": 0,
          "y": 0,
          "z": 130
        }
      }
    },
    {
      "id": "shoulder_link",
      "parent": "shoulder_pan_joint",
      "translation": {
        "x": 0,
        "y": 0,
        "z": 0
      }
    },
    {
      "id": "upper_arm_link",
      "parent": "shoulder_lift_joint",
      "translation": {
        "x": -425,
        "y": 0,
        "z": 0
      },
      "geometry": {
        "x": 550,
        "y": 150,
        "z": 120,
        "translation": {
          "x": -215,
          "y": -130,
          "z": 0
        }
      }
    },
    {
      "id": "forearm_link",
      "parent": "elbow_joint",
      "translation": {
        "x": -392.2,
        "y": 0,
        "z": 0
      },
      "geometry": {
        "x": 480,
        "y": 120,
        "z": 100,
        "translation": {
          "x": -190,
          "y": 0,
          "z": 0
        }
      }
    },
    {
      "id": "wrist_1_link",
      "parent": "wrist_1_joint",
      "translation": {
        "x": 0,
        "y": -133.3,
        "z": 0
      },
      "geometry": {
        "x": 90,
        "y": 130,
        "z": 130,
        "translation": {
          "x": 0,
          "y": -110,
          "z": 0
        }
      }
    },
    {
      "id": "wrist_2_link",
      "parent": "wrist_2_joint",
      "translation": {
        "x": 0,
        "y": 0,
        "z": -99.7
      },
      "geometry": {
        "x": 80,
        "y": 150,
        "z": 100,
        "translation": {
          "x": 0,
          "y": 0,
          "z": -100
        }
      }
    },
    {
      "id": "ee_link",
      "parent": "wrist_3_joint",
      "translation": {
        "x": 0,
        "y": -99.6,
        "z": 0
      },
      "orientation": {
        "type": "ov_degrees",
        "value": {
          "x": 0,
          "y": -1,
          "z": 0,
          "th": 90
        }
      }
    }
  ],
  "joints": [
    {
      "id": "shoulder_pan_joint",
      "type": "revolute",
      "parent": "base_link",
      "axis": {
        "x": 0,
        "y": 0,
        "z": 1
      },
      "max": 360,
      "min": -360
    },
    {
      "id": "shoulder_lift_joint",
      "type": "revolute",
      "parent": "shoulder_link",
      "axis": {
        "x": 0,
        "y": -1,
        "z": 0
      },
      "max": 360,
      "min": -360
    },
    {
      "id": "elbow_joint",
      "type": "revolute",
      "parent": "upper_arm_link",
      "axis": {
        "x": 0,
        "y": -1,
        "z": 0
      },
      "max": 180,
      "min": -180
    },
    {
      "id": "wrist_1_joint",
      "type": "revolute",
      "parent": "forearm_link",
      "axis": {
        "x": 0,
        "y": -1,
        "z": 0
      },
      "max": 360,
      "min": -360
    },
    {
      "id": "wrist_2_joint",
      "type": "revolute",
      "parent": "wrist_1_link",
      "axis": {
        "x": 0,
        "y": 0,
        "z": -1
      },
      "max": 360,
      "min": -360
    },
    {
      "id": "wrist_3_joint",
      "type": "revolute",
      "parent": "wrist_2_link",
      "axis": {
        "x": 0,
        "y": -1,
        "z": 0
      },
      "max": 360,
      "min": -360
    }
  ]
}
```

{{< /tab >}}
{{% tab name="DH" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "UR5e",
  "kinematic_param_type": "DH",
  "dhParams": [
    {
      "id": "base",
      "parent": "world",
      "a": 0,
      "d": 162.5,
      "alpha": 1.57079632679,
      "max": 360,
      "min": -360
    },
    {
      "id": "shoulder",
      "parent": "base",
      "a": -425,
      "d": 0,
      "alpha": 0,
      "max": 360,
      "min": -360
    },
    {
      "id": "elbow",
      "parent": "shoulder",
      "a": -392.2,
      "d": 0,
      "alpha": 0,
      "max": 180,
      "min": -180
    },
    {
      "id": "wrist_1",
      "parent": "elbow",
      "a": 0,
      "d": 133.3,
      "alpha": 1.57079632679,
      "max": 360,
      "min": -360
    },
    {
      "id": "wrist_2",
      "parent": "wrist_1",
      "a": 0,
      "d": 99.7,
      "alpha": -1.57079632679,
      "max": 360,
      "min": -360
    },
    {
      "id": "wrist_3",
      "parent": "wrist_2",
      "a": 0,
      "d": 99.6,
      "alpha": 0,
      "max": 360,
      "min": -360
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Info" color="info" %}}

These reference frames are ingested by the frame system.
They are not exposed in the [client SDKs](/program/), with one exception.
If your resource is an [arm component](/machine/components/arm/), you can use the [`GetKinematics()`](/machine/components/arm/#getkinematics) method to access its kinematics information.

{{% /alert %}}
