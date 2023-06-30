---
title: "Installation Guide"
linkTitle: "Installation Guide"
childTitleEndOverwrite: "Try Viam"
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

To use Viam software with your robot, install and run the `viam-server` binary on the computer that you want to use to control the robot.
In most cases, this will be a [single board computer (SBC)](#install-on-a-single-board-computer), like a Raspberry Pi, but you can also install `viam-server` on a [macOS or Linux computer](#install-on-a-macos-or-linux-computer).

For an overview of the Viam software platform, see [Viam in 3 minutes](/viam/).

## Install on a single board computer

### Prepare your board

If you haven't already, you must install a supported operating system on your {{< glossary_tooltip term_id="board" text="board" >}}.
`viam-server` supports Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures.
If you are using one of the following boards, you can follow our guide for that board to prepare it for installation:

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" size="xs" %}}
{{% card link="/installation/prepare/beaglebone-setup/" size="xs" %}}
{{% card link="/installation/prepare/sk-tda4vm/" size="xs" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" size="xs" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" size="xs" %}}
{{% card link="/installation/prepare/microcontrollers" size="xs" %}}
{{< /cards >}}

### Install `viam-server`

Once you have a compatible operating system on your board, follow along with the video below or walk through the steps outlined beneath it to install `viam-server` on your board:

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

#### Installation steps

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Linux` for **Mode** and select the appropriate **Architecture** for your board.
   On most Linux operating systems, you can run `uname -m` to confirm your board's architecture.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your board.

1. Once `viam-server` is installed and running on your board, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your robot has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.

## Install on a macOS or Linux computer

You can also install `viam-server` on a macOS or Linux computer.
This is useful if you don't have a board available, or if you want to run a Viam [service](/services/) with your robot that requires more computing resources than is otherwise available on an SBC.
Select the tab below for your operating system:

{{< tabs name="Install on computer" >}}
{{% tab name="macOS computer" %}}

### Install on a macOS computer

`viam-server` is available for macOS users through [Homebrew](https://docs.brew.sh/Installation), and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Mac` for **Mode**.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your macOS computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{% tab name="Linux computer" %}}

### Install on a Linux computer

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.
To install `viam-server` on a Linux computer:

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Linux` for **Mode** and select the appropriate **Architecture** for your computer.
   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your Linux computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.

{{% /tab %}}
{{< /tabs >}}

## Local installation

If desired, you can also install and run `viam-server` locally without connecting to the [Viam app](https://app.viam.com).
This is useful for situations where you have limited internet access, or if your robot will never connect to the internet itself.
You can install `viam-server` in this fashion to a board (SBC), macOS computer, or Linux computer.
Select the tab below appropriate for your installation:

{{< tabs name="Local Installation" >}}
{{% tab name="Board (SBC)" %}}

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.
To install `viam-server` on a board:

1. If you haven't already, you must install a supported operating system on your board.
   Follow the instructions to [prepare your board](#prepare-your-board) to install a supported OS on your board.

2. Next, `ssh` to your board.
   Create your robot's [local configuration file](/appendix/local-configuration-file/), and save the file to <file>/etc/viam.json</file>.

3. Run `uname -m` to determine the architecture of your board.
   `viam-server` supports the `aarch64` and `x86_64` architectures.

<!-- The below has to be in HTML because we're using a table inside another table with indentation-->
<ol start="4">
<li>Select the tab below matching your board's architecture, and run the command listed to download, install, and start <code>viam-server</code> on your board.
We recommend the stable release for most users:

{{< tabs name="linux-board-architectures" >}}
{{% tab name="aarch64" %}}

**Stable:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

**Latest:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

{{% /tab %}}
{{% tab name="x86_64" %}}

**Stable:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

**Latest:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-x86_64.AppImage -o viam-server &&
  chmod 755 viam-server && sudo ./viam-server --aix-install
```

{{% /tab %}}
{{< /tabs >}}

</li>
</ol>

