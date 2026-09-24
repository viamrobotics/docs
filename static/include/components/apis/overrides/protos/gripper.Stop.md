Stops the gripper.
It is assumed that the gripper stops immediately, so `IsMoving` will return false after calling `Stop`.

Whether a held object survives the stop depends on the gripper model: some models keep holding it, and on others `Stop` releases the drive and drops it. Check `IsHoldingSomething` afterward.
