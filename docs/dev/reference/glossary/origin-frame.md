---
title: Origin frame
id: origin-frame
full_link:
short_description: The origin frame is the frame at the base of an arm or other component that has a complex kinematics chain.
---

The origin frame is the frame at the base of an arm, gantry, or other component.
This is typically the point at the center of where the component is mounted to a table or stand.

Every component that has a kinematics chain has an origin frame and an end effector frame, for example `my_arm_origin` and `my_arm`.

If you parent a gripper to the arm's `my_arm` frame, the frame system will know the gripper is at the end of the arm.
If you mistakenly parent the gripper to the arm's `my_arm_origin` frame, the frame system will think the gripper is at the base of the arm, and the gripper will not move when you move the arm.

For more information, see [How the frame system works](/operate/reference/services/frame-system/#how-the-frame-system-works).
