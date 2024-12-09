---
title: "Create a sensor module with Python"
linkTitle: "Create a sensor module with Python"
type: "docs"
weight: 26
images: ["/icons/components/sensor.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Add a new model of sensor component by writing a module in Python."
languages: ["python"]
viamresources: ["sensor"]
platformarea: ["registry"]
level: "Beginner"
date: "2024-08-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

A sensor is anything that collects data.

A sensor could be something we typically think of as a sensor, like a temperature and humidity sensor, or it could be a "virtual," non-hardware sensor like a service that gets stock market data.

Although there are various [models available in Viam](/components/sensor/#configuration), you may have a different sort of sensor you'd like to use.

Making a module to support your sensor will allow you to use it with Viam's data capture and sync tools, as well as using the sensor API (using any of the different programming language [SDKs](/sdks/)) to get readings from it.

{{% alert title="In this page" color="info" %}}

1. [Start with a test script](#start-with-a-test-script)
1. [Generate template module code](#generate-template-module-code)
1. [Implement the sensor API](#implement-the-sensor-api)
1. [Make the module executable](#make-the-module-executable)
1. [Test your module locally](#test-your-module-locally)
1. [Upload your module](#upload-your-module-to-the-registry)

{{% /alert %}}

## Prerequisites

{{< expand "Install the Viam CLI and authenticate" >}}
Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

{{% expand "Install viam-server on your computer and connect to the Viam app" %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

## Start with a test script

Start by getting a test script working so you can check that your sensor code itself works before packaging it into a module.

Since this how-to uses Python, you need a Python test script so that you can more easily wrap it in a Python-based module.
You'll still be able to use any of Viam's SDKs to get readings from machines that use the module.

What you use as a test script depends completely on your sensor hardware (or software)—just find or write some script that gets readings from the sensor and prints them out.

{{< expand "An example of getting air quality data from an online source (Open-Meteo)" >}}
This example uses the Open-Meto API to get air quality data from [open-meteo.com](https://open-meteo.com/en/docs/air-quality-api#current=pm10,pm2_5&hourly=).
The following test script is from the linked code sample generator.

```python {class="line-numbers linkable-line-numbers"}
# test-script.py
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Set up the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important
# to assign them correctly below
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
  "latitude": 44.0582,
  "longitude": -121.3153,
  "current": ["pm10", "pm2_5"],
  "timezone": "America/Los_Angeles"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location.
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_pm10 = current.Variables(0).Value()
current_pm2_5 = current.Variables(1).Value()

print(f"Current time {current.Time()}")
print(f"Current pm10 {current_pm10}")
print(f"Current pm2_5 {current_pm2_5}")
```

{{< /expand >}}

{{< expand "An example of getting PM2.5 and PM10 readings over serial from sensor hardware" >}}
This script is based on the [pms7003 module](https://app.viam.com/module/joyce/pms7003).

```python {class="line-numbers linkable-line-numbers"}
# my-sensor-test.py
from serial import Serial
import time


def main():

    port = Serial('/dev/ttyAMA0', baudrate=9600)

    def parse_data(data):

        if len(data) < 2:
            return {}
        if data[0] == 0x42 and data[1] == 0x4d:
            pm2_5_atm = (data[12] << 8) + data[13]
            pm10_atm = (data[14] << 8) + data[15]
            print(f'PM2.5 (atmospheric): {pm2_5_atm} µg/m3')
            print(f'PM10 (atmospheric): {pm10_atm} µg/m3')

            # Return a dictionary of the readings
            return {
                "pm2_5_atm": pm2_5_atm,
                "pm10_atm": pm10_atm,
            }

        else:
            print('Data does not start with the expected start bytes.')
            return {}

    while port.in_waiting == 0:
        time.sleep(0.01)  # wait for 10 ms

    data = port.read(port.in_waiting)
    print(parse_data(data))


if __name__ == "__main__":
    main()
```

{{< /expand >}}

Run your test script from your terminal and make sure you are able to get readings from the sensor before proceeding.

## Generate template module code

There are a few standardized files that must be part of any module.
You can create these automatically using the Viam module generator:

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate
   ```

2. Follow the prompts, naming your module and selecting from the options.

<!--prettier-ignore-->
| Prompt | Description |
| -------| ----------- |
| Module name | The module name (also called repo name or family name) is generally the name of the GitHub repo where you will put your module code. Name it something related to what your module does. For example, `weather`. |
| Language | Choose Python to follow this tutorial. |
| Visibility | Choose `Private` to share only with your organization, or `Public` to share publicly with all organizations. |
| Namespace/Organization ID | In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page. Find the **Public namespace** and copy that string. In the example snippets below, the namespace is `jessamy`. |
| Resource to add to the module (API) | Choose `Sensor Component` for this tutorial. |
| Model name | Name your sensor based on what it supports, for example, if it supports a model of ultrasonic sensor called “XYZ Sensor 1234” you could call your model `XYZ_1234` or similar. |
| Enable cloud build | You can select `No` for this tutorial because you'll build the module yourself before uploading it. If you select `Yes`, the module will build from your specified GitHub repo using GitHub actions. |
| Register module | `Yes` unless you are creating a local-only module for testing purposes and do not intend to upload it. |

The generator will generate a folder containing stub files for your modular sensor component.
In the next section, you'll customize some of the generated files to support your sensor.

## Implement the sensor API

Other than the inherited methods, the [sensor API](/components/sensor/#api) only contains one method, `GetReadings()`.
You need to implement this method so your sensor supports the sensor API:

{{< table >}}
{{% tablestep %}}
**1. Edit configuration code**

In the generated <file>/YOUR_MODULE_NAME/src/</file> directory, open the </file>main.py</file> file.

Edit the config attributes to fit your sensor.
For example, if your sensor requires two pins, edit the validate function to check that they are configured.
Edit the reconfigure function to get the configured values of each parameter from the configuration.
If you want to be able to configure something else, for example the location to get online data from, you can add attributes for that (see example code in the expander below).
If your sensor doesn't require any configuration, leave the `validate` and `reconfigure` functions as they are; they're needed for the module to function even if they don't actually validate the input or reconfigure the resource.

{{% /tablestep %}}
{{% tablestep %}}
**2. Define `get_readings`**

In the `get_readings` function definition, replace `raise NotImplementedError()` by pasting your test script.
Edit the script to return a dictionary of readings instead of printing them.
Be sure to add any required imports to the top of the file.

{{% /tablestep %}}
{{% tablestep %}}
**3. (Optional) Add logging**

[Add logging messages](/how-tos/create-module/#optional-configure-logging) as desired.

{{% /tablestep %}}
{{< /table >}}
<br>

{{< expand "Example code for Open-Meteo data sensor" >}}

The following code puts the functionality of the [example test script](#start-with-a-test-script) into the `get_readings` function definition.

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from typing import Any, ClassVar, Final, Mapping, Optional, Sequence

from typing_extensions import Self
from viam.components.sensor import *
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, struct_to_dict

import openmeteo_requests
import requests_cache
from retry_requests import retry


class Meteopm(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("jessamy", "weather"), "meteo_PM")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.
        """
        fields = config.attributes.fields
        # Check that configured fields are floats
        if "latitude" in fields:
            if not fields["latitude"].HasField("number_value"):
                raise Exception("Latitude must be a float.")

        if "longitude" in fields:
            if not fields["longitude"].HasField("number_value"):
                raise Exception("Longitude must be a float.")
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.
        """
        attrs = struct_to_dict(config.attributes)

        self.latitude = float(attrs.get("latitude", 45))
        self.logger.debug("Using latitude: " + str(self.latitude))

        self.longitude = float(attrs.get("longitude", -121))
        self.logger.debug("Using longitude: " + str(self.longitude))
        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        # Set up the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession(
          '.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # The order of variables in hourly or daily is
        # important to assign them correctly below
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["pm10", "pm2_5"],
            "timezone": "America/Los_Angeles"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process location
        response = responses[0]

        # Current values. The order of variables needs
        # to be the same as requested.
        current = response.Current()
        current_pm10 = current.Variables(0).Value()
        current_pm2_5 = current.Variables(1).Value()

        self.logger.info(current_pm2_5)

        # Return a dictionary of the readings
        return {
            "pm2_5": current_pm2_5,
            "pm10": current_pm10
        }

if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
```

{{< /expand >}}

For more examples, see other sensor modules in the [Viam Registry](https://app.viam.com/registry).
Most modules have their implementation code linked on their module page, so you can see how they work.

## Edit requirements.txt

Update the generated <file>requirements.txt</file> file to include any packages that must be installed for the module to run.
Depending on your use case, you may not need to add anything here beyond `viam-sdk` which is auto-populated.

## Set up a virtual environment

Create a virtual Python environment with the necessary packages by running the setup file from within the <file>hello-world</file> directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
```

This environment is where the local module will run.
`viam-server` does not need to run inside this environment.

## Test your module locally

{{% expand "Prerequisite: A running machine connected to the Viam app." %}}

You can write a module without a machine, but to test your module you'll need a machine.
Make sure to physically connect your sensor to your machine's computer to prepare your machine for testing.

{{% snippet "setup.md" %}}

{{% /expand%}}

It's a good idea to test your module locally before uploading it to the [Viam Registry](https://app.viam.com/registry):

{{< table >}}
{{% tablestep link="/how-tos/create-module/#test-your-module-locally" %}}
**1. Configure your local module on a machine**

On your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), click the **+** (create) icon in the left-hand menu.
Select **Local module**, then **Local module**.

Type in the _absolute_ path on your machine's filesystem to your module's executable file, for example <file>/Users/jessamy/my-sensor-module/run.sh</file>.
Click **Create**.

{{% /tablestep %}}
{{% tablestep link="/how-tos/create-module/#test-your-module-locally" %}}
**2. Configure the model provided by your module**

Click the **+** button again, this time selecting **Local module** and then **Local component**.

For **Type** choose **sensor**.

Select or enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}} you specified in the [Name your model step](/how-tos/sensor-module/#generate-template-module-code), for example `jessamy:weather:meteo-PM`.

Click **Create**.

{{<imgproc src="/how-tos/sensor-module-config.png" resize="600x" style="width: 300px" alt="Configuring a local model after the local module is configured">}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Make sure readings are being returned**

Click the **TEST** bar at the bottom of your sensor configuration, and check whether readings are being returned there.

![The control tab with pm10 and pm2_5 readings displayed.](/how-tos/sensor-test.png)

If it works, you're almost ready to share your module by uploading it to the registry.
If not, you have some debugging to do.
For help, don't hesitate to reach out on the [Community Discord](https://discord.gg/viam).

{{% /tablestep %}}
{{< /table >}}

## Create a README

It's quite helpful to create a README to document what your module does and how to use it, especially if you plan to share your module with others.

{{< expand "Example sensor module README" >}}

````md
# `meteo_PM` modular component

This module implements the [Viam sensor API](https://github.com/rdk/sensor-api) in a jessamy:weather:meteo_PM model.
With this model, you can gather [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api) PM2.5 and PM10 air quality data from anywhere in the world, at the coordinates you specify.

## Build and Run

To use this module, add it from the machines **CONFIGURE** tab and select the `rdk:sensor:jessamy:weather:meteo_PM` model from the [`jessamy:weather:meteo_PM` module](https://app.viam.com/module/rdk/jessamy:weather:_PM).

## Configure your `meteo_PM` sensor

Navigate to the **CONFIGURE** tab of your robot’s page in the [Viam app](https://app.viam.com/).
Add a component.
Select the `sensor` type, then select the `jessamy:weather:meteo_PM` model.
Enter a name for your sensor and click **Create**.

On the new component panel, copy and paste the following attribute template into your sensor’s **Attributes** box:

```json
{
  "latitude": <float>,
  "longitude": <float>
}
```

### Attributes

The following attributes are available for `rdk:sensor:jessamy:weather:meteo_PM` sensors:

| Name        | Type  | Inclusion | Description                            |
| ----------- | ----- | --------- | -------------------------------------- |
| `latitude`  | float | Optional  | Latitude at which to get the readings  |
| `longitude` | float | Optional  | Longitude at which to get the readings |

### Example Configuration

```json
{
  "latitude": -40.6,
  "longitude": 93.125
}
```
````

{{< /expand >}}

## Upload your module to the registry

To share your module with others in your organization or with the world, [follow these instructions to upload your module to the modular resource registry](/how-tos/upload-module/).

Once you've uploaded your module, you can [deploy it on your machines](/how-tos/create-module/#deploy-your-module-to-more-machines) by adding it just as you'd add any component instead of as a local module.

## Next steps

{{< cards >}}
{{% card link="/how-tos/manage-modules/" %}}
{{< /cards >}}
