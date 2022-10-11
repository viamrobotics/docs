---
title: "Welcome to the Viam Documentation Site"
linkTitle: "Welcome to the Viam Documentation Site"
weight: 1
type: "docs"
---

<style>
    * {
  box-sizing: border-box;
}
.row {
  margin-left:-5px;
  margin-right:-5px;
}
  
.column {
  float: left;
  width: 40%;
  padding: 5px;
}

/* Clearfix (clear floats) */
.row::after {
  content: "";
  clear: both;
  display: table;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  border: none solid #ddd;
}

th, td {
  text-align: left;
  padding: 16px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>
</head>
<body>
<br>
<div class="row">
  <div class="column">
 
## Getting Started
Looking to get started with Viam? Check out the following:

- [Viam Overview](/getting-started/high-level-overview)
- [Viam Use Cases](http://www.viam.com/use-cases)
- [Intro Video](https://www.youtube.com/watch?v=TjmvnEdNVKs&ab_channel=EliotHorowitz)

## Product Overviews
- [Overview of Viam-Server and RDK](/product-overviews/rdk)
- [Viam's Fleet Management](/product-overviews/fleet-management)
- [Using Viam's SDKs as a Client Application](/product-overviews/sdk-as-client)
- [Using Viam's SDKs for a Server Hardware Implementation](/product-overviews/sdk-as-server)
- [Viam's Data Management Platform](/product-overviews/data-management)

  </div>
  <div class="column">
    <table>
      <tr>
        <td><a href="https://www.youtube.com/watch?v=TjmvnEdNVKs" target="_blank">Click to view our Founder's Message<img src="../img/eliot-vid-thumb.png" style="border: 1px solid black"> <span style="font-size:xx-small" </span> (Link opens in new tab)</a></td>
      </tr>
    </table>
  </div>
</div>


## Tutorials
SCUTTLE-based tutorials
- [Configuring SCUTTLE Rover with a Camera](/tutorials/scuttlebot)
- [Controlling a SCUTTLE Rover with a Bluetooth Gamepad](/tutorials/scuttle-gamepad)
- [Detecting Color with the SCUTTLE Rover](/tutorials/color-detection-scuttle)

Yahboom-based tutorials
- [Setting up a Yahboom 4WD Rover with a Bluetooth Gamepad](/tutorials/yahboom-rover)

Simple Raspberry Pi tutorials
- [Making an LED Blink with a Raspberry Pi](/tutorials/how-to-make-an-led-blink-with-a-raspberry-pi-using-viam)
- [Making an LED Blink with a Raspberry Pi and Viam's Python SDK](/tutorials/how-to-make-an-led-blink-with-a-raspberry-pi-and-python)

Other tutorials
- [Building a Line-Following Robot with a Rover and a Camera](/tutorials/webcam-line-follower-robot/)
- [All Tutorials](/tutorials/)

## Components - Pieces of hardware in your robot
- [Arm](/components/arm)
- [Base](/components/base) - a mobile robot base, examples: wheeled, tracked, boat, drone
- [Board](/components/board)
- [Camera](/components/camera)
- [Encoder](/components/encoder)
- [Gantry](/components/gantry)
- [Input Controller](/components/input-controller)
- [Motor](/components/motor)
- [Sensor](/components/sensor)
- [Servo](/components/servo)

## Services - Higher level software-only APIs
- [Robot Service](/services/robot-service) - meta data about a robot and robot level operations
- [Vision](/services/vision)
- [Motion](/services/motion)
- [Data Management](/services/data-management)
- [Simultaneous Localization and Mapping (SLAM)](/services/slam)


## Deep Dives
- [End-to-End Flow](/deeper-dive/robot-to-robot-comms)
- [Authentication](/deeper-dive/security)

## Appendix
- [Glossary](/appendix/glossary)
- [Orientation Vector](/appendix/orientation-vector)
- [Troubleshooting](/appendix/troubleshooting)
- [Learning Resources](/appendix/learning-resources)

## SDKs
- [Python SDK](https://python.viam.dev/)
