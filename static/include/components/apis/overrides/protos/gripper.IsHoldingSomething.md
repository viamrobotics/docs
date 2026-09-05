Return if the gripper is holding something.

When a client's session ends, viam-server stops every actuator that session commanded; a gripper that holds something keeps holding it, and a gripper that closed on nothing stops where it is with no force.
