---
title: "Manage viam-server"
linkTitle: "Manage viam-server"
weight: 30
no_list: true
type: docs
draft: false
icon: "/installation/img/thumbnails/manage.png"
images: ["/installation/img/thumbnails/manage.png"]
description: "Control and troubleshoot viam-server."
---

How you control `viam-server` will depend on whether or not you installed it as a system service.
Find information for each situation in the tabs below.

{{< tabs name="Starting and stopping viam-server">}}
{{% tab name="Linux"%}}

### As a system service

After setting up the system service per the [Linux install instructions](/installation/#install-viam-server), the AppImage binary will be located at <file>/usr/local/bin/viam-server</file>, and a systemd service file will be placed at <file>/etc/systemd/system/viam-server.service</file>.

By default, the `viam-server` is configured to start when the machine boots.

Sometimes you may want to manually start, stop or restart the `viam-server` systemd service, for instance, when troubleshooting.
You can use the following commands to do so:

Start:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl start viam-server
```

Stop:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl stop viam-server
```

Restart:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl restart viam-server
```

Enable (start automatically after boot):

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl enable viam-server
```

Disable (do not start automatically after boot):

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl disable viam-server
```

<br>

### From the command line

If you want to run the binary directly, be sure to stop the service first, then run `sudo /usr/local/bin/viam-server path/to/my/config.json`.
Note that on a Raspberry Pi, `viam-server` must always run as root in order to access the DMA subsystem for GPIO.

{{% /tab %}}

{{% tab name="macOS"%}}

### Run `viam-server` from the command line

(Recommended method on macOS)

You can run `viam-server` by running the following command, always making sure to replace `<YOUR_ROBOT_NAME>` with the name of your robot from the Viam app.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam-server -config ~/Downloads/viam-<YOUR_ROBOT_NAME>-main.json
```

You can also store the config file in a different folder (other than Downloads)--just make sure to run the above command with the correct filepath if you do so.

Hit **Ctrl + C** on your keyboard to stop running `viam-server`.

<br>

### Run as a system service

Installing `viam-server` as a system service is not recommended for most use cases on macOS.
However, if you are looking to create a robot that runs on macOS and you want it to run `viam-server` every time your OS boots up, then you will need to run `viam-server` as a service.
Once you have `viam-server` downloaded locally from Homebrew, you will need to use the following commands to control the service:

Start:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew services start viam-server
```

Stop:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew services stop viam-server
```

Restart:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew services restart viam-server
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< tabs name="Troubleshooting">}}
{{% tab name="Linux" %}}

### View Logs

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-server
```

If the robot is able to connect with the Viam app, logs can also be viewed in the **Logs** tab on the [Viam app](https://app.viam.com/).

### SquashFS Errors

Look like this...

```sh {id="terminal-prompt" class="command-line" data-prompt="$" data-output="1-10"}
Feb 10 13:11:26 hydro3-pi viam-server[933]: Something went wrong trying to read the squashfs image.
Feb 10 13:11:26 hydro3-pi viam-server[933]: open dir error: No such file or directory
```

The update process may have been interrupted and left a corrupt file.
Simply redownload the new file as instructed above.

### FUSE Errors

FUSE (Filesystem-in-Userspace), is included in almost all modern Linux distributions by default.
(The one real exception is that it doesn’t work (by default) due to security restrictions within Docker containers.)
For more information on troubleshooting FUSE-related issues (including Docker workarounds) see here: [I get some errors related to something called "FUSE" - AppImage documentation](https://docs.appimage.org/user-guide/troubleshooting/fuse.html).

{{% /tab %}}

{{% tab name="macOS" %}}

### View `viam-server` Logs

If you have already successfully connected `viam-server` to the Viam app, you can find all the `viam-server` logs on the **Logs** tab of the [Viam app](https://app.viam.com/).

You can also read `viam-server`'s log files locally.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cat $(brew --prefix)/var/log/viam.log
```

{{% /tab %}}
{{< /tabs >}}
