---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam is a complete software platform for smart machines that runs on any 64-bit Linux OS and macOS."
weight: 1
no_list: true
type: "docs"
noToc: true
hide_feedback: true
sitemap:
  priority: 1.0
---

<div class="max-page">
  <p>
    Welcome to the Viam Documentation!
    Viam is a complete software platform for {{< glossary_tooltip term_id="smart-machine" text="smart machines">}} that runs on Linux and macOS and supports a wide variety of popular systems, including:
  </p>
</div>

<div id="board-carousel" class="carousel max-page">
  <ul tabindex="0">
  <li id="c1_slide0">
      <a href="get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="get-started/installation/thumbnails/raspberry-pi-5-8gb.png" resize="148x120" declaredimensions=true alt="Raspberry Pi 5">}}
        <p>Raspberry Pi 5</p>
      </a>
    </li>
    <li id="c1_slide1">
      <a href="get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="148x120" declaredimensions=true alt="Raspberry Pi 4b">}}
        <p>Raspberry Pi 4</p>
      </a>
    </li>
    <li id="c1_slide2">
      <a href="get-started/installation/prepare/jetson-nano-setup/">
        {{<imgproc src="get-started/installation/thumbnails/jetson-orin-nano.jpeg" resize="148x120" declaredimensions=true alt="NVIDIA Jetson Orin Nano">}}
        <p>NVIDIA Jetson Orin Nano</p>
      </a>
    </li>
    <li id="c1_slide3">
      <a href="components/board/upboard/">
        {{<imgproc src="get-started/installation/thumbnails/up_4000.png" resize="148x120" declaredimensions=true alt="Intel Up board 4000">}}
        <p>Intel UP4000</p>
      </a>
    </li>
    <li id="c1_slide4">
      <a href="get-started/installation/prepare/pumpkin/">
        {{<imgproc src="get-started/installation/thumbnails/pumpkin.png" resize="148x120" declaredimensions=true alt="Mediatek genio 500 pumpkin">}}
        <p>Mediatek Genio 500 Pumpkin</p>
      </a>
    </li>
    <li id="c1_slide5">
      <a href="/build/micro-rdk/">
        {{<imgproc src="get-started/installation/thumbnails/esp32-espressif.png" resize="148x120" declaredimensions=true alt="E S P 32 - espressif">}}
        <p>Espressif ESP32</p>
      </a>
    </li>
    <li id="c1_slide6">
      <a href="get-started/installation/prepare/sk-tda4vm/">
        {{<imgproc src="get-started/installation/thumbnails/tda4vm.png" resize="148x120" declaredimensions=true alt="S K - T D A 4 V M">}}
        <p>Texas Instruments TDA4VM</p>
      </a>
    </li>
    <li id="c1_slide7">
      <a href="get-started/installation/prepare/jetson-nano-setup/">
        {{<imgproc src="get-started/installation/thumbnails/jetson-nano-dev-kit.png" resize="148x120" declaredimensions=true alt="NVIDIA Jetson Nano">}}
        <p>NVIDIA Jetson Nano</p>
      </a>
    </li>
    <li id="c1_slide8">
      <a href="get-started/installation/prepare/jetson-agx-orin-setup/">
        {{<imgproc src="get-started/installation/thumbnails/jetson-agx-orin-dev-kit.png" alt="Jetson A G X Orin Developer Kit" resize="148x120" declaredimensions=true >}}
        <p>NVIDIA Jetson AGX Orin</p>
      </a>
    </li>
    <li id="c1_slide9">
      <a href="components/board/jetson/">
        {{<imgproc src="get-started/installation/thumbnails/jetson-xavier.png" alt="Jetson Xavier NX Dev Kit" resize="148x120" declaredimensions=true >}}
        <p>NVIDIA Jetson Xavier NX</p>
      </a>
    </li>
    <li id="c1_slide10">
      <a href="get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="get-started/installation/thumbnails/rpi-3.png" alt="Raspberry Pi 3" resize="148x120" declaredimensions=true >}}
        <p>Raspberry Pi 3</p>
      </a>
    </li>
    <li id="c1_slide11">
      <a href="get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="get-started/installation/thumbnails/raspberry-pi-zero-2w.png" alt="Raspberry Pi" resize="148x120" declaredimensions=true >}}
        <p>Raspberry Pi Zero 2 W</p>
      </a>
    </li>
    <li id="c1_slide12">
      <a href="get-started/installation/prepare/beaglebone-setup/">
        {{<imgproc src="get-started/installation/thumbnails/beaglebone.png" resize="148x120" declaredimensions=true alt="BeagleBone A I-64">}}
        <p>BeagleBone AI-64</p>
      </a>
    </li>
    <li id="c1_slide13">
      <a href="components/board/numato/">
        {{<imgproc src="get-started/installation/thumbnails/numato.png" alt="Numato GPIO Modules" resize="148x120" declaredimensions=true >}}
        <p>Numato GPIO Modules</p>
      </a>
    </li>
    <li id="c1_slide14">
      <a href="components/board/pca9685/">
        {{<imgproc src="get-started/installation/thumbnails/pca9685.png" alt="P C A 9685 I 2 C Interface" resize="148x120" declaredimensions=true >}}
        <p>PCA9686 I<sup>2</sup>C Interface</p>
      </a>
    </li>
  </ul>
  <ol style="visibility: hidden" aria-hidden="true">
    <li><a href="#c1_slide0">Raspberry Pi 5</a></li>
    <li><a href="#c1_slide1">Raspberry Pi 4</a></li>
    <li><a href="#c1_slide2">NVIDIA Jetson Orin Nano</a></li>
    <li><a href="#c1_slide3">Intel UP4000</a></li>
    <li><a href="#c1_slide4">Mediatek Genio 500 Pumpkin</a></li>
    <li><a href="#c1_slide5">Espressif ESP32</a></li>
    <li><a href="#c1_slide6">Texas Instruments TDA4VM</a></li>
    <li><a href="#c1_slide7">NVIDIA Jetson Nano</a></li>
    <li><a href="#c1_slide8">NVIDIA Jetson AGX Orin</a></li>
    <li><a href="#c1_slide9">NVIDIA Jetson Xavier NX</a></li>
    <li><a href="#c1_slide10">Raspberry Pi 3</a></li>
    <li><a href="#c1_slide11">Raspberry Pi Zero 2 W</a></li>
    <li><a href="#c1_slide12">BeagleBone AI-64</a></li>
    <li><a href="#c1_slide13">Numato GPIO Modules</a></li>
    <li><a href="#c1_slide14">PCA9686 I<sup>2</sup>C Interface</a></li>
  </ol>
  <div class="prev" style="display: block">‹</div>
  <div class="next" style="display: block">›</div>
