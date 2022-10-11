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
    <table>
      <tr>
        <td><h2>Getting Started</h2>
<li><a href="/getting-started/high-level-overview">Viam Overview</a></li>
<li><a href="http://www.viam.com/use-cases">Viam Use Cases</a></li>
<br><h2>Product Overview</h2>
<ul>
<li><a href="/product-overviews/rdk">Overview of Viam-Server and RDK</a></li>
<li><a href="/product-overviews/fleet-management">Viam's Fleet Management</a></li>
<li><a href="/product-overviews/sdk-as-client">Using Viam's SDKs as a Client Application</a></li>
<li><a href="/product-overviews/sdk-as-server">Using Viam's SDKs for a Server Hardware Implementation</a></li>
<li><a href="/product-overviews/data-management">Viam's Data Management Platform</a></li></td>
</ul>
      </tr>
    </table>
  </div>
  <div class="column">
    <table>
      <tr>
        <td><iframe width="640" height="360" src="https://www.youtube.com/embed/TjmvnEdNVKs" title="Viam Intro Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></td>
      </tr>
    </table>
  </div>
</div>


## Tutorials
Scuttle based tutorials
- [Configuring SCUTTLE Rover with a Camera](/tutorials/scuttlebot)
- [Controlling a SCUTTLE Rover with a Bluetooth Gamepad](/tutorials/scuttle-gamepad)
- [Detecting Color with the SCUTTLE Rover](/tutorials/color-detection-scuttle)

Yahboom based tutorials
- [Setting up a Yahboom 4WD Rover with a Bluetooth Gamepad](/tutorials/yahboom-rover)

Simple Raspberry tutorials
- [Making an LED Blink with a Raspberry Pi](/tutorials/how-to-make-an-led-blink-with-a-raspberry-pi-using-viam)
- [Making an LED Blink with a Raspberry Pi and Viam's Python SDK](/tutorials/how-to-make-an-led-blink-with-a-raspberry-pi-and-python)

Other tutorials
- [Building a Line-Following Robot with a Rover and a Camera](/tutorials/webcam-line-follower-robot/)
- [All Tutorials](/tutorials/)

## Components - Pieces of hardware in your robot
- [Arm](/components/arm)
- [Board](/components/board)
- [Camera](/components/camera)
- [Motor](/components/motor)
- [Servo](/components/servo)
- [Encoder](/components/encoder)
- [Base](/components/base) - a mobile robot base, examples: wheeled, tracked, boat, drone, 
- [Input Controller](/components/input-controller)
- [Sensor](/components/sensor)

## Services - Higher level software-only APIs
- [Robot Service](/services/robot-service) - meta data about a robot and robot level operations
- [Vision](/services/vision)
- [Motion](/services/motion)
- [Data Capture](/services/data-capture)
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
