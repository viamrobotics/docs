---
title: "Create modules for ESP32 microcontrollers"
linkTitle: "Modules for ESP32"
type: "docs"
weight: 29
images: ["/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
tags: ["modular resources", "components", "services", "registry"]
description: "Create your own modules for use with an Espressif ESP32 microcontroller."
languages: ["rust"]
date: "2024-12-11"
# updated: ""  # When the content was last entirely checked
aliases:
  - /installation/prepare/microcontrollers/development-setup/
  - /get-started/installation/prepare/microcontrollers/development-setup/
  - /get-started/installation/microcontrollers/development-setup/
  - /get-started/installation/viam-micro-server-dev/
  - /installation/viam-micro-server-dev/
---

If no existing modules support your hardware or software, you can create your own.
To create a new module compatible with the Micro-RDK, follow these steps.

1. If you have not previously developed a module for the Micro-RDK, please review the [module template README](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) and the [example module implementation walkthrough](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md) before continuing.

1. Generate a new module skeleton from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module):

   ```sh { class="command-line" data-prompt="$"}
   cargo generate --git https://github.com/viamrobotics/micro-rdk.git
   ```

   Select `templates/module` when prompted, give the module a name of your choice, and answer any additional prompts.

1. Change directories into the generated tree:

   ```sh { class="command-line" data-prompt="$"}
   cd <your-path-to/your-module-directory>
   ```

1. If you wish to use version control for the module, this is the best time to initialize a git repository and commit all the generated files.
   There are no secrets in a newly generated module repository:

   ```sh { class="command-line" data-prompt="$"}
   git add .
   git commit -m "initial commit"
   ```

1. Develop the module by defining `structs` which implement the necessary `traits` and adding tests and registration hooks for them, per the walkthrough.

1. To use the module, follow the [Build custom firmware](/operate/get-started/other-hardware/micro-module/#build-custom-firmware) workflow in a different directory, and register your module in the `dependencies` section of the project's `Cargo.toml` file, then build and flash the project.

For further details on Micro-RDK development, including credentials management and developer productivity suggestions, please see the [development technical notes page on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md).
