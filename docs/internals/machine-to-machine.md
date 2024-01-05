---
title: "Machine-to-Machine Communication: End-to-End Flow"
linkTitle: "Machine-to-Machine Communication"
weight: 10
type: "docs"
description: "Explanation of how a machine and its parts interact at the communication layer."
aliases:
  - "/internals/robot-to-robot-comms/"
---

When building a smart machine application in the [Viam app](https://app.viam.com), a user typically begins by configuring their machine which can consist of one or more {{< glossary_tooltip term_id="part" text="parts" >}}.
Next they will test that it is wired up properly using the Viam app's Control page.
Once they've ensured everything is wired up properly, they will build their main application and the business logic for their robot using one of Viam's language SDKs.
This SDK-based application is typically run on either the main part of the robot or a separate computer dedicated to running the business logic for the machine.

Below, we describe the flow of information through a Viam-based multipart robot and then get into the specifics of what backs these connections and communcations APIs.

## High-Level Inter-Robot/SDK Communication

To begin, let's define our machine's topology:

![robot communication diagram](/internals/robot-to-robot-comms/robot-communication-diagram.png)

This robot is made of two parts and a separate SDK-based application, which we'll assume is on a third machine, though it could just as easily run on the main part without any changes.

- The first and main part, RDK Part 1, consists of a Raspberry Pi and a single USB connected camera called Camera.

- The second and final part, RDK Part 2, consists of a Rapsberry Pi connected to a robotic arm over ethernet and a gantry over GPIO.

RDK Part 1 will establish a bidirectional gRPC/{{< glossary_tooltip term_id="webrtc" >}} connection to RDK Part 2.
RDK Part 1 is considered the controlling peer (client).
RDK Part 2 is consider the controlled peer (server).

Let's suppose our SDK application uses the camera to track the largest object in the scene and instructs the arm to move to that same object.

Since RDK Part 1 is the main part and has access to all other parts, the application will connect to it using the SDK.
Once connected, it will take the following series of actions:

<OL>
<li>Get segmented point clouds from the camera and the object segmentation service.</li>

<li>Find the largest object by volume.</li>

<li>Take the object's center pose and tell the motion service to move the arm to that point.</li>

<li>Go back to 1.</li>
</OL>
Let's breakdown how these steps are executed.

<ol>
<li>Get segmented point clouds from the camera and the object segmentation service:</li>

![robot communication diagram](/internals/robot-to-robot-comms/getobjectpointcloud-flow.png)

<OL type="a">
<li>The SDK will send a GetObjectPointClouds request with Camera being referenced in the message to RDK Part 1's Object Segmentation Service.</li>

<li>RDK Part 1 will look up the camera referenced, call the GetPointCloud method on it.</li>

<li>The Camera will return the PointCloud data to RDK Part</li>

<li>RDK Part 1 will use a point cloud segmentation algorithm to segment geometries in the PointCloud.</li>
{{% alert title="Important" color="note" %}}
The points returned are respective to the reference frame of the camera.
This will become important in a moment.
{{% /alert %}}
<li>The set of segmented point clouds and their bounding geometries are sent back to the SDK-based application.</li>
</ol>

<li>Find the largest object by volume:</li>
<ol type="a">
<li>The application will iterate over the geometries of the segmented point clouds returned to it and find the object with the greatest volume and record its center pose.</li>
</ol>

<li>Take the object's center pose and tell the motion service to move the arm to that point:</li>

![motion service move flow](/internals/robot-to-robot-comms/motion-service-move-flow.png)

<ol type="a">
<li>The SDK application will send a Move request for the arm to the motion service on RDK Part 1 with the destination set to the center point determined by the application.</li>

<li>RDK Part 1's motion service will break down the Move request and perform the necessary frame transforms before sending the requests along to the relevant components.
This is where the frame system comes into play.
Our center pose came from the camera but we want to move the arm to that position even though the arm lives in its own frame.
The frame system logic in the RDK automatically handles the transformation logic between these two reference frames while also handling understanding how the frame systems are connected across the two parts.</li>

<li>Having computed the pose in the reference frame of the arm, the motion service takes this pose, and sends a plan on how to move the arm in addition to the gantry to achieve this new goal pose to RDK Part 2.
The plan consists of a series of movements that combine inverse kinematics, mathematics, and constraints based motion planning to get the arm and gantry to their goal positions.</li>

<li>In executing the plan, which is being coordinated on RDK Part 1, Part 1 will send messages to the Arm and Gantry on RDK Part 2.
RDK Part 2 will be unaware of the actual plan and instead will only receive distinct messages to move the components individually.</li>

<li>The arm and gantry connected to RDK Part 2 return an acknowledgement of the part Move requests to RDK Part 2.</li>

<li>RDK Part 2 returns an acknowledgement of the Motion Move request to RDK Part 1.</li>

<li>RDK Part 1 returns an acknowledgement of the Motion Move request to the SDK application.</li>
</ol>

## Low-Level Inter-Robot/SDK Communication

All component and service types in the RDK, and the Viam API for that matter, are represented as [Protocol Buffers (protobuf)](https://developers.google.com/protocol-buffers) services.
protobuf is a battle tested Interface Description Language (IDL) that allows for specifying services, their methods, and the messages that comprise those methods.
Code that uses protobuf is autogenerated and compiles messages into a binary form.

[gRPC](https://grpc.io/) is responsible for the transport and communication of protobuf messages when calling protobuf methods.
It generally works over a TCP, TLS backed HTTP2 connection operating over framing see [gRPC's HTTP2 documentation](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) for more.

The RDK uses protobuf and gRPC to enable access and control to its components and services.
That means if there are two arms in a robot configuration, there is only one Arm service that handles the Remote Procedure Calls (RPC) for all arms configured.

In addition to gRPC, the RDK uses [WebRTC](https://webrtcforthecurious.com/) video and audio streams and data channels to enable peer to peer (P2P) communication between robot parts as well as SDKs and the Remote Control interface.

An outline of how WebRTC is utilized lives on [Go.dev](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection), but in short, an RDK is always waiting on the Viam app ([app.viam.com](https://app.viam.com)) to inform it of a connection requesting to be made to it whereby it sends details about itself and how to connect on a per connection basis.
Once a connection is made, the Viam app is no longer involved in any packet transport and leaves it up to the two peers to communicate with each other.
