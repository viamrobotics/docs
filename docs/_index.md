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
    <li id="c1_slide1">
      <a href="get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="148x120" declaredimensions=true alt="Raspberry Pi">}}
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
      <a href="build/configure/components/board/upboard/">
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
      <a href="build/configure/components/board/jetson/">
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
        <p>Raspberry Pi Zero 2W</p>
      </a>
    </li>
    <li id="c1_slide12">
      <a href="get-started/installation/prepare/beaglebone-setup/">
        {{<imgproc src="get-started/installation/thumbnails/beaglebone.png" resize="148x120" declaredimensions=true alt="BeagleBone A I-64">}}
        <p>BeagleBone AI-64</p>
      </a>
    </li>
    <li id="c1_slide13">
      <a href="build/configure/components/board/numato/">
        {{<imgproc src="get-started/installation/thumbnails/numato.png" alt="Numato GPIO Modules" resize="148x120" declaredimensions=true >}}
        <p>Numato GPIO Modules</p>
      </a>
    </li>
    <li id="c1_slide14">
      <a href="build/configure/components/board/pca9685/">
        {{<imgproc src="get-started/installation/thumbnails/pca9685.png" alt="P C A 9685 I 2 C Interface" resize="148x120" declaredimensions=true >}}
        <p>PCA9686 I<sup>2</sup>C Interface</p>
      </a>
    </li>
  </ul>
  <ol style="visibility: hidden" aria-hidden="true">
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
    <li><a href="#c1_slide11">Raspberry Pi Zero 2W</a></li>
    <li><a href="#c1_slide12">BeagleBone AI-64</a></li>
    <li><a href="#c1_slide13">Numato GPIO Modules</a></li>
    <li><a href="#c1_slide14">PCA9686 I<sup>2</sup>C Interface</a></li>
  </ol>
  <div class="prev" style="display: block">‹</div>
  <div class="next" style="display: block">›</div>
</div>
<br>

<div class="max-page">
  <h3>
    Start with these common use cases
  </h3>
</div>

<div class="cards max-page">
  <div class="row">
    <div class="col sectionlist">
        <div>
        <ul class="sectionlist">
        <li><a href="build/configure/"><div><p>Configure resources for machines</p></div></a></li>
        <li><a href="registry/"><div><p>Add functionality with modules</p></div></a></li>
        <li><a href="build/program/"><div><p>Deploy code</p></div></a></li>
        </ul>
        </div>
    </div>
    <div class="col sectionlist">
        <div>
        <ul class="sectionlist">
        <li><a href="fleet/"><div><p>Manage fleets of machines</p></div></a></li>
        <li><a href="mobility/motion/"><div><p>Add motion to machines</p></div></a></li>
        <li><a href="tutorials/services/navigate-with-rover-base/"><div><p>Navigate with rovers</p></div></a></li>
        </ul>
        </div>
    </div>
    <div class="col sectionlist">
        <div>
        <ul class="sectionlist">
        <li><a href="data/"><div><p>Manage and Sync Data</p></div></a></li>
        <li><a href="ml/"><div><p>Train machine learning models</p></div></a></li>
        <li><a href="ml/vision/" target="_blank"><div><p>Use Computer Vision</p></div></a></li>
        </ul>
        </div>
    </div>
  </div>
</div>

<div class="max-page">
  <h3>
    Follow popular tutorials
  </h3>
</div>

<div class="cards max-page">
  <div class="row">
    {{< card link="/tutorials/services/data-mlmodel-tutorial/" class="green">}}
    {{< card link="/tutorials/services/plan-motion-with-arm-gripper/" class="pink">}}
    {{< card link="/tutorials/services/navigate-with-rover-base/" class="yellow">}}
    {{< card link="/tutorials/services/color-detection-scuttle/" class="purple">}}
  </div>
</div>
<br>
<div class="max-page">
  <h3>
    Browse by product
  </h3>
</div>