5. To make [configuration changes](/manage/configuration/) to your robot, edit the <file>/etc/viam.json</file> configuration file and save your changes.
   You can also use [the Viam app](https://app.viam.com) to [build and edit your configuration file](/appendix/local-configuration-file/#build-a-local-configuration-file-in-the-viam-app) and download it to your board, replacing the existing file.
   When you save your edits to the configuration file, `viam-server` applies those changes immediately -- there is no need to restart `viam-server` to apply changes.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.

{{% /tab %}}
{{% tab name="macOS computer" %}}

`viam-server` is available for macOS users through [Homebrew](https://docs.brew.sh/Installation), and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. First, run the following command to download and install `viam-server` on your macOS computer using `brew`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   brew tap viamrobotics/brews && brew install viam-server
   ```

2. Next, copy the provided example configuration file to a convenient location on your filesystem.
   The following example places the file in your home directory:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cp /opt/homebrew/etc/viam.json ~/viam.json
   ```

   This configuration file contains some example [component](/components/) and [service](/services/) configurations, as well as an example of a {{< glossary_tooltip term_id="process" text="process" >}}.

3. Then, start `viam-server` with the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam-server -config ~/viam.json
   ```

4. To make [configuration changes](/manage/configuration/) to your robot, edit the <file>~/viam.json</file> configuration file and save your changes.
   You can also use [the Viam app](https://app.viam.com) to [build and edit your configuration file](/appendix/local-configuration-file/#build-a-local-configuration-file-in-the-viam-app) and download it to your macOS computer, replacing the existing file.
   When you save your edits to the configuration file, `viam-server` applies those changes immediately -- there is no need to restart `viam-server` to apply changes.

{{% /tab %}}
{{% tab name="Linux computer" %}}

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.
To install `viam-server` on a Linux computer:

1. On your Linux computer, create your robot's [local configuration file](/appendix/local-configuration-file/), and save the file to <file>~/viam.json</file>.

2. Run `uname -m` on the command line to determine your system architecture.
   `viam-server` supports the `aarch64` and `x86_64` architectures.

<!-- The below has to be in HTML because we're using a table inside another table with indentation-->
<ol start="3">
<li>Select the tab below matching your computer's architecture, and run the command listed to download and install <code>viam-server</code> on your Linux computer.
We recommend the stable release for most users:

{{< tabs name="linux-computer-architectures" >}}
{{% tab name="aarch64" %}}

**Stable:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage -o viam-server &&
  chmod 755 viam-server
```

**Latest:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage -o viam-server &&
  chmod 755 viam-server
```

{{% /tab %}}
{{% tab name="x86_64" %}}

**Stable:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server &&
  chmod 755 viam-server
```

**Latest:**

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-x86_64.AppImage -o viam-server &&
  chmod 755 viam-server
```

{{% /tab %}}
{{< /tabs >}}

</li>
</ol>

4. Start `viam-server`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   ./viam-server -config ~/viam.json
   ```

5. _Optional:_ If you would like to run `viam-server` as a system service, run the following command to move the binary to a system location and install a service file for use with `systemd`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sudo ./viam-server --aix-install
   ```

   When you run this command, `viam-server` is configured to start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.

   In addition, this command also installs an example configuration file at <file>/etc/viam.json</file>, and configures `viam-server` to use this file as its configuration file.
   If you have already created a configuration file at <file>~/viam.json</file>, you can copy it to the location that the system service expects it to be with the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sudo cp ~/viam.json /etc/viam.json
   ```

6. To make [configuration changes](/manage/configuration/) to your robot, edit the configuration file and save your changes.
   You can also use [the Viam app](https://app.viam.com) to [build and edit your configuration file](/appendix/local-configuration-file/#build-a-local-configuration-file-in-the-viam-app) and download it to your Linux computer, replacing the existing file.
   When you save your edits to the configuration file, `viam-server` applies those changes immediately -- there is no need to restart `viam-server` to apply changes.

{{% /tab %}}
{{< /tabs >}}

## Next Steps

{{< cards >}}
  {{% card link="/installation/manage" size="small" %}}
  {{% card link="/installation/update" size="small" %}}
{{< /cards >}}
