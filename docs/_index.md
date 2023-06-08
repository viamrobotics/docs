---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam is a complete software platform for robots that runs on any 64-bit Linux OS and macOS."
weight: 1
no_list: true
type: "docs"
hide_feedback: true
sitemap:
  priority: 1.0
---

Welcome to the Viam Documentation!
Viam is a complete software platform for robots that runs on any 64-bit Linux OS and macOS.

Explore the following resources to jump right in:

<div class="container td-max-width-on-larger-screens">
  <div class="row">
    <div class="col landing-hover-card">
        <div class="landing-hover-card-padding yellow">
            <h4>Learn and Try</h4>
            <p style="text-align: left;">
            Learn about <a href="viam/">the Viam platform in 3 minutes</a> and then
            <a href="try-viam/">drive a Viam rover</a> from the comfort of your home or follow along with a <a href="tutorials/"> tutorial</a>.</p>
            {{<gif webm_src="img/rover.webm" mp4_src="img/rover.mp4" alt="A Viam Rover moving about">}}
        </div>
    </div>
    <div class="col landing-hover-card ">
        <div class="landing-hover-card-padding purple">
        <h4>Configure your robots</h4>
        <div style="text-align: left">
            <ol style="padding-inline-start: 1.1rem">
            <li><a href="/manage/fleet/robots/">Set up your robot</a> or<a href="manage/fleet/"> fleet</a></li>
            <li><a href="installation/">Install Viam on your robot</a></li>
            <li><a href="manage/configuration/">Configure your robot</a></li>
            <li><a href="manage/fleet/robots/#control">Test your robot</a></li>
            </ol>
            {{<gif webm_src="img/blink.webm" mp4_src="img/blink.mp4" alt="A blinking L.E.D. connected to a Raspberry Pi">}}
        </div>
    </div>
    </div>
  </div>
  <div class="row">
    <div class="col landing-hover-card">
        <div class="landing-hover-card-padding teal">
        <h4>Program your robots</h4>
        <p style="text-align: left;">
            Program and control your robots in <a href="program/sdks/"> the languages you already know</a> like <a href="https://python.viam.dev/">Python</a>, <a href="https://pkg.go.dev/go.viam.com/rdk">Go</a>, or <a href="https://ts.viam.dev/">TypeScript</a>.
        </p>
        <img src="img/code.png" alt="Robot code">
        </div>
    </div>
    <div class="col landing-hover-card">
        <div class="landing-hover-card-padding pink">
            <h4>Community</h4>
            <p style="text-align: left;">Have questions, or want to meet other people working on robots? <a href="https://discord.gg/viam">Join us in the Community Discord!</a></p>
            {{<gif webm_src="img/heart.webm" mp4_src="img/heart.mp4" alt="A robot drawing a heart">}}
        </div>
    </div>
    </div>
</div>
<br>

