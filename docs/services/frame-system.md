---
title: "Frame System"
linkTitle: "Frame System"
summary: "Describes the Frame System, its configuration, its functionality, and its interfaces."
type: docs
weight: 45
---
# The Robot Frame System

Any robot that has been configured in Viam comes with a service we call the Frame System. 
This is an internally managed and (mostly) static storage of the reference frame of each component of a robot within a coordinate system configured by the user. 
The Frame System is especially important as it is the basis for many of Viam's other services (like motion and vision) and holds required contextual information to make use of the position and orientation readings returned by some components. 
In this page, we will explain:

* How to configure a robot's components to make use of the frame system
* How the viam server builds the frame system from the configuration information
* How to access and use reference frame information from the frame system service
* How other component and service functions implicitly utilize the frame system

## Configuration

To supply reference frame information when configuring a component in the Viam App ([https://app.viam.com](app.viam.com)), click **Add Frame** to launch the Frame group where you will enter Reference Frame details.
This opens the Frame group:

![add reference frame pane](..\img\image8.png)

The reference frame requires three pieces of information:

* Parent: The name of a parent reference frame
    - **world** is the name of a default reference frame that acts as the universal reference frame. 
  When a component would seemingly have no parent, its parent must be considered **world**.

* Translation: The coordinates that the origin of this component's reference frame has within its parent's reference frame (these units are in millimeters)
    - keep in mind that +X is forward, +Y is left, and +Z is up

* Orientation: The rotation that when applied to the axes of the parent's reference frame yields the axes of the component's reference frame
    - while this representation appears to represent an R4 Axis Angle, it is actually our own [orientation vector](https://docs.viam.com/appendix/orientation-vector/) format.
    - in the UI the type option currently controls whether to supply theta in degrees for  configuration purposes, but note that *the orientation vector stored and returned by the frame system will be in radians*.

The information mathematically operates in the following way. 
Let P be the parent's coordinate system and C be the component's coordinate system. 
To get the coordinates in P of the vector (0,0,1) as measured in C, we apply the translation and orientation (as a rotation) to the vector (0,0,1) as measured in P.

Viam recommends that you mark a sensible origin point in the physical space in which your robot will operate. 
This will be the origin point of the "world" reference frame. 
Then you can measure from the origin of either the world or a parent component to a point on the component guaranteed to be fixed to the origin to obtain the frame information for each component. 
Refer to the [Configuration Examples](#configuration-examples) section for more clarification.

### Model Configuration

Many components are non-trivial kinematic chains and require an additional set of intermediate reference frames. 
For example, a traditional arm may have a reference frame whose origin is at its base, but it also has an alternating sequence of links and joints whose frames of reference matter when attempting to move the arm to a certain pose. 
Each driver of such a component in the Viam system requires a JSON file named **Model JSON** that details the attachment of reference frames. However, that is a requirement for Viam's drivers. If you implement your own drivers, the decision whether to require Model JSON files will depend on your code.
These reference frames are ingested by the Frame System *but not exposed via gRPC call* (meaning they are unavailable for inspection by any of the SDKs)

!!! note 
    If you are using a component driver provided by Viam, the **Model JSON** should come pre-packaged. Otherwise, please refer to the [**Model JSON** section](#Model-JSON).

## How the Robot Builds the Frame System

Once configuration is complete and the server is started, the robot builds a tree of reference frames with the world as the root node. 
A <a href="https://en.wikipedia.org/wiki/Topological_sorting" target="_blank">topologically-sorted list</a>[^tsl] of the generated reference frames is printed by the server and can be seen in the server logs. 
Viam regenerates this tree in the process of [reconfiguration](https://docs.viam.com/product-overviews/fleet-management/#configurationlogging)

[^tsl]: Topological Sorting (wiki): <a href="https://en.wikipedia.org/wiki/Topological_sorting" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Topological_sorting</a>


![an example of a logged frame system](..\img\frame_sys_log_example.png)

Viam builds this tree by looking at the frame portion of each component in the robot's configuration (including those defined on any remotes) and creating two reference frames. 
* One reference frame is given the name of the component and represents the actuator or final link in the component's kinematic chain (e.g., the end of an arm, the platform of a gantry, etc.). 
* Viam creates an additional static reference frame whose translation and orientation relative to its parent is provided by the user in configuration. Viam names this reference frame with the component name and the suffix *"_origin"*. For example, "right-arm_<em>origin</em>".

As an example, let's consider an arm on a gantry.

Let our gantry be named "G" and our arm be named "A". 
We might decide that the static origin of our gantry is its zero position and specify a translation and orientation with respect to the world frame. 
The Frame System considers the reference frame with this static origin to be "G_origin" and the reference frame with its origin being the location of the platform to be "G". 
This choice is made so that when we specify the parent frame of the arm, we can simply use "G" and the Frame System will understand that the arm's parent frame is the platform of the gantry and not it's zero position used as a point of reference to the world. 
The resulting tree of reference frames could be visualized like so:

![reference frame tree](..\img\frame_tree.png)

## Configuration Examples

### Example 1: A robot arm attached to the side of a table (a component fixed to the world frame)

We can consider one corner of the table the origin of the world and measure from that point to the *base* of the arm to get the translation. 
We might consider a sensible default orientation for the arm to be the vector (0,0,1) with theta being 0. 
We can then supply this frame information when configuring the arm component, making sure that the parent is "world".

### Example 2: A robot arm attached to a gantry (a component fixed to the actuator of another component)

Here we pick the zero position of the gantry as its origin and do the measurements to wherever we have marked the origin of our world frame as in the first example. 
After configuring the gantry frame, we can configure the arm. 

The base of the arm is always at the position of the gantry, so we specify the arm's parent as the name of our gantry. 
We use the 0-vector as the translation and for the orientation we can probably use a (0,0,1) vector with a theta of 0.

## Accessing the Frame System

The [robot service](https://docs.viam.com/services/robot-service/) supplies two gRPC library functions by which to interact with the Frame System:
<ol>
<li>TransformPose</li></OL>
<ul><li>transforms a pose measured in one reference frame to the same pose as it would have been measured in another.</li></ul>
<OL START="2">
<li>FrameSystemConfig</li></OL>
<ul><li>returns a topologically sorted list of all the reference frames monitored by the frame system.</li>
<li>supplemental transforms (explained below) are merged into the tree and returned back in the result topologically sorted.</li>
</ul>


### Supplemental Transforms

One important concept in using the Frame System (as well understanding how other Viam services use the Frame System) is the concept of *Supplemental Transforms*. 
This concept exists to compensate for the fact that the Frame System maintained by the robot *only supports knowledge of components that have a part that is fixed with respect to a reference frame already in the system*.

An arm on a gantry, for example, can be managed by the Frame System directly because the base of the arm is fixed with respect to the gantry's platform, and the gantry's zero position is fixed with respect to the world reference frame.

On the other hand, an arm on a rover that is unaware of its own position cannot be configured into the frame system because the rover can move freely with respect to the world frame. A knowledgeable user could code a mobile base with an organic SLAM system able to report its own position without the need for supplementary transforms.

So, how do we deal with such components? 
One solution would be to introduce a motion tracker or a camera in combination with our [vision service](/services/vision/) as a third component. 
This component is fixed in space (making it configurable in the Frame System) and can supply the location and orientation of the rover in its own reference frame. 
This *supplemental transform* is the missing link to be able to transform a pose in the arm's reference frame to the world reference frame (or others that may exist in the frame system).

Both TransformPose and FrameSystemConfig optionally take in these supplemental transforms.

Functions of some services and components take in a WorldState parameter (e.g., ArmMoveToPosition). 
This data structure includes an entry for supplying supplemental transforms for use by internal calls to the Frame System.

## Reference
Viam uses model files written in JSON, similar to the URDF files used in ROS. JSON files are better suited for use in Python environments.


### Model JSON

As explained in the [Model Configuration](#model-configuration) section, some components use an additional **Model JSON** file to specify reference frame information about the kinematic chain of the component to the Frame System. 

When writing a driver for a particular piece of hardware that implements one of these components, you must create its accompanying **Model JSON** file.

!!! note
    There is currently (15 Sept 2022) no user interface in the Viam App (<a href="https://app.viam.com">https://app.viam.com</a>) by which to create these files. 

Furthermore, only our Go implementation supports creation of custom **Model JSON** files (15 Sept 2022) as a way if ingesting kinematic parameters is provided in our Go repository. Native support for specifying kinematic parameters of arms is not yet supported in the Python SDK."

This means that a user will fork our [repository](https://github.com/viamrobotics/rdk), create one of these files in that fork, and then use it to build the package for running the server.

We currently support two methods of supplying reference frame parameters for a kinematic chain: 
1. <a href="https://drake.mit.edu/doxygen_cxx/group__multibody__spatial__vectors.html" target="_blank">Spatial Vector Algebra</a>[^sva] (SVA) - supplying reference frame information for each link and each joint.
2. <a href="https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters" target="_blank">Denavit-Hartenberg</a>[^dh] (DH) parameters.

[^sva]: Spatial Vector Algebra (SVA):  <a href="https://drake.mit.edu/doxygen_cxx/group__multibody__spatial__vectors.html" target="_blank">ht<span></span>tps://drake.mit.edu/doxygen_cxx/group__multibody__spatial__vectors.html</a>

[^dh]: Denavit-Hartenberg (DH): <a href="https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters" target="_blank">https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters</a>

Of the two methods, Viam prefers Spacial Vector Algebra over Denavit-Hartenberg. 

Viam wants roboticists to be able to specify link frames arbitrarily, which DH parameters are unable to guarantee. We also want roboticists to make their own (messy) robots; accurate identification of DH parameters for a mass-produced robot can be exceedingly difficult. Furthermore, incorrect SVA parameters are much easier to troubleshoot than incorrect DH parameters.

Below are JSON examples for each parameter type used by our Universal Robots[^ur] arms driver: 
[^ur]: Universal Robots: [https://www.universal-robots.com/](https://www.universal-robots.com/)


**Example: kinematic_param_type=SVA:**

```json
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
                "type" : "ov_degrees",
                "value" : {
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
**Example: kinematic_param_type=DH**

```json
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
