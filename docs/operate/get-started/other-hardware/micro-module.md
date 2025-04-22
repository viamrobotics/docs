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

1. Generate a new module skeleton from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module):

   ```sh { class="command-line" data-prompt="$"}
   cargo generate --git https://github.com/viamrobotics/micro-rdk.git
   ```

   Select `templates/module` when prompted, give the module a name of your choice, and answer any additional prompts.

   The CLI automatically initializes a git repository in the generated module directory.

1. Navigate into the generated module directory:

   ```sh { class="command-line" data-prompt="$"}
   cd <path-to/your-module-directory>
   ```

1. Develop the module by defining structs which implement the necessary traits and adding tests and registration hooks for them, per the [example module implementation walkthrough](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md).
   The traits you need to implement are determined by the API you chose to implement.
   For example, to create a random number generator that implements the sensor API, you need to implement the `Sensor` trait by adding the following code to <file>src/lib.rs</file>:

   ```rust { class="line-numbers" data-start="24"}
    impl Sensor for MySensor {}

    impl Readings for MySensor {
        fn read(&self) -> Result<f64, SensorError> {
            use rand::Rng;
            let mut rng = rand::thread_rng();
            Ok(rng.gen())
        }
    }
   ```

1. To use the module, follow the [Build and flash custom firmware](/operate/get-started/other-hardware/micro-module/#build-custom-firmware) workflow in a different directory from your module.
   Be sure to register your module in the `dependencies` section of the project's `Cargo.toml` file, for example:

   ```toml
   [dependencies]
   ...
   my_module = { path = "../my_module" }
   ```

For further details on Micro-RDK development, including credentials management and developer productivity suggestions, please see the [development technical notes page on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md).
