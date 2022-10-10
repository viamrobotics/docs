---
title: "Run SLAM on your robot"
linkTitle: "Run SLAM"
weight: 90
type: "docs"
draft: true
description: "Instructions to run SLAM with either a webcam or provided example data."
---
[SLAM](https://docs.viam.com/services/slam/) is used to allow the robot to create a map of its surroundings, as well as find its location within that map.
This tutorial shows you how to run ORB-SLAM3 on your robot. There are two choices:
* Run SLAM in online mode with a webcam. The webcam can be installed on a robot, or just be held by hand.
* Run SLAM in offline mode either with collected data or our provided example data.

## Requirements

* A Raspberry Pi with Raspian OS 64-bit Lite and the viam-server installed.
Refer to [Installing Raspian on the Raspberry Pi](../../getting-started/installation/#installing-raspian-on-the-raspberry-pi), if necessary.
* [optionally] A webcam or other off-the-shelf RGB camera.

## Setup
If you haven’t already, please set up the Raspberry Pi on the [Viam App](https://app.viam.com) per [these instructions](../../getting-started/installation).

Next, we'll install the ORB-SLAM3 binary.

### Installing the ORB-SLAM3 binary
First, check the architecture of your system by running `lscpu`. Depending on that, download one of the following 