Viam includes pre-configured software integration for many popular [boards](/installation/#preparation) and robotics [components](/components/) out of the box, and includes many popular [services](/services/) you might want to use with your robot.
Click the selections below to learn more:

#### Supported boards

Viam supports the following [boards](/installation/#preparation) out of the box:

<div id="board-carousel" class="carousel td-max-width-on-larger-screens">
  <ul tabindex="0">
   <li id="c1_slide1">
    <a href="installation/prepare/jetson-nano-setup/">
        <img src="installation/img/jetson-nano-setup/jetson-nano-dev-kit.png" alt="Jetson Nano" width="100%">
        <h6>NVIDIA Jetson Nano</h6>
    </a>
  </li>
  <li id="c1_slide2">
    <a href="installation/prepare/rpi-setup/">
        <img src="installation/img/thumbnails/raspberry-pi-4-b-2gb.png" alt="Raspberry Pi" width="100%">
        <h6>Raspberry Pi 4</h6>
    </a>
  </li>
  <li id="c1_slide3">
    <a href="installation/prepare/beaglebone-setup/">
        <img src="installation/img/thumbnails/beaglebone.png" alt="BeagleBone A I-64" width="100%">
        <h6>BeagleBone AI-64</h6>
    </a>
  </li>
  <li id="c1_slide4">
    <a href="installation/prepare/sk-tda4vm/">
        <img src="installation/img/thumbnails/tda4vm.png" alt="S K - T D A 4 V M" width="100%">
        <h6>Texas Instruments TDA4VM</h6>
    </a>
  </li>
  <li id="c1_slide5">
    <a href="installation/prepare/microcontrollers/">
        <img src="installation/img/thumbnails/esp32-espressif.png" alt="E S P 32 - espressif" width="100%">
        <h6>Espressif ESP32</h6>
    </a>
  </li>
  <li id="c1_slide6">
    <a href="installation/prepare/rpi-setup/">
        <img src="installation/img/thumbnails/rpi-3.png" alt="Raspberry Pi 3" width="100%">
        <h6>Raspberry Pi 3</h6>
    </a>
  </li>
  <li id="c1_slide7">
    <a href="installation/prepare/jetson-agx-orin-setup/">
        <img src="installation/img/jetson-agx-orin-setup/jetson-agx-orin-dev-kit.png" alt="Jetson A G X Orin Developer Kit" width="100%">
        <h6>NVIDIA Jetson AGX Orin</h6>
    </a>
  </li>
  <li id="c1_slide8">
    <a href="components/board/jetson/">
        <img src="installation/img/thumbnails/jetson-xavier.png" alt="Jetson Xavier NX Dev Kit" width="100%">
        <h6>NVIDIA Jetson Xavier NX</h6>
    </a>
  </li>
  <li id="c1_slide9">
    <a href="installation/prepare/rpi-setup/">
        <img src="installation/img/thumbnails/raspberry-pi-zero-2w.png" alt="Raspberry Pi" width="100%">
        <h6>Raspberry Pi Zero 2W</h6>
    </a>
  </li>
  <li id="c1_slide10">
    <a href="components/board/nanopi/">
        <img src="installation/img/thumbnails/nanopi.png" alt="FriendlyElec's NanoPi Mini Board" width="100%">
        <h6>FriendlyElec NanoPi</h6>
    </a>
  </li>
  <li id="c1_slide11">
    <a href="components/board/numato/">
        <img src="installation/img/thumbnails/numato.png" alt="Numato GPIO Modules" width="100%">
        <h6>Numato GPIO Modules</h6>
    </a>
  </li>
  <li id="c1_slide12">
    <a href="components/board/pca9685/">
        <img src="installation/img/thumbnails/pca9685.png" alt="P C A 9685 Arduino I 2 C Interface" width="100%">
        <h6>PCA9686 Arduino I<sup>2</sup>C Interface</h6>
    </a>
  </li>
  </ul>
  <ol style="visibility: hidden" aria-hidden="true">
    <li><a href="#c1_slide1">NVIDIA Jetson Nano</a></li>
    <li><a href="#c1_slide2">Raspberry Pi 4</a></li>
    <li><a href="#c1_slide3">BeagleBone AI-64</a></li>
    <li><a href="#c1_slide4">Texas Instruments TDA4VM</a></li>
    <li><a href="#c1_slide5">Espressif ESP32</a></li>
    <li><a href="#c1_slide6">Raspberry Pi 3</a></li>
    <li><a href="#c1_slide7">NVIDIA Jetson AGX Orin</a></li>
    <li><a href="#c1_slide8">NVIDIA Jetson Xavier NX</a></li>
    <li><a href="#c1_slide9">Raspberry Pi Zero 2W</a></li>
    <li><a href="#c1_slide10">FriendlyElec NanoPi</a></li>
    <li><a href="#c1_slide11">Numato GPIO Modules</a></li>
    <li><a href="#c1_slide12">PCA9686 Arduino I<sup>2</sup>C Interface</a></li>
  </ol>
  <div class="prev" style="display: block">‹</div>
  <div class="next" style="display: block">›</div>
</div>

#### Supported components

Viam offers pre-defined integration with the following [components](/components/):

<div id="board-carousel" class="carousel td-max-width-on-larger-screens">
  <ul tabindex="0">
   <li id="c2_slide1">
    <a href="components/arm/">
        <img src="components/img/components/arm.svg" alt="Arm component" width="100%">
        <h6>Arm</h6>
    </a>
  </li>
  <li id="c2_slide2">
    <a href="components/base/">
        <img src="components/img/components/base.svg" alt="Base component" width="100%">
        <h6>Base</h6>
    </a>
  </li>
  <li id="c2_slide3">
    <a href="components/board/">
        <img src="components/img/components/board.svg" alt="Board component" width="100%">
        <h6>Board</h6>
    </a>
  </li>
  <li id="c2_slide4">
    <a href="components/camera/">
        <img src="components/img/components/camera.svg" alt="Camera component" width="100%">
        <h6>Camera</h6>
    </a>
  </li>
  <li id="c2_slide5">
    <a href="components/encoder/">
        <img src="components/img/components/encoder.svg" alt="Encoder component" width="100%">
        <h6>Encoder</h6>
    </a>
  </li>
  <li id="c2_slide6">
    <a href="components/gantry/">
        <img src="components/img/components/gantry.svg" alt="Gantry component" width="100%">
        <h6>Gantry</h6>
    </a>
  </li>
  <li id="c2_slide7">
    <a href="components/gripper/">
        <img src="components/img/components/gripper.svg" alt="Gripper component" width="100%">
        <h6>Gripper</h6>
    </a>
  </li>
  <li id="c2_slide8">
    <a href="components/input-controller/">
        <img src="components/img/components/controller.svg" alt="Input controller component" width="100%">
        <h6>Input Controller</h6>
    </a>
  </li>
  <li id="c2_slide9">
    <a href="components/motor/">
        <img src="components/img/components/motor.svg" alt="Motor component" width="100%">
        <h6>Motor</h6>
    </a>
  </li>
  <li id="c2_slide10">
    <a href="components/movement-sensor/">
        <img src="components/img/components/imu.svg" alt="Movement sensor component" width="100%">
        <h6>Movement Sensor</h6>
    </a>
  </li>
  <li id="c2_slide11">
    <a href="components/sensor/">
        <img src="components/img/components/sensor.svg" alt="Sensor component" width="100%">
        <h6>Sensor</h6>
    </a>
  </li>
  <li id="c2_slide12">
    <a href="components/servo/">
        <img src="components/img/components/servo.svg" alt="Servo component" width="100%">
        <h6>Servo</h6>
    </a>
  </li>
  </ul>
  <ol style="visibility: hidden" aria-hidden="true">
    <li><a href="#c2_slide1">Arm</a></li>
    <li><a href="#c2_slide2">Base</a></li>
    <li><a href="#c2_slide3">Board</a></li>
    <li><a href="#c2_slide4">Camera</a></li>
    <li><a href="#c2_slide5">Encoder</a></li>
    <li><a href="#c2_slide6">Gantry</a></li>
    <li><a href="#c2_slide7">Gripper</a></li>
    <li><a href="#c2_slide8">Input Controller</a></li>
    <li><a href="#c2_slide9">Motor</a></li>
    <li><a href="#c2_slide10">Movement Sensor</a></li>
    <li><a href="#c2_slide11">Sensor</a></li>
    <li><a href="#c2_slide12">Servo</a></li>
  </ol>
  <div class="prev" style="display: block">‹</div>
  <div class="next" style="display: block">›</div>
</div>

#### Included services

Viam includes the following [services](/services/) for use with your robot:

<div id="board-carousel" class="carousel td-max-width-on-larger-screens">
  <ul tabindex="0">
   <li id="c3_slide1">
    <a href="services/data/">
        <img src="services/img/icons/data-capture.svg" alt="Data capture service" width="100%">
        <h6>Data Capture</h6>
    </a>
  </li>
  <li id="c3_slide2">
    <a href="services/motion/">
        <img src="services/img/icons/motion.svg" alt="Motion service" width="100%">
        <h6>Motion</h6>
    </a>
  </li>
  <li id="c3_slide3">
    <a href="services/frame-system/">
        <img src="services/img/icons/frame-system.svg" alt="Frame system service" width="100%">
        <h6>Frame System</h6>
    </a>
  </li>
  <li id="c3_slide4">
    <a href="services/ml/">
        <img src="services/img/icons/ml.svg" alt="Machine learning service" width="100%">
        <h6>Machine Learning</h6>
    </a>
  </li>
  <li id="c3_slide5">
    <a href="services/slam/">
        <img src="services/img/icons/slam.svg" alt="SLAM service" width="100%">
        <h6>SLAM</h6>
    </a>
  </li>
  <li id="c3_slide6">
    <a href="services/vision/">
        <img src="services/img/icons/vision.svg" alt="Vision service" width="100%">
        <h6>Vision</h6>
    </a>
  </li>
  </ul>
  <ol style="visibility: hidden" aria-hidden="true">
    <li><a href="#c3_slide1">Arm</a></li>
    <li><a href="#c3_slide2">Base</a></li>
    <li><a href="#c3_slide3">Board</a></li>
    <li><a href="#c3_slide4">Camera</a></li>
    <li><a href="#c3_slide5">Encoder</a></li>
    <li><a href="#c3_slide6">Gantry</a></li>
  </ol>
</div>

#### Extend Viam

You can also [create your own custom components or services](/program/extend/) for use with Viam, or use one of our [SDKs](/program/sdks/) to integrate a Viam robot with your own software application.

<script type="text/javascript" src="js/carousel-min.js"></script>
<link rel="stylesheet" href="css/carousel-min.css">
