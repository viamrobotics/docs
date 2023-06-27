---
title: "Try Viam"
linkTitle: "Try Viam"
childTitleEndOverwrite: "Try Viam"
weight: 15
type: "docs"
description: "Try Viam by taking over a Viam Rover in our robotics lab."
images: ["/tutorials/img/try-viam-sdk/image1.gif"]
aliases:
    - "/getting-started/try-viam/"
---

Viam is a general robotics platform that can run on any hardware.
The easiest way to try Viam is to [rent and remotely configure and control a Viam Rover](https://app.viam.com/try) located on-site at Viam in New York:

{{<gif webm_src="img/rover-reservation.webm" mp4_src="img/rover-reservation.mp4" alt="Rover reservation management page" max-width="800px">}}

## Get started with Viam

During your rover rental, you can [try out some of the Viam platform functionality](try-viam-tutorial/):

- Drive the rover from wherever you are
- Use services like computer vision to identify colors and objects
- Explore the configuration and control interface for the rover's sensors and actuators in the Viam app
- Write code to control the rover

## Control your rover with SDKs

If you want to control and automate your rover with Python or Go, use the [Viam SDKs](/program/apis/).

Viam also exposes a {{< glossary_tooltip term_id="grpc" text="gRPC" >}} [API for robot controls](https://github.com/viamrobotics/api).

Both the API and the SDKs support {{< glossary_tooltip term_id="webrtc" >}}.
The SDKs provide a wrapper around the `viam-server` [gRPC](https://grpc.io/) API and streamline connection, authentication, and encryption against a server.

## Next steps
