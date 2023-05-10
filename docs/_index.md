---
title: "Welcome to the Viam Documentation"
linkTitle: "Viam Documentation"
weight: 1
no_list: true
type: "docs"
hide_feedback: true
---

Viam is a complete software platform for robots.

{{< alert title="New to Viam?" color="tip" >}}
Learn about [the Viam platform in 3 minutes](viam).
{{< /alert >}}

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" size="xs" %}}
{{% card link="/installation/prepare/beaglebone-setup/" size="xs" %}}
{{% card link="/installation/prepare/sk-tda4vm/" size="xs" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" size="xs" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" size="xs" %}}
{{% card link="/installation/prepare/microcontrollers" size="xs" %}}
{{< /cards >}}

<div class="container td-max-width-on-larger-screens">
  <div class="row">
    <div class="col landing-hover-card">
        <div class="landing-hover-card-padding yellow">
            <h4>Try Viam</h4>
            <p style="text-align: left;"><a href="try-viam">Drive a Viam rover</a> from the comfort of your home right now or follow along with some <a href="tutorials">example robot tutorials</a>.</p>
            {{<gif webm_src="img/rover.webm" mp4_src="img/rover.mp4" alt="A Viam Rover moving about">}}
        </div>
    </div>
    <div class="col landing-hover-card ">
        <div class="landing-hover-card-padding purple">
        <h4>Configure your robots</h4>
        <div style="text-align: left">
            <ol style="padding-inline-start: 1.1rem">
            <li><a href="/manage/fleet/robots/">Set up your robot</a> or<a href="manage/fleet/"> fleet</a></li>
            <li><a href="installation">Install Viam on your robot</a></li>
            <li><a href="manage/configuration/">Configure your robot</a></li>
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
            Program and control your robots in <a href="program/sdk-as-client/"> the languages you already know</a> like <a href="https://python.viam.dev/">Python</a>, <a href="https://pkg.go.dev/go.viam.com/rdk">Go</a>, or <a href="https://ts.viam.dev/">TypeScript</a>.
        </p>
        <img src="img/code.png" alt="Robot code">
        </div>
    </div>
    <div class="col landing-hover-card">
        <div class="landing-hover-card-padding pink">
        <a href="https://discord.gg/viam">
            <h4>Community</h4>
            <p style="text-align: left;">Have questions, or want to meet other people working on robots? Join us in the Community Discord!</p>
            {{<gif webm_src="img/heart.webm" mp4_src="img/heart.mp4" alt="A robot drawing a heart">}}
        </a>
        </div>
    </div>
    </div>
</div>
