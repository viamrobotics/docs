---
title: "Create a sensor module with Python"
linkTitle: "Create a sensor module with Python"
type: "docs"
weight: 26
images: ["/icons/components/sensor.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Add support for a new model of sensor by creating a module written in Python."
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

{{< table >}}
{{% tablestep %}}
**1. Install the module generator**

Install the [module generator](https://github.com/viam-labs/generator-viam-module/tree/main):

1. Install node (version 16 or later) and npm if you don't already have them:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
   nvm install 16
   nvm use 16
   ```

1. Install Yeoman:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   npm install -g yo
   ```

1. Now install the module generator:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   npm install -g generator-viam-module
   ```

{{% /tablestep %}}
{{% tablestep %}}
**2. Run the generator**

Go to the directory where you want to create your module and run the generator:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
yo viam-module
```

{{% /tablestep %}}
{{% tablestep %}}
**3. Name your model**

When prompted for a model triplet, use `<your organization public namespace>:<repo name>:<what you want to call your sensor model>`.
For example, `jessamy:weather:meteo_PM`.

- You can find your organization namespace by going to your organization settings in the [Viam app](https://app.viam.com).
- The repo name (also called family name) is generally the name of the GitHub repo where you will put your module code.
  Name it something related to what your module does.
- Name your sensor based on what it supports, for example, if it supports a model of ultrasonic sensor called "XYZ Sensor 1234" you could call your model `XYZ_1234` or similar.

For more information, see [Name your new resource model](/how-tos/create-module/#name-your-new-resource-model).

{{% /tablestep %}}
{{% tablestep %}}
**4. Specify the API**

For the API triplet, enter `rdk:component:sensor`.
This means that you are implementing the standard Viam sensor API.

When asked whether this is a Viam SDK built-in API, enter `yes`.

{{% /tablestep %}}
{{< /table >}}
<br>

The generator creates a `run.sh` file, a `requirements.txt` file, a readme, and source code files.
In the next section, you'll customize some of these files to support your sensor.

## Implement the sensor API

Other than the inherited methods, the [sensor API](/components/sensor/#api) only contains one method, `GetReadings()`.
You need to implement this method so your sensor supports the sensor API:

{{< table >}}
{{% tablestep %}}
**1. Edit configuration code**

In the generated <file>/YOUR_MODULE_NAME/src/</file> directory, open the </file>MODEL_NAME.py</file> file.

Edit the config attributes to fit your sensor.
For example, if your sensor requires two pins, copy the `some_pin` lines and add another pin with a different name.
If you want to be able to configure something else, for example the location to get online data from, you can add attributes for that.
If your sensor doesn't require any configuration, delete the `some_pin` lines but don't delete the `validate` and `reconfigure` functions entirely; they're needed for the module to function even if they don't actually validate the input or reconfigure the resource.

{{% /tablestep %}}
{{% tablestep %}}
**2. Define `get_readings`**

In the `get_readings` function definition, paste your test script.
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
# meteo_PM.py
from typing import ClassVar, Mapping, Any, Optional
from typing_extensions import Self

from viam.utils import SensorReading, struct_to_dict
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.sensor import Sensor
from viam.logging import getLogger

import openmeteo_requests
import requests_cache
from retry_requests import retry

LOGGER = getLogger(__name__)


class meteo_PM(Sensor, Reconfigurable):

    """
    Sensor represents a sensing device that can provide measurement readings.
    """

    MODEL: ClassVar[Model] = Model(
      ModelFamily("jessamy", "weather"), "meteo_PM")

    # Class parameters
    latitude: float  # Latitude at which to get data
    longitude: float  # Longitude at which to get data

    # Constructor
    @classmethod
    def new(
      cls, config: ComponentConfig,
      dependencies: Mapping[ResourceName, ResourceBase]
      ) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        fields = config.attributes.fields
        # Check that configured fields are floats
        if "latitude" in fields:
            if not fields["latitude"].HasField("number_value"):
                raise Exception("Latitude must be a float.")

        if "longitude" in fields:
            if not fields["longitude"].HasField("number_value"):
                raise Exception("Longitude must be a float.")
        return

    # Handles attribute reconfiguration
    def reconfigure(
      self, config: ComponentConfig,
      dependencies: Mapping[ResourceName, ResourceBase]
      ):
        attrs = struct_to_dict(config.attributes)

        self.latitude = float(attrs.get("latitude", 45))
        LOGGER.debug("Using latitude: " + str(self.latitude))

        self.longitude = float(attrs.get("longitude", -121))
        LOGGER.debug("Using longitude: " + str(self.longitude))

        return

    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None, **kwargs
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

        LOGGER.info(current_pm2_5)

        # Return a dictionary of the readings
        return {
            "pm2_5": current_pm2_5,
            "pm10": current_pm10
        }
```

{{< /expand >}}

For more examples, see other sensor modules in the [Viam Registry](https://app.viam.com/registry).
Most modules have their implementation code linked on their module page, so you can see how they work.

## Edit requirements.txt

Update the generated <file>requirements.txt</file> file to include any packages that must be installed for the module to run.
Depending on your use case, you may not need to add anything here beyond `viam-sdk` which is auto-populated.

## Make the module executable

You need an executable file so that `viam-server` can run your module.
The module generator already created the <file>run.sh</file> "entrypoint" file for you, so all you need to do is make this file executable by running the following command with your correct file path:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo chmod +x <your-file-path-to>/run.sh
```

## Test your module locally

{{% expand "Prerequisite: A running machine connected to the Viam app." %}}

You can write a module without a machine, but to test your module you'll need a machine.
Make sure to physically connect your sensor to your machine's computer to prepare your machine for testing.

{{% snippet "setup.md" %}}

{{% /expand%}}

It's a good idea to test your module locally before uploading it to the [Viam registry](https://app.viam.com/registry):

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

Enter your {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}} you specified in the [Name your model step](/how-tos/sensor-module/#generate-template-module-code), for example `jessamy:weather:meteo-PM`.
Click **Create**.

![Configuring a local model after the local module is configured.](/how-tos/sensor-module-config.png)

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
