---
title: "Build a simple smart machine"
linkTitle: "Build simple smart machines"
weight: 10
type: "docs"
description: "Build a simple robot in a few steps."
tags: ["components", "configuration"]
---

You can get a smart machine running with Viam in just a few steps.

Viam's modular system of {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} means that you can start doing interesting things with your machine without writing much or any code.

<table>
  <tr>
    <th>{{<imgproc src="/use-cases/signup-narrow.png" class="fill alignleft" resize="500x" style="max-width: 200px" declaredimensions=true alt="Viam app login screen.">}}
      <b>1. Create a machine in the Viam app</b><br><br>
      <p>First, <a href="https://app.viam.com/">create a Viam account</a> if you haven't already. Log in.</p>
      <p>Then create a machine by typing in a name and clicking <strong>Add machine</strong>.</p>
      <p>{{<imgproc src="/use-cases/new-machine.png" class="fill aligncenter" resize="400x" style="max-width: 250px" declaredimensions=true alt="Viam app login screen.">}}</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/data-capture.svg" class="fill alignright" style="max-width: 150px" declaredimensions=true alt="Installation icon">}}
      <b>2. Install Viam on your machine</b><br><br>
      <p>All of the software that runs your smart machine is packaged into a binary called <code>viam-server</code>.
      Install it on the computer controlling your smart machine by following the steps on your machine's <strong>Setup</strong> tab in the <a href="https://app.viam.com/">Viam app</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/icons/components.png" class="fill alignleft" resize="400x" style="max-width: 220px" declaredimensions=true alt="An assortment of components.">}}
      <b>3. Configure your components</b><br><br>
      <p>Each piece of your smart machine that is controlled by a computer is called a <i>component</i>. For example, if your smart machine includes a Raspberry Pi, a motor, and a camera, each of those is a component.</p>
      <p>You need to <i><a href="/build/configure/">configure</a></i> your machine so that <code>viam-server</code> can interact with its hardware. Use the configuration builder tool in the Viam app to create a file that describes what hardware you are using and how it is connected.
      For example, if you have a DC motor, follow the <a href="/components/motor/gpio/">corresponding configuration instructions</a> to tell the software which pins it is connected to.</p>
    </th>
  </tr>
  <tr>
    <th>{{<gif webm_src="/tutorials/lazy-susan/control-dcmotor.webm" mp4_src="/tutorials/lazy-susan/control-dcmotor.mp4" alt="The Viam app Control tab with a control panel for each component. The panel for a DC motor is clicked, expanding to show power controls." max-width="400px" class="fill alignleft">}}
      <b>4. Test your components</b><br><br>
      <p>When you configure a component, a remote control panel is generated for it in the <b>Control</b> tab of the Viam app. Here, you can drive motors at different speeds, view your camera feed, see sensor readings, and generally test the basic functionality of your robot before you've even written any code.
      </p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignright" style="max-width: 220px"  declaredimensions=true alt="Services">}}
      <b>5. Configure services</b><br><br>
      <p>Services are built-in Viam software packages that add high-level functionality to your smart machine like computer vision or motion planning.
      If you want to use any services, see their <a href="/services/">documentation</a> for configuration and usage information.
      If you are making a simple machine that doesn't use services, you can skip this step!
      </p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/configure.svg" class="fill alignleft" style="max-width: 210px"  declaredimensions=true alt="Services">}}
      <b>6. Do more with code</b><br><br>
      <p>Write a program to control your smart machine using the programming language of your choice. Viam has <a href="/sdks/">SDKs</a> for Python, Golang, C++, TypeScript and Flutter.</p>
      <p>The easiest way to get started is to copy the auto-generated boilerplate code from your machine's <b>Code sample</b> tab in the Viam app. You can run this code directly on the machine or from a separate computer; it will connect to the machine using API keys.</p>
    </th>
  </tr>
</table>

## Next steps

{{< cards >}}
{{% card link="/get-started/try-viam/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{< /cards >}}
