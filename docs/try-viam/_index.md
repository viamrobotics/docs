---
title: "Try Viam"
linkTitle: "Try Viam"
weight: 15
type: "docs"
description: "Try Viam by taking over a Viam Rover in our robotics lab for 15 minutes or ordering your own."
---

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <br>
        <img src="img/try-viam/reservation-management.png" alt="Overhead view of the Viam rover showing it as it drives in a square.">
        <br>
        <a href="try-viam-tutorial/">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Borrow a rover right now</h4>
            <p style="text-align: left;">Rent and remotely configure and control a Viam Rover located on-site at Viam in NYC.</p>
        </a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <br>
        <img src="rover-resources/img/viam-rover/rover-side.jpg" alt="detectionCam stream displaying a color detection.">
        <br>
        <a href="../../tutorials/viam-rover/try-viam-color-detection">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Order and build your own rover</h4>
            <p style="text-align: left;"> Order your own preassembled rover, add a raspberry pi and some batteries, and get rolling.</p>
        <a>
    </div>
  </div>
</div>

## Get started with Viam

Once you have rented or received yout Viam rover, you can:

- teleoperate (that means drive) the rover from wherever you are
- see what the rover sees using services like computer vision or data management
- configure and control the rover's sensors and actuators in the Viam app
- write code to control the rover

If you have rented a rover, follow the [Try Viam tutorial](/tutorials/viam-rover/).
If you have ordered and received your own rover, start by [unboxing and setting up your Viam rover].

## Control your rover with SDKs

If you want to control and automate your rover with Python or Go, use the [Viam SDKs](/program/sdk-as-client).

Viam also exposes exposes a gRPC [API for robot controls](https://github.com/viamrobotics/api).

Both the API and the SDKs support [WebRTC](https://webrtcforthecurious.com/). The SDKs provide a wrapper around the viam-server [gRPC](https://grpc.io/) API and streamline connection, authentication, and encryption against a server.

## Next steps
