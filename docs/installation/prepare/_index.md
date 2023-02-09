---
title: "Prepare Your Computer"
linkTitle: "Prepare Your Computer"
weight: 10
no_list: true
type: docs
draft: false
icon: "img/thumbnails/viam-icon-board.png"
description: "Prepare your computer before installing viam-server."
---

Make sure your system is compatible with Viam.
Viam is supported on:

- Linux 64-bit operating systems
- macOS

<div class="container text-left">
    <div class="row">
        <img src="../img/thumbnails/pc.png" style="max-width:100px" alt="Desktop computer">
        <div class="col">
            <br>
            <p> If you plan to run <code>viam-server</code> on your laptop or desktop with a Linux or Mac operating system, no special prep is required. Proceed to <a href="/installation/install/">install <code>viam-server</code></a>. </p>
        </div>
    </div>
</div>


If you are using a single board computer (SBC) like a Raspberry Pi or BeagleBone, prepare your SBC by following the relevant setup document:

{{< tabs name="TabPanelExample" >}}
{{% tab name="BeagleBone AI-64"%}}

{{< readfile "beaglebone-install.md" >}}

{{% /tab %}}

{{% tab name="Raspberry Pi" %}}

{{< readfile "rpi-setup.md" >}}

{{% /tab %}}

{{% tab name="SK-TDA4VM" %}}

{{< readfile "sk-tda4vm.md" >}}


{{% /tab %}}

{{< /tabs >}}