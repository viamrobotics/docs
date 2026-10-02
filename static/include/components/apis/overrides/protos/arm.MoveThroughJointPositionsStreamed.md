Stream batches of timed trajectory points to the arm and execute them in order as they arrive.
Unlike `MoveThroughJointPositions`, the full trajectory does not have to be known before the motion starts: the caller keeps appending points while the arm executes the ones it already has.
