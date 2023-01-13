---
title: "Manage viam-server"
linkTitle: "Manage"
weight: 30
simple_list: false
type: docs
draft: false
---

Sometimes you may want to manually start, stop or restart viam-server, for instance, when troubleshooting.
You can use the following commands to do so:

{{< tabs name="Starting and stopping viam-server">}}
{{% tab name="Linux"%}}

After setting up the system service per the [Linux install instructions](/installation/install/linux-install/), the AppImage binary will be located at <file>/usr/local/bin/viam-server</file>, and a systemd service file will be placed at <file>/etc/systemd/system/viam-server.service</file>.

To control the systemd service (viam-server) use the following commands:

Start:

```bash
sudo systemctl start viam-server
```

Stop:

```bash
sudo systemctl stop viam-server
```

Restart:

```bash
sudo systemctl restart viam-server
```

Enable (start automatically after boot):

```bash
sudo systemctl enable viam-server
```

Disable:

```bash
sudo systemctl disable viam-server
```

<br>

If you want to run the binary directly, be sure to stop the service first, then run `sudo /usr/local/bin/viam-server path/to/my/config.json`.
Note that on a Raspberry Pi, viam-server must always run as root in order to access the DMA subsystem for GPIO.

{{% /tab %}}

{{% tab name="macOS"%}}

### From the command line (recommended method on macOS)

You can run viam-server by running the following command, always making sure to replace `<YOUR_ROBOT_NAME>` with the name of your robot from the Viam app.

```bash
viam-server -config ~/Downloads/viam-<YOUR_ROBOT_NAME>-main.json
```

You can also store the config file in a different folder (other than Downloads)--just make sure to run the above command with the correct filepath if you do so.

Hit **Ctrl + C** on your keyboard to stop running viam-server.

### As a system service

Installing `viam-server` as a system service is not recommended for most use cases on macOS.
However, if you are looking to create a robot that runs on macOS and you want it to run `viam-server` every time your OS boots up, then you will need to run `viam-server` as a service.
Once you have `viam-server` downloaded locally from Homebrew, you will need to use the following commands to control the service:

Start:

```bash
brew services start viam-server
```

Stop:

```bash
brew services stop viam-server
```

Restart:

```bash
brew services restart viam-server
```

{{% /tab %}}
{{< /tabs >}}
