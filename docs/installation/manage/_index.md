---
title: "Manage viam-server"
linkTitle: "Manage viam-server"
weight: 30
no_list: true
type: docs
draft: false
image: "/installation/thumbnails/manage.png"
imageAlt: "Manage viam-server"
images: ["/installation/thumbnails/manage.png"]
description: "Control and troubleshoot viam-server."
aliases:
  - /installation/update/
---

Once you've [installed `viam-server`](/installation/), you can chose to run it as a system service or directly on the command line.
Running as a system service enables you to configure `viam-server` to start automatically when your system boots, and is the [default installation option](/installation/#install-viam-server) on Linux.
Running on the command line is suitable for local development.

## Run `viam-server`

Select the tab for your platform:

{{< tabs name="Managing viam-server">}}
{{% tab name="Linux"%}}

### Run as a system service

After [installation](/installation/#install-viam-server), the `viam-server` [AppImage](https://appimage.org/) binary will be located at <file>/usr/local/bin/viam-server</file>, and a `systemd` service file will be placed at <file>/etc/systemd/system/viam-server.service</file>.
By default, `viam-server` is configured to start when the machine boots.

Running `viam-server` as a system service is the recommended method for Linux.

You can use the following commands to manage `viam-server` when installed as a system service.
These commands require that you store your configuration file at <file>/etc/viam.json</file>.

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

Run the following on the command line to start `viam-server`, providing the path to your own configuration file:

```sh {class="command-line" data-prompt="$"}
sudo viam-server -config /path/to/my/config.json
```

If you followed the [Installation Guide](/installation/#install-viam-server), your robot's configuration file is available at <file>/etc/viam.json</file>.
You can provide this path in the above command, or move the configuration file to a desired location and change the path in this command accordingly.
If you don't yet have a configuration file, you can [build a new configuration file](/appendix/local-configuration-file/).

Note that on a Raspberry Pi, `viam-server` must always run as `root` (using `sudo`) in order to access the DMA subsystem for GPIO.
When running `viam-server` from your home directory on a Linux computer, you do not need to use `sudo`.

#### Stop

Press **Ctrl + C** on your keyboard within the terminal session where you are running `viam-server` to stop it.

{{% /tab %}}

{{% tab name="macOS"%}}

### Run from the command line

After [installation](/installation/#install-viam-server), `viam-server` can be run directly on the command line.

Running `viam-server` on the command line is the recommended method for macOS.

You can use the following commands to manage `viam-server` on the command line:

#### Start

Run the following on the command line to start `viam-server`, providing the path to your own configuration file:

```sh {class="command-line" data-prompt="$"}
viam-server -config /path/to/my/config.json
```

If you followed the [Installation Guide](/installation/#install-viam-server), your robot's configuration file is available in your <file>~/Downloads/</file> directory, named similarly to <file>viam-robotname-main.json</file>.
You can provide this path in the above command, or move the configuration file to a desired location and change the path in this command accordingly.
If you don't yet have a configuration file, you can use the example configuration file provided at <file>/opt/homebrew/etc/viam.json</file> or you can [build a new configuration file](/appendix/local-configuration-file/).

#### Stop

Type **Ctrl + C** on your keyboard within the terminal session where you are running `viam-server` to stop it.

<br>

### Run as a system service

Installing `viam-server` as a system service is not recommended for most use cases on macOS.
However, if you are looking to create a robot that runs on macOS and you want it to run `viam-server` automatically when your macOS system boots, then you will need to run `viam-server` as a service.

Once you have [installed `viam-server`](/installation/#install-viam-server) on your macOS computer, use the following commands to control the service.
These commands require that you store your configuration file at <file>/opt/homebrew/etc/viam.json</file>.

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

Select the tab for your platform:

{{< tabs name="Updating viam-server" >}}
{{% tab name=Linux %}}

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/), and includes a built-in self-update feature.
When you [run `viam-server`](#run-viam-server) as a service on Linux, it will check for updates automatically on launch, and update itself if a newer version is detected.

The automatic update behavior of `viam-server` should meet the needs of most deployments, but if you need to manually force an update, you can do so with the `--aix-update` flag:

```sh {class="command-line" data-prompt="$"}
sudo viam-server --aix-update
```

### Disable Service-based Updates

If you want to disable `viam-server` from automatically checking for updates each time you launch it, comment out the `ExecStartPre` line from your <file>/etc/systemd/system/viam-server.service</file> service file (by prepending with a `#` character), so that it matches the following:

```sh {class="command-line" data-prompt="$"}
# ExecStartPre=-/usr/local/bin/viam-server --aix-update
```

Then, reload the service file with the following command:

```sh {class="command-line" data-prompt="$"}
sudo systemctl daemon-reload
```

To resume automatic update checking, delete the leading `#` character once more, and run `sudo systemctl daemon-reload` again.

{{% /tab %}}
{{% tab name=macOS %}}

`viam-server` is distributed for macOS through the Homebrew package manager, which includes a built-in update feature.

To upgrade to the latest version of `viam-server` using Homebrew:

```sh {class="command-line" data-prompt="$"}
brew upgrade viam-server
```

Homebrew does not support automatic updates, so you will need to manually perform this step each time you wish to check for updates. We recommend running `brew upgrade viam-server` on a regular basis.

{{% /tab %}}
{{% /tabs %}}

## View `viam-server` logs

`viam-server` writes log messages as it starts up and runs, providing useful information when managing or troubleshooting the process.
Use the following commands to view these log messages locally on your system.

{{< alert title="Tip" color="tip" >}}
If your system is able to connect with the Viam app, you can also view logs in the **Logs** tab on [the Viam app](https://app.viam.com/).
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

To remove the configuration file, run:

```sh {class="command-line" data-prompt="$"}
sudo rm /etc/viam.json
```

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

To remove the configuration file, run:

```sh {class="command-line" data-prompt="$"}
sudo rm /etc/viam.json
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
