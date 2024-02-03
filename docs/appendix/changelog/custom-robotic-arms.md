---
title: Implement custom robotic arms as Viam modules
date: "2023-06-01"
color: "added"
---

When prototyping a robotic arm, you can now facilitate movement without creating your own motion planning.
This update enables you to implement custom models of an arm component as a [modular resource](/registry/) by coding three endpoints of the [Arm API](/components/arm/#api):

- `getJointPositions`
- `movetoJointPositions`
- `GetKinematics`

Then, use the [motion planning service](/mobility/motion/) to specify poses, and Viam handles the rest.

For more information, see this [tutorial on creating a custom arm](/registry/examples/custom-arm/).
