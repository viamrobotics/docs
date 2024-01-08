---
title: "Platform"
linkTitle: "Platform"
description: "Use Viam to configure, program, operate, manage, and collect data from your smart machines."
weight: 400
type: docs
---

Viam is a complete software platform for {{< glossary_tooltip term_id="smart-machine" text="smart machines">}} that runs on Linux and macOS and supports a wide variety of popular systems, including:

<div id="board-carousel" class="carousel max-page">
  <ul tabindex="0">
  <li id="c1_slide0">
      <a href="/get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/raspberry-pi-5-8gb.png" resize="148x120" declaredimensions=true alt="Raspberry Pi 5">}}
        <p>Raspberry Pi 5</p>
      </a>
    </li>
    <li id="c1_slide1">
      <a href="/get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="148x120" declaredimensions=true alt="Raspberry Pi 4b">}}
        <p>Raspberry Pi 4</p>
      </a>
    </li>
    <li id="c1_slide2">
      <a href="/get-started/installation/prepare/jetson-nano-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/jetson-orin-nano.jpeg" resize="148x120" declaredimensions=true alt="NVIDIA Jetson Orin Nano">}}
        <p>NVIDIA Jetson Orin Nano</p>
      </a>
    </li>
    <li id="c1_slide3">
      <a href="/components/board/upboard/">
        {{<imgproc src="/get-started/installation/thumbnails/up_4000.png" resize="148x120" declaredimensions=true alt="Intel Up board 4000">}}
        <p>Intel UP4000</p>
      </a>
    </li>
    <li id="c1_slide4">
      <a href="/get-started/installation/prepare/pumpkin/">
        {{<imgproc src="/get-started/installation/thumbnails/pumpkin.png" resize="148x120" declaredimensions=true alt="Mediatek genio 500 pumpkin">}}
        <p>Mediatek Genio 500 Pumpkin</p>
      </a>
    </li>
    <li id="c1_slide5">
      <a href="/build/micro-rdk/">
        {{<imgproc src="/get-started/installation/thumbnails/esp32-espressif.png" resize="148x120" declaredimensions=true alt="E S P 32 - espressif">}}
        <p>Espressif ESP32</p>
      </a>
    </li>
    <li id="c1_slide6">
      <a href="/get-started/installation/prepare/sk-tda4vm/">
        {{<imgproc src="/get-started/installation/thumbnails/tda4vm.png" resize="148x120" declaredimensions=true alt="S K - T D A 4 V M">}}
        <p>Texas Instruments TDA4VM</p>
      </a>
    </li>
    <li id="c1_slide7">
      <a href="/get-started/installation/prepare/jetson-nano-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/jetson-nano-dev-kit.png" resize="148x120" declaredimensions=true alt="NVIDIA Jetson Nano">}}
        <p>NVIDIA Jetson Nano</p>
      </a>
    </li>
    <li id="c1_slide8">
      <a href="/get-started/installation/prepare/jetson-agx-orin-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/jetson-agx-orin-dev-kit.png" alt="Jetson A G X Orin Developer Kit" resize="148x120" declaredimensions=true >}}
        <p>NVIDIA Jetson AGX Orin</p>
      </a>
    </li>
    <li id="c1_slide9">
      <a href="/components/board/jetson/">
        {{<imgproc src="/get-started/installation/thumbnails/jetson-xavier.png" alt="Jetson Xavier NX Dev Kit" resize="148x120" declaredimensions=true >}}
        <p>NVIDIA Jetson Xavier NX</p>
      </a>
    </li>
    <li id="c1_slide10">
      <a href="/get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/rpi-3.png" alt="Raspberry Pi 3" resize="148x120" declaredimensions=true >}}
        <p>Raspberry Pi 3</p>
      </a>
    </li>
    <li id="c1_slide11">
      <a href="/get-started/installation/prepare/rpi-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/raspberry-pi-zero-2w.png" alt="Raspberry Pi" resize="148x120" declaredimensions=true >}}
        <p>Raspberry Pi Zero 2 W</p>
      </a>
    </li>
    <li id="c1_slide12">
      <a href="/get-started/installation/prepare/beaglebone-setup/">
        {{<imgproc src="/get-started/installation/thumbnails/beaglebone.png" resize="148x120" declaredimensions=true alt="BeagleBone A I-64">}}
        <p>BeagleBone AI-64</p>
      </a>
    </li>
    <li id="c1_slide13">
      <a href="/components/board/numato/">
        {{<imgproc src="/get-started/installation/thumbnails/numato.png" alt="Numato GPIO Modules" resize="148x120" declaredimensions=true >}}
        <p>Numato GPIO Modules</p>
      </a>
    </li>
    <li id="c1_slide14">
      <a href="/components/board/pca9685/">
        {{<imgproc src="/get-started/installation/thumbnails/pca9685.png" alt="P C A 9685 I 2 C Interface" resize="148x120" declaredimensions=true >}}
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

Explore the elements of the Viam platform:

{{< cards >}}
{{% card link="/build" %}}
{{% card link="/registry" %}}
{{% card link="/fleet" %}}
{{% card link="/data" %}}
{{% card link="/ml" %}}
{{% card link="/mobility" %}}
{{< /cards >}}
