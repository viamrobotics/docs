---
title: "Build a simple smart machine"
linkTitle: "Build simple smart machines"
weight: 10
type: "docs"
description: "Build a simple robot in a few steps."
tags: ["components", "configuration"]
---

You can get a smart machine running with Viam in just a few steps.
Install all the necessary Viam software and connect your robot to the cloud for remote control with two terminal commands.
Then copy-paste starter code that Viam automatically generates for your specific robot to start controlling it programatically right away.

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
    <th>{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Installation icon">}}
      <b>2. Install Viam on your machine</b><br><br>
      <p>All of the software that runs your robot is packaged into a binary called <code>viam-server</code>.
      Install it on the computer controlling your smart machine by following the steps on your machine's <strong>Setup</strong> tab in the <a href="https://app.viam.com/">Viam app</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/icons/components.png" class="fill alignleft" resize="400x" style="max-width: 210px" declaredimensions=true alt="An assortment of components.">}}
      <b>3. Configure components</b><br><br>
      <p>Each piece of your smart machine that is controlled by a computer is called a <i>component</i>. For example, if your smart machine includes a Raspberry Pi, a motor, and a camera, each of those is a component.</p>
      <p>You need to <i><a href="/build/configure/">configure</a></i> your machine so that <code>viam-server</code> can interact with its hardware. Use the configuration builder tool in the Viam app to create a file that describes what hardware you are using and how it is connected.
      For example, if you have a DC motor, follow the <a href="/components/motor/gpio/">corresponding configuration instructions</a> to tell the software which pins it is connected to.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/ml/collect.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Services">}}
      <b>4. Configure services</b><br><br>
      <p>Services are built-in Viam software packages that add high-level functionality to your smart machine like computer vision or motion planning.
      Depending on what you are doing, you may not need to configure any services on your smart machine.
      </p>
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