<div class="cards max-page">
  <div class="row">
    <div class="col sectionlist">
        <div>
        <div>Build smart machines</div>
        <br>
        <p>Simplify smart machine creation, configuration, and customization.</p>
        <ul class="sectionlist">
        <li><a href="build/configure/"><div><p>Configuration</p></div></a></li>
        <li><a href="build/configure/components/"><div><p>Components</p></div></a></li>
        <li><a href="build/configure/services/"><div><p>Services</p></div></a></li>
        <li><a href="build/configure/parts-and-remotes/"><div><p>Robot Architecture</p></div></a></li>
        <li><a href="build/micro-rdk/"><div><p>Microcontrollers</p></div></a></li>
        </ul>
        </div>
    </div>
    <div class="col sectionlist">
      <div>
        <div>Fleet management</div>
        <br>
        <p>Launch, monitor, and update all smart machines from a unified display.</p>
        <ul class="sectionlist">
        <li><a href="build/configure/"><div><p>Machines</p></div></a></li>
        <li><a href="build/configure/components/"><div><p>Locations</p></div></a></li>
        <li><a href="build/configure/services/"><div><p>Organizations</p></div></a></li>
        <li><a href="build/program/"><div><p>CLI</p></div></a></li>
        </ul>
      </div>
    </div>
    <div class="col sectionlist">
        <div>
        <div>Data Management</div>
        <br>
        <p>Capture, store, sync, view, and analyze machine data.</p>
        <ul class="sectionlist">
        <li><a href="data/capture/"><div><p>Capture machine data
</p></div></a></li>
        <li><a href="data/cloud-sync/"><div><p>Sync to the cloud
</p></div></a></li>
        <li><a href="data/view/"><div><p>Retrieve or view data
</p></div></a></li>
        <li><a href="data/datasets"><div><p>Prepare data for training models
</p></div></a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col sectionlist">
        <div>
        <div>Registry</div>
        <br>
        <p>Easily add and deploy custom drivers, services, or your own code to your smart machine.</p>
        <ul class="sectionlist">
        <li><a href="registry/configure/"><div><p>Find and use modules
</p></div></a></li>
        <li><a href="registry/create/"><div><p>Build new drivers</p></div></a></li>
        <li><a href="registry/upload/"><div><p>Upload to the registry</p></div></a></li>
        </ul>
      </div>
    </div>
    <div class="col sectionlist">
        <div>
        <div>Mobility</div>
        <br>
        <p>Make smart machines move and navigate where they need to go.</p>
        <ul class="sectionlist">
        <li><a href="mobility/frame-system/"><div><p>Frame System</p></div></a></li>
        <li><a href="mobility/motion/"><div><p>Motion Service</p></div></a></li>
        <li><a href="mobility/slam/"><div><p>SLAM Service</p></div></a></li>
        <li><a href="mobility/navigation/"><div><p>Navigation Service
</p></div></a></li>
        </ul>
      </div>
    </div>
    <div class="col sectionlist">
        <div>
        <div>Machine Learning</div>
        <br>
        <p>Collect and label data to train and deploy machine learning models that enhance smart machine performance.</p>
        <ul class="sectionlist">
        <li><a href="ml/train-model/"><div><p>Train a model</p></div></a></li>
        <li><a href="ml/upload-model/"><div><p>Upload a model</p></div></a></li>
        <li><a href="ml/deploy-model/"><div><p>Deploy a model</p></div></a></li>
        <li><a href="ml/vision/"><div><p>Use Computer Vision
</p></div></a></li>
        </ul>
      </div>
    </div>
</div>
<br>
<div class="max-page">
  <h3>
    Find out more
  </h3>
</div>
<div class="cards max-page">
  <div class="row">
    <div class="col sectionlist">
        <div>
        <div>Get Started</div>
        <ul class="sectionlist">
        <li><a href="build/get-started/try-viam/"><div><p>Try Viam</p></div></a></li>
        <li><a href="build/get-started/viam/"><div><p>Viam in 3 minutes</p></div></a></li>
        <li><a href="build/machine/"><div><p>Configure a machine</p></div></a></li>
        <li><a href="build/program/"><div><p>Program a machine</p></div></a></li>
        </ul>
        </div>
    </div>
    <div class="col sectionlist">
        <div>
        <div>SDKs</div>
        {{<sectionlist section="/reference/sdks">}}
        </div>
    </div>
     <div class="col sectionlist">
        <div>
        <div>Learn and Share</div>
        <ul class="sectionlist">
        <li><a href="tutorials/"><div><p>Follow tutorials</p></div></a></li>
        <li><a href="https://discord.gg/viam"><div><p>Join the community discord</p></div></a></li>
        </ul>
        </div>
    </div>
  </div>
</div>
