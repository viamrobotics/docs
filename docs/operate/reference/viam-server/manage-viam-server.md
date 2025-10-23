---
title: "Manage viam-server"
linkTitle: "Manage viam-server"
weight: 120
no_list: true
type: docs
draft: false
images: ["/installation/thumbnails/manage.png"]
imageAlt: "Manage viam-server"
description: "If you have manually installed viam-server, you can chose to run it as a system service or on the command line."
date: "2024-08-16"
# updated: ""  # When the content was last entirely checked
aliases:
  - /installation/update/
  - /installation/manage-viam-server/
  - /get-started/installation/manage-viam-server/
---

If you have manually [installed `viam-server`](/operate/install/setup/), you can chose to run it as a system service or directly on the command line.
Running as a system service enables you to configure `viam-server` to start automatically when your system boots, and is the [default installation option](/operate/install/setup/#installation-methods-viam-agent-versus-manual) on Linux.
Running on the command line is suitable for local development.

{{< alert title="Note" color="note" >}}
If you have installed `viam-agent`, see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/) instead.
{{< /alert >}}

## Run `viam-server`

Select the tab for your platform:

{{< tabs name="Managing viam-server">}}
{{% tab name="Linux"%}}

### Run as a system service

After [installation](/operate/install/setup/), the `viam-server` [AppImage](https://appimage.org/) binary will be located at <file>/usr/local/bin/viam-server</file>, and a `systemd` service file will be placed at <file>/etc/systemd/system/viam-server.service</file>.
By default, `viam-server` is configured to start when the machine boots.

Running `viam-server` as a system service is the recommended method for Linux.

You can use the following commands to manage `viam-server` when installed as a system service.
These commands require that you store your machine cloud credentials file at <file>/etc/viam.json</file>.

#### Start

```sh {class="command-line" data-prompt="$"}
sudo systemctl start viam-server
```

#### Stop

```sh {class="command-line" data-prompt="$"}
sudo systemctl stop viam-server
```

#### Restart

```sh {class="command-line" data-prompt="$"}
sudo systemctl restart viam-server
```

#### Enable (start automatically with system boot, default)

```sh {class="command-line" data-prompt="$"}
sudo systemctl enable viam-server
```

#### Disable (do not start automatically with system boot)

```sh {class="command-line" data-prompt="$"}
sudo systemctl disable viam-server
```

<br>

### Run from the command line

When running `viam-server` on the command line, you can use the following commands to manage the process.
If `viam-server` is already running as a system service, be sure to stop the service first before using these commands.

#### Start

Run the following on the command line to start `viam-server`, providing the path to your configuration file:

```sh {class="command-line" data-prompt="$"}
sudo viam-server -config /path/to/my/config.json
```

If you followed the [Installation Guide](/operate/install/setup/), your machine's cloud credentials file is available at <file>/etc/viam.json</file>.
You can provide this path in the above command, or move the configuration file to a desired location and change the path in this command accordingly.

Note that on a Raspberry Pi, `viam-server` must always run as `root` (using `sudo`) in order to access the DMA subsystem for GPIO.
When running `viam-server` from your home directory on a Linux computer, you do not need to use `sudo`.

#### Stop

Press **Ctrl + C** on your keyboard within the terminal session where you are running `viam-server` to stop it.

{{% /tab %}}

{{% tab name="macOS"%}}

### Run from the command line

After [installation](/operate/install/setup/), `viam-server` can be run directly on the command line.

Running `viam-server` on the command line is the recommended method for macOS.

You can use the following commands to manage `viam-server` on the command line:

#### Start

Run the following on the command line to start `viam-server`, providing the path to your own configuration file:

```sh {class="command-line" data-prompt="$"}
viam-server -config /path/to/my/config.json
```

If you followed the [Installation Guide](/operate/install/setup/), your machine's configuration file is available in your <file>~/Downloads/</file> directory, named similarly to <file>viam-machinename-main.json</file>.
You can provide this path in the above command, or move the configuration file to a desired location and change the path in this command accordingly.

#### Stop

Type **Ctrl + C** on your keyboard within the terminal session where you are running `viam-server` to stop it.

<br>

### Run as a system service

Installing `viam-server` as a system service is not recommended for most use cases on macOS.
However, if you are looking to create a machine that runs on macOS and you want it to run `viam-server` automatically when your macOS system boots, then you will need to run `viam-server` as a service.

Once you have [installed `viam-server`](/operate/install/setup/) on your macOS computer, use the following commands to control the service.
These commands require that you store your machine cloud credentials file at <file>/opt/homebrew/etc/viam.json</file>.

#### Start

```sh {class="command-line" data-prompt="$"}
brew services start viam-server
```

#### Stop

```sh {class="command-line" data-prompt="$"}
brew services stop viam-server
```

#### Restart

```sh {class="command-line" data-prompt="$"}
brew services restart viam-server
```

{{% /tab %}}
{{< /tabs >}}

## Update `viam-server`

The steps to update `viam-server` differ depending on your installation method.
To determine your installation method, check if the `viam-agent` process is running.
Run the following command:

```sh {class="command-line" data-prompt="$" data-output="2"}
ps aux | grep viam-agent
root      566431  0.5  0.2 1247148 20336 ?       Ssl  11:24   0:00 /opt/viam/bin/viam-agent --config /etc/viam.json
```

If the output includes a process named `viam-agent`, you used `viam-agent` to install `viam-server`.
Follow the steps to use `viam-agent` to update `viam-server`.

If the output does not include a process named `viam-agent`, you did not use `viam-agent`.
Follow the manual steps to update the standalone version.

{{< tabs >}}
{{% tab name="Installed with viam-agent" %}}

By default, `viam-agent` automatically upgrades to the latest stable version of `viam-server`.
You can change this behavior in the [`version_control` settings of your machine](/manage/reference/viam-agent/#version_control-version-management-for-viam-agent-and-viam-server).
For example, the following `version_control` configuration will always update to the latest stable release of `viam-agent` and the latest development release of `viam-server`:

```json {class="line-numbers linkable-line-numbers" data-line=""}
{
  "agent": {
    "version_control": {
      "agent": "stable",
      "viam-server": "dev"
    }
  },
  "components": [ ... ]
}
```

{{% /tab %}}
{{% tab name="Manual" %}}

To update to the newest RDK version, you need to update your `viam-server`.
Select the tab for your platform:

{{< tabs name="Updating viam-server" >}}
{{% tab name=Linux %}}

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/), and includes a built-in self-update feature.
When you [run `viam-server`](#run-viam-server) as a service on Linux, it will check for updates automatically on launch, and update itself if a newer version is detected.

The automatic update behavior of `viam-server` should meet the needs of most deployments, but if you need to manually force an update, you can do so with the `--aix-update` flag:

```sh {class="command-line" data-prompt="$"}
sudo viam-server --aix-update
```

{{% /tab %}}
{{% tab name=macOS %}}

`viam-server` is distributed for macOS through the Homebrew package manager, which includes a built-in update feature.

To upgrade to the latest version of `viam-server` using Homebrew:

```sh {class="command-line" data-prompt="$"}
brew upgrade viam-server
```

Homebrew does not support automatic updates, so you will need to manually perform this step each time you wish to check for updates.
We recommend running `brew upgrade viam-server` on a regular basis.
{{% /tab %}}

{{< /tabs >}}
{{% /tab %}}
{{< /tabs >}}

### Disable automatic updates

{{< tabs >}}
{{% tab name="Installed with viam-agent" %}}

To disable automatic updates, configure the [`version_control` settings of your machine](/manage/reference/viam-agent/#version_control-version-management-for-viam-agent-and-viam-server) to a specific version number.
For example, the following `version_control` configuration pins `viam-server` to version `0.52.1`, preventing `viam-server` from updating to a more recent version:

```json {class="line-numbers linkable-line-numbers" data-line=""}
{
  "agent": {
    "version_control": {
      "agent": "stable",
      "viam-server": "0.52.1"
    }
  },
  "components": [ ... ]
}
```

If you are changing to a different version of `viam-server` and `viam-agent`, `viam-agent` restarts itself automatically.
This also restarts `viam-server`.
{{% /tab %}}
{{% tab name="Manual" %}}

`viam-server` automatically checks for updates.
On Linux, you can disable automatic `viam-server` updates.
To disable the updates, open <file>/etc/systemd/system/viam-server.service</file> and comment out the line that starts with `ExecStartPre`.
Add a `#` character at the beginning of the line so that it matches the following:

```sh
# ExecStartPre=-/usr/local/bin/viam-server --aix-update
```

Then, reload the service file with the following command:

```sh {class="command-line" data-prompt="$"}
sudo systemctl daemon-reload
```

To resume automatic update checking, delete the leading `#` character in <file>/etc/systemd/system/viam-server.service</file>, then run `sudo systemctl daemon-reload` again.

{{% /tab %}}
{{< /tabs >}}

## View `viam-server` logs

`viam-server` writes log messages as it starts up and runs, providing useful information when managing or troubleshooting the process.
Use the following commands to view these log messages locally on your system.

{{< alert title="Tip" color="tip" >}}
If your system is able to connect to Viam, you can also view logs in the **LOGS** tab.
{{< /alert >}}

Select the tab below for your platform:

{{< tabs name="View logs">}}
{{% tab name="Linux"%}}

### As a system service

If you are running `viam-server` as a system service, run the following command to view log messages:

```sh {class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-server
```

Use the arrow keys to page vertically or horizontally through the log messages.

You can also "tail" the logs, viewing new messages as they come in with:

```sh {class="command-line" data-prompt="$"}
sudo journalctl -f --unit=viam-server
```

Use the q key to stop following the logs.

You can also view log messages specific to `viam-server` in the `syslog` with the following command:

```sh {class="command-line" data-prompt="$"}
grep viam-server /var/log/syslog
```

### From the command line

If you are running `viam-server` on the command line, log messages are written to standard out (`stdout`) in the same terminal session you started `viam-server` in.

You can also view log messages specific to `viam-server` in the `syslog` with the following command:

```sh {class="command-line" data-prompt="$"}
grep viam-server /var/log/syslog
```

{{% /tab %}}

{{% tab name="macOS" %}}

When running `viam-server` on macOS, log messages are written to standard out (`stdout`) in the same terminal session you started `viam-server` in.

You can also access the local `viam-server` log file using the following command:

```sh {class="command-line" data-prompt="$"}
cat $(brew --prefix)/var/log/viam.log
```

{{% /tab %}}
{{< /tabs >}}

## Uninstall `viam-server`

{{< tabs name="Uninstall viam-server">}}
{{% tab name="Linux"%}}

Remove the system installed service with the following three commands:

```sh {class="command-line" data-prompt="$"}
sudo systemctl disable --now viam-server
sudo rm /etc/systemd/system/viam-server.service
sudo systemctl daemon-reload
```

To remove the machine cloud credentials file, run:

```sh {class="command-line" data-prompt="$"}
sudo rm /etc/viam.json
```

{{< alert title="Caution" color="caution" >}}
If you remove the machine cloud credentials file you will not be able to connect to your machine.
You can only restore this file if you have access to the machine configuration.
{{< /alert >}}

To remove various Viam caches and logs for the root (service) user, run:

```sh {class="command-line" data-prompt="$"}
sudo rm -r /root/.viam/
```

If you ever run `viam-server` directly, to remove various Viam caches and logs for your own user run:

```sh {class="command-line" data-prompt="$"}
rm -r ~/.viam/
```

To remove the `viam-server` binary itself, run:

```sh {class="command-line" data-prompt="$"}
sudo rm /usr/local/bin/viam-server
```

{{% /tab %}}
{{% tab name="macOS" %}}

Uninstall `viam-server` with the following command:

```sh {class="command-line" data-prompt="$"}
brew uninstall viam-server
```

To remove various Viam caches and logs, run:

```sh {class="command-line" data-prompt="$"}
rm -r ~/.viam/
```

To remove the machine cloud credentials file, run:

```sh {class="command-line" data-prompt="$"}
rm ~/Downloads/viam-<your-part-name>.json
```

For example, `rm ~/Downloads/viam-mymachine1-main.json`.

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/manage/troubleshoot/troubleshoot/).
