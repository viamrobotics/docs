Return if the gripper is holding something.

When a client's session ends, viam-server stops every actuator that session commanded. Whether a held object survives that stop depends on the gripper model: some models keep holding it, and on others the stop releases the drive and drops it. A gripper that closed on nothing stops where it is with no force. Check `IsHoldingSomething` after a carry, and keep a sequence that must hold an object across steps in one session.
