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

If you haven't already, you must install a supported operating system to your {{< glossary_tooltip term_id="board" text="board" >}}.
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

1. Click the **Setup** tab on your robot page.

1. Select `Linux` under **Mode** and select the appropriate **Architecture** for your board.
   On most Linux operating systems, you can run `uname -m` to confirm your board's architecture.

1. Follow the steps on the **Setup** tab to install `viam-server` on your board.

1. Once `viam-server` is installed and running on your board, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your robot has successfully connected.

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

1. Click the **Setup** tab on your robot page.

1. Select `Mac` under **Mode**

1. Follow the steps on the **Setup** tab to install `viam-server` on your macOS computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{% tab name="Linux computer" %}}

### Install on a Linux computer

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.
To install `viam-server` on a Linux computer:

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. Click the **Setup** tab on your robot page.

1. Select `Linux` under **Mode** and select the appropriate **Architecture** for your computer.
   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

1. Follow the steps on the **Setup** tab to install `viam-server` on your Linux computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

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

1. Next, `ssh` to your board and run `uname -m` to determine the architecture of your board.
   `viam-server` supports the `aarch64` and `x86_64` architectures.

<!-- The below has to be in HTML because we're using a table inside another table with indentation-->
<ol start="3">
<li>Select the tab below matching your board's architecture, and run the command listed to download and install <code>viam-server</code> on your board.
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

4. Create your robot's [configuration file](/installation/configuration-file/), and save the file to <file>/etc/viam.json</file>.

5. Then, start `viam-server` on your board with the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sudo systemctl start viam-server
   ```

6. To make configuration changes to your robot, edit the <file>/etc/viam.json</file> configuration file, then stop and restart `viam-server`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sudo systemctl stop viam-server
   sudo systemctl start viam-server
   ```

{{% /tab %}}
{{% tab name="macOS computer" %}}

`viam-server` is available for macOS users through [Homebrew](https://docs.brew.sh/Installation), and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. First, run the following command to download and install `viam-server` on your macOS computer using `brew`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   brew tap viamrobotics/brews && brew install viam-server
   ```

1. Next, copy the example configuration file to a convenient location on your filesystem.
   The following example places the file in your home directory:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cp /opt/homebrew/etc/viam.json ~/viam.json
   ```

   This example configuration file contains some example [component](/components/) and [service](/services/) configurations, as well as an example of a {{< glossary_tooltip term_id="process" text="process" >}}. See [Configuration file](/installation/configuration-file/) for more information.

1. Then, start `viam-server` with the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam-server -config ~/viam.json
   ```

1. To make configuration changes to your robot, edit the <file>~/viam.json</file> configuration file, then stop and restart `viam-server`.
   You can also build a configuration file on the [Viam app](https://app.viam.com) without connecting your robot to it.
   Use the **Config** tab to add and configure the components and services you'll be using, then switch the **Mode** to `Raw JSON` to view and download your configuration file.

{{% /tab %}}
{{% tab name="Linux computer" %}}

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.
To install `viam-server` on a Linux computer:

1. Run `uname -m` on your Linux computer's command line to determine your system architecture.
   `viam-server` supports the `aarch64` and `x86_64` architectures.

<!-- The below has to be in HTML because we're using a table inside another table with indentation-->
<ol start="2">
<li>Select the tab below matching your computer's architecture, and run the command listed to download and install <code>viam-server</code>.
   We recommend the stable release for most users:

{{< tabs name="linux-computer-architectures" >}}
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

3. Create your robot's [configuration file](/installation/configuration-file/), and save the file to <file>/etc/viam.json</file>.

4. Then, start `viam-server` on your board with the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sudo systemctl start viam-server
   ```

5. To make configuration changes to your robot, edit the <file>/etc/viam.json</file> configuration file, then stop and restart `viam-server`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sudo systemctl stop viam-server
   sudo systemctl start viam-server
   ```

{{% /tab %}}
{{< /tabs >}}

## Next Steps

{{< cards >}}
  {{% card link="/installation/manage" size="small" %}}
  {{% card link="/installation/update" size="small" %}}
{{< /cards >}}