</div>
<br>

<div class="max-page">
  <p>
    Explore more about the Viam platform or try it out for yourself:
  </p>
</div>

<div class="cards max-page">
  <div class="row">
      <div class="col hover-card landing yellow">
        <div>
          <div>Learn and Try</div>
          <p style="text-align: left;">
            Learn about <a href="/get-started/viam/">the Viam platform in 3 minutes</a> and then
            <a href="get-started/try-viam/">drive a Viam rover</a> from the comfort of your home or follow along with a <a href="tutorials/"> tutorial</a>.</p>
        </div>
        {{<gif webm_src="/rover.webm" mp4_src="/rover.mp4" alt="A Viam Rover moving about">}}
      </div>
      <div class="col hover-card landing purple">
        <div>
          <div>Configure your machine</div>
          <div style="text-align: left">
            <ol style="padding-inline-start: 1.1rem">
              <li>Configure a <a href="build/configure/"> machine</a> or a <a href="fleet/">fleet</a></li>
              <li><a href="get-started/installation/">Install Viam on your machine</a></li>
              <li>Configure <a href="components/">components</a> and <a href="services/">add services</a></li>
              <li><a href="fleet/machines/#control">Control and test your machine</a></li>
            </ol>
          </div>
        </div>
        {{<gif webm_src="/blink.webm" mp4_src="/blink.mp4" alt="A blinking L.E.D. connected to a Raspberry Pi">}}
      </div>
      <div class="col hover-card landing teal">
        <div>
          <div>Program your machine</div>
          <p style="text-align: left;">
            Program and control your machines in <a href="/build/program/apis/"> the languages you already know</a> like <a href="https://python.viam.dev/">Python</a>, <a href="https://pkg.go.dev/go.viam.com/rdk">Go</a>, <a href="https://ts.viam.dev/">TypeScript</a>, <a href="https://cpp.viam.dev/" target="_blank">C++</a>, or <a href="https://flutter.viam.dev/" target="_blank">Flutter</a>.
          </p>
        </div>
        <div class="hover-card-img">
          {{<imgproc src="/general/code.png" alt="Robot code" resize="400x" >}}
        </div>
      </div>
      <div class="col hover-card landing pink">
        <div>
          <div>Community</div>
          <p style="text-align: left;">Have questions, or want to meet other people working on smart machines? <a href="https://discord.gg/viam">Join us in the Community Discord!</a></p>
        </div>
        {{<gif webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart">}}
      </div>
    </div>
</div>

<h2>Capabilities and APIs</h2>

<div class="cards max-page">
  <div class="row">
    <div class="col sectionlist">
        <div>
        <div>Components</div>
        {{<sectionlist section="/components/">}}
        </div>
    </div>
    <div class="col sectionlist">
<div><div>Services</div><ul class="sectionlist"><li><a href="data/" title="Data Management Service"><div><picture><img src="services/icons/data-capture.svg" width="/services/icons/data-capture" height="/services/icons/data-capture" alt="Data Management" loading="lazy"></picture><p>Data Management</p></div></a></li></ul><ul class="sectionlist"><li><a href="mobility/motion/" title="Motion Service"><div><picture><img src="services/icons/motion.svg" width="/services/icons/motion" height="/services/icons/motion" alt="Motion" loading="lazy"></picture><p>Motion</p></div></a></li></ul><ul class="sectionlist"><li><a href="mobility/frame-system/" title="The Robot Frame System"><div><picture><img src="services/icons/frame-system.svg" width="/services/icons/frame-system" height="/services/icons/frame-system" alt="Frame System" loading="lazy"></picture><p>Frame System</p></div></a></li></ul><ul class="sectionlist"><li><a href="mobility/base-rc/" title="Base Remote Control Service"><div><picture><img src="services/icons/base-rc.svg" width="/services/icons/base-rc" height="/services/icons/base-rc" alt="Base Remote Control" loading="lazy"></picture><p>Base Remote Control</p></div></a></li></ul><ul class="sectionlist"><li><a href="ml/" title="ML Model Service"><div><picture><img src="services/icons/ml.svg" width="/services/icons/ml" height="/services/icons/ml" alt="ML Model" loading="lazy"></picture><p>ML Model</p></div></a></li></ul><ul class="sectionlist"><li><a href="mobility/navigation/" title="The Navigation Service"><div><picture><img src="services/icons/navigation.svg" width="/services/icons/navigation" height="/services/icons/navigation" alt="Navigation" loading="lazy"></picture><p>Navigation</p></div></a></li></ul><ul class="sectionlist"><li><a href="mobility/slam/" title="SLAM Service"><div><picture><img src="services/icons/slam.svg" width="/services/icons/slam" height="/services/icons/slam" alt="SLAM" loading="lazy"></picture><p>SLAM</p></div></a></li></ul><ul class="sectionlist"><li><a href="ml/vision/" title="Vision Service"><div><picture><img src="services/icons/vision.svg" width="/services/icons/vision" height="/services/icons/vision" alt="Vision" loading="lazy"></picture><p>Vision</p></div></a></li></ul></div>
    </div>
    <div class="col sectionlist">
        <div>
        <div>SDKs</div>
        {{<sectionlist section="/sdks">}}
        </div>
    </div>
  </div>
</div>

<h2>Popular Tutorials</h2>

<div class="cards max-page">
  <div class="row">
    {{< card link="/tutorials/services/data-mlmodel-tutorial/" class="green">}}
    {{< card link="/tutorials/services/plan-motion-with-arm-gripper/" class="pink">}}
    {{< card link="/tutorials/services/color-detection-scuttle/" class="purple">}}
    {{< card link="/tutorials/projects/integrating-viam-with-openai/" class="yellow">}}
  </div>
</div>
