Move the arm's joints through a trajectory delivered as a stream of timed waypoints.
`MoveThroughJointPositions` takes a whole trajectory in one request.
This method opens a stream instead and accepts batches of waypoints until the caller closes it, so a long or continuously generated trajectory does not have to be complete before the arm starts moving.
The call blocks until the arm finishes the trajectory, the stream fails, or a new operation cancels it.
