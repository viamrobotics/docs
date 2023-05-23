---
title: "Installation Guide"
linkTitle: "Installation Guide"
weight: 20
no_list: true
type: docs
icon: "/installation/img/thumbnails/install.png"
images: ["/installation/img/thumbnails/install.png"]
aliases:
    - /installation/prepare/
    - /installation/macos-install/
    - /installation/linux-install/
    - /installation/install/
    - /installation/install/linux-install/
    - /installation/install/macos-install
    - /getting-started/installation/
    - /getting-started/macos-install/
    - /getting-started/linux-install/
---

To use Viam software with your robot, you need to install and run a binary called `viam-server` on the computer you want to use to control the robot.
See [What is Viam?](/viam/) for more information.

## Preparation

Make sure your system is compatible with Viam.
You can run `viam-server` on any device that runs:

- **any** Linux 64-bit operating system
- macOS

<div class="container text-left td-max-width-on-larger-screens">
    <div class="row">
        <img src="img/thumbnails/pc.png" style="max-width:100px" alt="Desktop computer">
        <div class="col">
            <p> If you plan to run <code>viam-server</code> on your laptop or desktop with a Linux or Mac operating system, no special prep is required. Proceed to <a href="#install-viam-server">Install <code>viam-server</code></a>. </p>
        </div>
    </div>
</div>

<br>

If you are using a single board computer (SBC) or a microcontroller, prepare your device by following the relevant setup document:

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" size="xs" %}}
{{% card link="/installation/prepare/beaglebone-setup/" size="xs" %}}
{{% card link="/installation/prepare/sk-tda4vm/" size="xs" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" size="xs" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" size="xs" %}}
{{% card link="/installation/prepare/microcontrollers" size="xs" %}}
{{< /cards >}}

## Install `viam-server`

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

Once you have a compatible operating system on your computer, you are ready to install `viam-server`.

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots#add-a-new-robot).
   If this is your first time using the Viam app, you first need to create an account.
2. Click the **Setup** tab on your robot page.
3. Select the **Mode** and **Architecture** settings for your device.
4. Follow the steps on the **Setup** tab to install `viam-server`.
   Also detailed in [Detailed Installation Instructions](#detailed-installation-instructions).

### Detailed Installation Instructions

{{< tabs name="Detailed Installation Instructions" >}}
{{% tab name="Linux"%}}

`viam-server` is distributed as an AppImage.
The AppImage is a single, self-contained binary that runs on any Linux system (except FUSE) with the correct CPU architecture, with no need to install any dependencies.

1. **Download the Viam app config to your computer.** `viam-server` uses this config file to connect to app.viam.com.
   This connection allows the robot to pull its full configuration information and allows you to monitor and control your robot from the Viam app.
   Download your robot's config file from the **Setup** tab of your robot on the Viam app. </li>

<!-- The below has to be in HTML because we're using a table inside another table with indentation-->
<ol start="2">
<li> <strong>Download and install <code>viam-server</code>.</strong>

   Run `viam-server` locally on your Mac with the config you just downloaded.
   Replace `<YOUR_ROBOT_NAME>` with the name of your robot from the Viam app.

   To determine the CPU architecture (x86_64 or aarch64) of your device, run `uname -m` on the command line.
   Raspberry Pi and Jetson boards are aarch64 and most desktops and laptops are x86_64.

{{< tabs name="different-architectures" >}}
{{% tab name="Aarch64"%}}

Stable:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

Latest:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

{{% /tab %}}
{{% tab name="X86_64"%}}

Stable:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

Latest:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-x86_64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

{{% /tab %}}
{{< /tabs >}}

If you do not want to run `viam-server` as a service, you can also [run it manually as a binary](#start-manually-from-the-command-line).

</li>
</ol>

3. **Connect and configure.** Go to the **Setup** page on the Viam app and wait for confirmation that your robot has successfully connected.

{{% /tab %}}
{{% tab name="macOS"%}}

`viam-server` is available for macOS users through [Homebrew](https://docs.brew.sh/Installation).

1. **Install `viam-server` on your Mac**

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   brew tap viamrobotics/brews && brew install viam-server
   ```

2. **Download the Viam app config to your Mac.** `viam-server` uses this config file to connect to app.viam.com.
   This connection allows the robot to pull its full configuration information and allows you to monitor and control your robot from the Viam app.
   Download your robot's config file from the **Setup** tab of your robot on the Viam app.

3. **Start `viam-server` on your Mac.** Run `viam-server` locally on your Mac with the config you just downloaded.
   Replace `<YOUR_ROBOT_NAME>` with the name of your robot from the Viam app.

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam-server -config ~/Downloads/viam-<YOUR_ROBOT_NAME>-main.json
   ```

4. **Connect and configure.** Go to the **Setup** page on the Viam app and wait for confirmation that your robot has successfully connected.

{{% /tab %}}
{{< /tabs >}}

### Starting `viam-server` on Linux

To run `viam-server`, you have two options:

#### Start manually from the command line

To run `viam-server` directly from the command line, you can use the following command, replacing "myconfig" with the name of your configuration file.
`sudo` is necessary on some devices to access hardware.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo ./viam-server -config myconfig.json
```

#### Start automatically on boot

If you install `viam-server` as a system service, `viam-server` starts automatically every time you boot your device.
Note that this is the default way `viam-server` is set up if you follow the **Setup** tab instructions on the [Viam app](https://app.viam.com).

For this setup your configuration file must be at <file>/etc/viam.json</file>.

The following command creates a systemd service file at <file>/etc/systemd/system/viam-server.service</file> and sets it to start on boot, using a config placed at <file>/etc/viam.json</file>.
It will also move the actual binary (AppImage) to <file>/usr/local/bin/viam-server</file> (regardless of the previous filename).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo ./viam-server --aix-install
```

Start the service by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl start viam-server
```

The service is an AppImage and will check for updates and self-update automatically each time the service is started.
Self-updates can take a couple of minutes, so the service may sometimes take a moment to start while this runs.
You can disable this by commenting out the ExecPre line (the one with --aix-update on it) in the service file.

## Next Steps

{{< cards >}}
  {{% card link="/installation/manage" size="small" %}}
  {{% card link="/installation/update" size="small" %}}
{{< /cards >}}
