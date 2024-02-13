---
title: "Mobility"
linkTitle: "Mobility"
weight: 460
type: "docs"
description: "Plan and control your robot's motion with Viam's integrated tools."
image: "/platform/mobility.svg"
imageAlt: "A path around obstacles."
menuindent: true
no_list: true
---

The {{< glossary_tooltip term_id="rdk" text="RDK" >}} includes several built-in services that make it easy to move your robot in intelligent ways, whether moving a single arm, a connected system of gantries and arms, or an entire robot on wheels.

The following services work together to coordinate your robot's movement:

## Frame system

{{<imgproc src="/services/icons/frame-system.svg" class="fill alignleft" style="max-width: 190px" declaredimensions=true alt="Frame system icon">}}

The [frame system service](/mobility/frame-system/):

- Allows you to describe the physical relationship between your machine's parts by organizing the machine's {{< glossary_tooltip term_id="component" text="components" >}} into a tree of reference frames.
- Displays a visualization of that tree of reference frames in <a href="https://app.viam.com">the Viam app</a>.
- Has an API method that allows you to translate a point in the coordinate system of one component (such as a camera) to a point in the coordinate system of another component (such as an arm)
- The motion service uses the tree of reference frames internally to make and execute motion plans while avoiding self-collisions as well as collisions with external objects.

## Motion and navigation

{{<imgproc src="/services/icons/motion.svg" class="fill alignleft" style="max-width: 170px" declaredimensions=true alt="Motion path icon">}}

- The [motion service](/mobility/motion/) allows you to:
  - Create and execute plans to move components to goal positions in the components' own coordinate systems, as well as to move an entire robot on a GPS map or SLAM map.
  - Set constraints on the motion plans, such as requiring a component to maintain its orientation throughout the move (for example, an arm holding a cup upright as it moves).
- The [navigation service](/mobility/navigation/) lets you specify a list of waypoints that a robot should travel through on a GPS map, and delegates to the motion service to create and execute the corresponding sequence of motion plans.

## Simultaneous localization and mapping (SLAM)

{{<imgproc src="/services/icons/slam.svg" class="fill alignleft" style="max-width: 170px" declaredimensions=true alt="SLAM icon">}}
The [SLAM service](/mobility/slam/):

- Defines [an API](/mobility/slam/#api) for returning a map of a robot's environment as a _point cloud_, or set of points that represent the occupied space in the environment.
- Includes a {{< glossary_tooltip term_id="module" text="module" >}} that wraps the Cartographer SLAM algorithm.
- Supports using the Cartographer module to create, update, or do pure localization on maps created either using a live robot or data that was previously captured on a robot using [data capture](/data/capture/).
- Allows you to view all maps you have created in your **SLAM Library** on the [Viam app](https://app.viam.com).
- Allows you to deploy a map from your **SLAM Library** onto a robot to use the map with the motion service.

## Get started

To get acquainted with the frame system, [configure the frame system](/mobility/frame-system/frame-config/) for an arm attached to a table.

To create a SLAM map of your home or office, use a mobile [{{< glossary_tooltip term_id="base" text="base" >}}](/components/base/) of your choice along with an RPLIDAR A1 or A3 and the [Cartographer module](/mobility/slam/cartographer).

Or, get started with one of our tutorials:

{{< cards >}}
{{< card link="/tutorials/services/plan-motion-with-arm-gripper/">}}
{{< card link="/tutorials/services/navigate-with-rover-base/">}}
{{< card link="/tutorials/services/constrain-motion/">}}
{{< /cards >}}
