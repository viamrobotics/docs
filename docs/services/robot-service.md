---
title: "Robot Service"
linkTitle: "Robot"
description: "The Robot Service consists of a set of robot monitoring and management APIs that most robots support."
type: "docs"
draft: "true"
weight: 10
tags: ["robot state", "services"]
# SME: Cheuk
---

The Robot Service refers to the minimum set of APIs that most robots running `viam-server` support.
This means that any of the various robot clients in Viam, like the Python SDK, Go Client SDK, or modular resources, should also support methods to interface with these same APIs from the client (instead of server) side.
If you are implementing your own client, keep this in mind.
Use the Robot Service as an entrypoint to interact with Viam robots and provide a way to get updates from the robot as a whole.

The below is a current list of interfaces provided by the Robot Service.

<table>
<tr><th>Operation</th><th>Description</th></tr>
    <tr>
        <td>BlockForOperation</td>
        <td>The request will only return once the specified operation is complete.
        Useful if a process needs to work until another is completed.
        Requires the <strong>Operations ID</strong>.</td>
    </tr>
    <tr>
        <td>CancelOperation</td>
        <td>Cancels a specified operation.
        Requires the <strong>Operations ID</strong>.</td>
    </tr>
    <tr>
        <td>DiscoverComponents</td>
        <td>Returns a best-effort configuration for a resource subtype and model that can be discovered on the robot (like a webcam on a Pi).</td>
    </tr>
    <tr>
        <td>FrameSystemConfig</td>
        <td>Returns the frame system configuration of the robot.</td>
    </tr>
    <tr>
        <td>GetOperations</td>
        <td>Returns all running operations initiated over gRPC (<a href="https://en.wikipedia.org/wiki/GRPC" target="_blank">Google Remote Procedure Call</a></td>
    </tr>
    <tr>
        <td>GetStatus</td>
        <td>Returns the status for the resources queried for, all resources if none specified.</td>
    </tr>
    <tr>
        <td>ResourceNames</td>
        <td>Returns the list of all resources currently available on the robot.
        This includes remote resources.</td>
    </tr>
    <tr>
        <td>ResourceRPCSubtypes</td>
        <td>Returns all resource subtypes available on the robot (this is more of an advance feature, the RDK uses it for user defined resources)</td>
    </tr>
    <tr>
        <td>StopAll</td>
        <td>Cancels all ongoing operations and then attempts to stop all resources that can be stopped.</td>
    </tr>
    <tr>
        <td>StreamStatus</td>
        <td>Streams the status for the resources queried for, all resources if none specified.
        The interval at which the stream refreshes can also be specified.</td>
    </tr>
    <tr>
        <td>TransformPose</td>
        <td>Transforms the pose in frame into a frame within the robot’s frame system.</td>
    </tr>
</table>

## Operation and Operation IDs

**Operation IDs** are how Viam tracks in-flight operations/robot commands over gRPC network requests.

The robot creates a unique **Operation ID** for every request (operation).
This ID expires once the request is completed.
Each new gRPC request creates a new **Operation ID**, even if it was created from a pre-existing operation.

Users can cancel an operation by passing in its **Operation ID,** and can also block a specific operation, again, by specifying its **Operation ID**, until that operation is complete.

For example, consider two _connected_ robots. Robot "A," with an attached base and navigation service and robot "B," operating remotely with an attached GPS.
A client’s request to the navigation service to move "A" creates a new **Operation ID**.

The request to the attached {{% glossary_tooltip term_id="base" text="base"%}} is a local request (that is, a non-gRPC request) between the navigation service and its base and does not create a new **Operation ID**.
However, the navigation service request to the GPS is through gRPC, which spawns a new operation and thus another **Operation ID**.

Canceling the initial **Operation ID** cancels the first operation on the navigation service, but that does not cancel the second operation (obtaining the location from the remote GPS).
