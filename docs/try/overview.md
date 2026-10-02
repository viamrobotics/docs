---
linkTitle: "Overview"
title: "Try Viam"
weight: 1
layout: "docs"
type: "docs"
no_list: true
description: "Pick a hands-on way to try Viam. Most pathways need no hardware to get started."
capabilities: ["section-index", "docs"]
diataxis: overview
date: "2025-01-30"
aliases:
  - /operate/hello-world/
  - /operate/hello-world/first-project/
  - /operate/hello-world/quickstart/
  - /operate/hello-world/tutorial-desk-safari/
  - /dev/reference/try-viam/
  - /dev/reference/try-viam/reserve-a-rover/
  - /dev/reference/try-viam/try-viam-tutorial/
  - /try-viam/
  - /try-viam/reserve-a-rover/
  - /try-viam/faq/
  - /get-started/try-viam/
  - /get-started/try-viam/reserve-a-rover/
  - /get-started/try-viam/faq/
  - /appendix/try-viam/
  - /appendix/try-viam/reserve-a-rover/
  - /appendix/try-viam/reserve-a-rover
  - /appendix/try-viam/tutorials/
  - /appendix/try-viam-faq/
  - /appendix/get-started/try-viam/faq/
  - /getting-started/try-viam/
  - /tutorials/viam-rover/
  - /try/viam-rover/rent-a-rover/
---

Viam enables you to build and manage real robotics applications, but you don't need any hardware to start learning it.

Each pathway below teaches practical Viam skills through a hands-on project. Choose whichever matches your learning goals.

| Pathway                                                                   | Description                                                                                                                                                                      | Hardware required                                | Time         |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------ |
| [Viam 101](https://www.viam.com/education)                                | Learn robotics fundamentals for working with physical spaces and motion planning, and build an application for a robotic arm in the Viam framework using your own control logic. | None (Viam visualization)                        | ~90 minutes  |
| [Viam 102](https://www.viam.com/education)                                | Turn a control script into a production-grade module, covering the module lifecycle, resource management, and publishing to the Viam Registry.                                   | None (Viam visualization)                        | ~120 minutes |
| [Quality Inspection](/try/quality-inspection/overview/)                   | Use a vision pipeline and ML model to capture data and write inspection logic for a simulated canning line.                                                                      | None (Gazebo simulation)                         | ~55 minutes  |
| [SO-101: Teleop and Motion Capture](https://www.viam.com/education/so101) | Drive a real SO-101 arm by hand, capture motions by demonstration, and trigger them with hand gestures, all with no code.                                                        | SO-101 arm                                       | ~60 minutes  |
| [Miniature Palletizing](/tutorials/so-arm101-palletizing/)                | Teach a desktop arm its workspace by hand, then write Python that picks cubes and stacks them on a pallet while the motion planner avoids the cubes already placed.              | SO-ARM101 arm and gripper, eight 16 mm cubes     | ~90 minutes  |
| [Pick and Place](/tutorials/pick-and-place/)                              | Use Viam's Python SDK and vision models to program an arm to detect, pick up, and place blocks on its own.                                                                       | uFactory xArm6 and gripper, Intel RealSense D435 | ~90 minutes  |

{{< alert title="Viam Rover discontinued" color="caution" >}}
As of September 2026, the Viam Rover has been discontinued and is no longer available to rent or purchase.
If you are new to Viam, we recommend taking our free [Viam 101 course](https://www.viam.com/education) to try Viam in a simulation environment, no hardware required.
You can also try the [Quality Inspection tutorial](/try/quality-inspection/overview/), which uses a Gazebo simulation.
If you already own a Viam Rover, the [rover setup guides](/reference/device-setup/viam-rover/) are still available as reference.
{{< /alert >}}
