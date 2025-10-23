---
title: "Manage viam-agent"
linkTitle: "Manage viam-agent"
weight: 110
no_list: true
type: docs
draft: false
images: ["/installation/thumbnails/manage.png"]
imageAlt: "Manage viam-agent"
description: "Control and manage the viam-agent systemd service."
date: "2024-08-16"
aliases:
  - /installation/manage-viam-agent/
# updated: ""  # When the content was last entirely checked
---

[`viam-agent`](/manage/reference/viam-agent/) is installed as a `systemd` service named `viam-agent`.

{{< tabs >}}
{{% tab name="Linux" %}}

- To restart `viam-agent`:

  {{< alert title="Alert" color="note" >}}
  When you restart `viam-agent`, the agent will restart `viam-server` as well.
  {{< /alert >}}

  {{< tabs >}}
  {{% tab name="Web UI" %}}

  1. Navigate to your machine in [Viam](https://app.viam.com).
  1. Click on the machine status indicator next to the machine name.
  1. Click on the restart arrow symbol.
     This will restart `viam-server` and `viam-agent`.

  {{% /tab %}}
  {{% tab name="Shell" %}}

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl restart viam-agent
  ```

  {{% /tab %}}
  {{< /tabs >}}

- To start `viam-agent`:

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl start viam-agent
  ```

- To stop `viam-agent`:

  {{< alert title="Alert" color="note" >}}
  When you stop `viam-agent`, the agent will stop `viam-server` as well.
  {{< /alert >}}

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl stop viam-agent
  ```

- To completely uninstall `viam-agent` and `viam-server`, run the following command:

  ```sh {class="command-line" data-prompt="$"}
  sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/uninstall.sh)"
  ```

  This command uninstalls `viam-agent`, `viam-server`, the machine cloud credentials file (<file>/etc/viam.json</file>), and the provisioning configuration file (<file>/etc/viam-provisioning.json</file>).

{{< alert title="Caution" color="caution" >}}
If you remove the machine cloud credentials file you will not be able to connect to your machine.
You can only restore this file if you have access to the machine configuration.
{{< /alert >}}

{{% /tab %}}
{{% tab name="Windows native" %}}

On Windows, you can manage `viam-agent` using the Services GUI or the command line.
You can also use the Viam web UI to restart `viam-agent`.

{{< tabs >}}
{{% tab name="Services GUI" %}}

1. Open the **Services** management console from your computer's start menu.

1. Find `viam-agent` in the list of services.

   {{<imgproc src="/manage/viam-agent-windows-services-manager.png" resize="x1100" declaredimensions=true alt="Windows Services manager with viam-agent highlighted." style="max-width:600px" class="shadow imgzoom" >}}

1. Use the **Restart Service**, **Stop Service**, and **Start Service** buttons to manage `viam-agent`.

1. To change the startup type of `viam-agent`, right-click on `viam-agent` and select **Properties**.
   Select your desired startup type from the **Startup type** dropdown menu.

   {{<imgproc src="/manage/startup-type-windows.png" resize="x1000" declaredimensions=true alt="Windows Services manager with viam-agent properties open." style="max-width:350px" class="shadow imgzoom" >}}

{{% /tab %}}
{{% tab name="Command line" %}}

1. Open a PowerShell prompt, selecting **Run as administrator**.

1. Use the following commands to manage `viam-agent`:

   - To start `viam-agent`:

     ```sh {class="command-line" data-prompt="$"}
     Start-Service viam-agent
     ```

   - To stop `viam-agent`:

     ```sh {class="command-line" data-prompt="$"}
     Stop-Service viam-agent
     ```

   - To restart `viam-agent`:

     ```sh {class="command-line" data-prompt="$"}
     Restart-Service viam-agent
     ```

   - To change the startup type of `viam-agent`, use one of the following commands:

     ```sh {class="command-line" data-prompt="$"}
     Set-Service -Name "viam-agent" -StartupType Manual
     Set-Service -Name "viam-agent" -StartupType Automatic
     ```

{{% /tab %}}
{{% tab name="Web UI" %}}

1. Navigate to your machine in [Viam](https://app.viam.com).
1. Click on the machine status indicator next to the machine name.
1. Click on the restart arrow symbol.
   This will restart `viam-server` and `viam-agent`.

{{% /tab %}}
{{< /tabs >}}

To uninstall `viam-agent`, run the following command in an administrator prompt:

```sh {class="command-line" data-prompt="$"}
sc stop viam-agent
sc delete viam-agent
Remove-Item \opt\viam -Recurse
Remove-Item C:\Windows\system32\config\systemprofile\.viam -Recurse
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find assistance in the [Troubleshooting section](/manage/troubleshoot/troubleshoot/).
