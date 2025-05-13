---
linkTitle: "Move an arm"
title: "Move an arm"
weight: 20
layout: "docs"
type: "docs"
description: "Move a robotic arm with a no-code interface or with the motion planning API."
aliases:
  - /how-tos/move-robot-arm/
  - /tutorials/motion/accessing-and-moving-robot-arm/
  - /tutorials/motion/
next: "/operate/mobility/move-arm/configure-arm/"
---

You can move a robotic arm in three ways:

- Use the Viam app to move the arm with a no-code interface.
  - Useful for getting started and quick testing.
- Use the arm API to move the arm with code.
  - Not recommended for production use cases, because it does not allow you to configure obstacles or constrain orientation.
- Use the motion planning API to move the arm with code.
  - Recommended for most use cases.

To get started:

1. [Configure your arm](/operate/mobility/move-arm/configure-arm/).

1. If you have a component such as a gripper or camera attached to the arm, [configure it](/operate/mobility/move-arm/configure-additional/).

1. [Move the arm with no code](/operate/mobility/move-arm/arm-no-code/).

1. [Move the arm with the motion planning API](/operate/mobility/move-arm/arm-motion/).
