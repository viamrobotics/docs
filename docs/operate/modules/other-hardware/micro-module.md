---
title: "Create modules for ESP32 microcontrollers"
linkTitle: "Modules for ESP32"
type: "docs"
weight: 60
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
You'll write it in Rust and then embed it in the firmware you flash onto your device.

## Create a new module for ESP32

To create a new module compatible with the Micro-RDK, follow these steps:

1. Set up your development environment following the [development setup instructions](/operate/install/setup-micro/#set-up-your-development-environment).

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

1. Develop the module by defining structs which implement the necessary traits.
   The required traits are determined by the API you chose to implement.

   For example, to implement the sensor API, you need to implement `Readings`, `SensorT<f64>` and `Status` traits.

   {{< expand "Example implementation" >}}
   The following example <file>src/lib.rs</file> file implements the sensor API to return random numbers:

   ```rust { class="line-numbers linkable-line-numbers" }
    use std::sync::{Arc, Mutex};
    use std::collections::HashMap;
    use micro_rdk::DoCommand;
    use micro_rdk::common::config::ConfigType;
    use micro_rdk::common::registry::{ComponentRegistry, RegistryError, Dependency};
    use micro_rdk::common::sensor::{
        Sensor, SensorType, Readings, SensorError, SensorT, SensorResult,
        GenericReadingsResult, TypedReadingsResult
    };
    use micro_rdk::common::status::{Status, StatusError};

    pub fn register_models(registry: &mut ComponentRegistry) -> Result<(), RegistryError> {
        registry.register_sensor("my_sensor", &MySensor::from_config)
    }

    #[derive(DoCommand)]
    pub struct MySensor {}

    impl MySensor {
        pub fn from_config(_cfg: ConfigType, _deps: Vec<Dependency>) -> Result<SensorType, SensorError> {
            Ok(Arc::new(Mutex::new(MySensor {})))
        }
    }

    // Mark this type as a sensor
    impl Sensor for MySensor {}

    // Implementation for getting readings
    impl SensorT<f64> for MySensor {
        fn get_readings(&self) -> Result<TypedReadingsResult<f64>, SensorError> {
            use rand::Rng;
            let mut rng = rand::thread_rng();
            let mut readings = HashMap::new();
            readings.insert("random_value".to_string(), rng.gen());
            Ok(readings)
        }
    }

    // Required to convert typed readings to generic readings
    impl Readings for MySensor {
        fn get_generic_readings(&mut self) -> Result<GenericReadingsResult, SensorError> {
            Ok(self
                .get_readings()?
                .into_iter()
                .map(|v| (v.0, SensorResult::<f64> { value: v.1 }.into()))
                .collect())
        }
    }

    // Basic status implementation
    impl Status for MySensor {
        fn get_status(&self) -> Result<Option<micro_rdk::google::protobuf::Struct>, StatusError> {
            Ok(Some(micro_rdk::google::protobuf::Struct {
                fields: HashMap::new(),
            }))
        }
    }

   ```

   {{< /expand >}}

   For more examples, see the [example module implementation walkthrough](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md).

## Test your module

To use your module with your ESP32, follow the [Build and flash custom firmware](/operate/install/setup-micro/#build-and-flash-custom-firmware) workflow in a separate directory.
