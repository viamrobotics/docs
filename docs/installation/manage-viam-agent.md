---
title: "Manage viam-agent"
linkTitle: "Manage viam-agent"
weight: 80
no_list: true
type: docs
draft: false
images: ["/installation/thumbnails/manage.png"]
imageAlt: "Manage viam-agent"
description: "Control and manage the viam-agent systemd service."
date: "2024-08-16"
# updated: ""  # When the content was last entirely checked
---

[`viam-agent`](/configure/agent/) is installed as a `systemd` service named `viam-agent`.

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

- To restart `viam-agent`:

  {{< alert title="Alert" color="note" >}}
  When you restart `viam-agent`, the agent will restart `viam-server` as well.
  {{< /alert >}}

  ```sh {class="command-line" data-prompt="$"}
  sudo systemctl restart viam-agent
  ```

- To completely uninstall `viam-agent` and `viam-server`, run the following command:

  ```sh {class="command-line" data-prompt="$"}
  sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/uninstall.sh)"
  ```

  This command uninstalls `viam-agent`, `viam-server`, the machine configuration file (<file>/etc/viam.json</file>), and the provisioning configuration file (<file>/etc/viam-provisioning.json</file>).

## Troubleshooting

You can find assistance in the [Troubleshooting section](/appendix/troubleshooting/).
