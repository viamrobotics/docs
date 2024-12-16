---
linkTitle: "Integrate other hardware"
title: "Integrate other hardware"
weight: 30
layout: "docs"
type: "docs"
no_list: true
description: "Add support for more hardware to the Viam ecosystem."
---

If your hardware is not [already supported](../supported-hardware/) by an existing {{< glossary_tooltip term_id="module" text="module" >}}, you can create a new module to add support for it.
You can keep the module private or share it with your organization or the public.
You can use built-in tools to manage versioning and deployment to machines as you iterate on your module.

{{% alert title="In this page" color="info" %}}

1. [Design your module](#design-your-module)
1. [Write your module](#write-your-module)
1. [Test your module locally](#test-your-module-locally)
1. [Upload your module](#upload-your-module)

{{% /alert %}}
{{% alert title="See also" color="info" %}}

- [Write a module for microcontrollers (to use alongside viam-micro-server)](./micro-module/)
- [Hello World guide to writing a module with Python or Go](./hello-world-module/)
- [Write a module with C++](./cpp-module/)
- [Update and manage modules](./manage-modules/)

{{% /alert %}}

## Design your module

### Write a test script (optional)

You can think of a module as a packaged wrapper around some script, that takes the functionality of the script and maps it to a standardized API for use within the Viam ecosystem.
Start by finding or writing a test script to check that you can connect to and control your hardware from your computer, perhaps using the manufacturer's API or other low-level code.

### Choose an API

Decide exactly what functionality you want your module to provide in terms of inputs and outputs.
With this in mind, look through the [component APIs](/dev/reference/apis/#component-apis) and choose one that fits your use case.

For example, if you just need to get readings or other data and don't need any other endpoints, you could use the [sensor API](/dev/reference/apis/components/sensor/), which contains only the `GetReadings` method (as well as the methods that all Viam resources implement: `Reconfigure`, `DoCommand`, `GetResourceName`, and `Close`).

You do not need to fully implement all the methods of an API.
For example, if you want to use the [camera API](/dev/reference/apis/components/camera/) because you want to return images, but your camera does not get point cloud data, you can implement the `GetImage` method but for the `GetPointCloud` method you can return nil and an "unimplemented" error or similar, depending on the method and the language you use to write your module.

If you need a method that is not in your chosen API, you can use the flexible `DoCommand` (which is built into all component APIs) to create custom commands.

### Decide on configuration attributes and dependencies

Make a list of required and optional attributes for users to configure when adding your module to a machine.
For example, you can require users to configure a path from which to access data, or a pin to which a device is wired, and you could allow them to optionally change a frequency from some default.
You'll need to add these attributes to the `Validate` and `Reconfigure` functions when you write the module.

## Write your module

### Generate stub files

The easiest way to generate the files for your module is to use the [Viam CLI](/cli/):

1. Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

   {{< expand "Install the Viam CLI and authenticate" >}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

1. Run the `module generate` command in your terminal:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate
   ```

1. Follow the prompts.
   Find more information in the following table:

<!--prettier-ignore-->
| Prompt | Description |
| -------| ----------- |
| Module name | The module name describes the module or the family of devices it supports. It is generally the same as the name of the GitHub repo where you will put your module code. |
| Language | The language for the module. |
| Visibility | Choose `Private` to share only with your organization, or `Public` to share publicly with all organizations. If you are testing, choose `Private`. |
| Namespace/Organization ID | In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page. Find the **Public namespace** and copy that string. |
| Resource to add to the module (API) | The [component API](/appendix/apis/#component-apis) your module will implement. |
| Model name | Name your component model based on what it supports, for example, if it supports a model of ultrasonic sensor called “XYZ Sensor 1234” you could call your model `XYZ_1234` or similar. |
| Enable cloud build | You can select `No` if you will always build the module yourself before uploading it. If you select `Yes` and push the generated files (including the <file>.github</file> folder) and create a release of the format `vX.X.X`, the module will build and upload to the Viam registry and be available for all Viam-supported architectures without you needing to build for each architecture. |
| Register module | Select `Yes` unless you are creating a local-only module for testing purposes and do not intend to upload it. |

The generator will create a folder containing stub files for your modular sensor component.
In the next section, you'll customize some of the generated files to support your sensor.

#### Creating multiple models within one module

If you have multiple modular components that are related to or even dependent upon each other, you can opt to put them all into one module.
For an example of how this is done, see [Create a Hello World module](/operate/get-started/other-hardware/hello-world-module/).

### Implement the component API

Edit the generated files to add your logic:

{{< tabs >}}
{{% tab name="Python" %}}

1. Open <file>/src/main.py</file>.
1. **Edit the `validate_config` function** to do the following:

   - Check that the user has configured required attributes
   - Return any implicit dependencies

      <details>
        <summary><strong>Explicit versus implicit dependencies</strong></summary>

     Some modular resources require that other {{< glossary_tooltip term_id="resource" text="resources" >}} start up first.
     For example, a mobile robotic base might need its motors to instantiate before the overall base module instantiates.
     If your use case requires that things initialize in a specific order, you have two options:

     - Explicit dependencies: Require that a user list the names of all resources that must start before a given component in the `depends_on` field of the component's configuration.
       - Useful when dependencies are optional.
     - Implicit dependencies: Instead of explicitly using the `depends_on` field, require users to configure a named attribute (for example `"left-motor": "motor1"`), and write your module with that attribute as a dependency.
       Note that most named attributes are _not_ dependencies; you need to specify a resource as not only an attribute but also a dependency for it to be initialized first.
       See code examples below.

       - This is the preferred method when dependencies are required, because implicit dependencies make it more clear what needs to be configured, they eliminate the need for the same attribute to be configured twice, and they make debugging easier.

       </details><br>

1. **Edit the `reconfigure` function** to do the following:

   - Assign any default values as necessary to any optional attributes if the user hasn't configured them.<br><br>

1. **Edit the methods you want to implement**:

   For each method you want to implement, replace the body of the method with the relevant logic from your test script.
   Make sure you return the correct type in accordance with the function's return signature.
   You can find details about the return types at [python.viam.dev](https://python.viam.dev/autoapi/viam/components/index.html).

{{< expand "Example code for a sensor module" >}}

The following code implements the sensor API by getting weather data from Open-Meteo and returning it using the `get_readings` function.

The `validate` and `reconfigure` functions have been edited so that the user can configure coordinates from which to get weather data, but if the user does not configure these optional attributes, defaults are assigned.

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from typing import Any, ClassVar, Final, Mapping, Optional, Sequence

from typing_extensions import Self
from viam.components.sensor import Sensor
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
    MODEL: ClassVar[Model] = Model(
      ModelFamily("jessamy", "weather"), "meteo_PM")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[
          ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter
        and then calls `reconfigure`.
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object
        received from the machine, as well as to return any implicit
        dependencies based on that `config`.
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
        self, config: ComponentConfig, dependencies: Mapping[
          ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service
        when it receives a new `config` object.
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

5. **Add logging** messages as desired.
   The following log levels are available for resource logs:

   ```python {class="line-numbers linkable-line-numbers"}
    # Within some method, log information:
    self.logger.debug("debug info")
    self.logger.info("info")
    self.logger.warn("warning info")
    self.logger.error("error info")
    self.logger.exception("error info", exc_info=True)
    self.logger.critical("critical info")
   ```

   Resource-level logs are recommended instead of global logs for modular resources, because they make it easier to determine which component or service an error is coming from.
   Resource-level error logs appear in the <strong>ERROR LOGS</strong> section of each resource’s configuration card in the app.

   {{% alert title="Note" color="note" %}}
   In order to see resource-level debug logs when using your modular resource, you'll either need to run `viam-server` with the `-debug` option or [configure your machine or individual resource to display debug logs](/architecture/viam-server/#logging).
   {{% /alert %}}

{{< expand "Click for global logging information" >}}

If you need to publish to the global machine-level logs instead of using the recommended resource-level logging, you can follow this example:

```python {class="line-numbers linkable-line-numbers" data-line="2,5"}
# In your import block, import the logging package:
from viam.logging import getLogger

# Before your first class or function, define the LOGGER variable:
LOGGER = getLogger(__name__)

# in some method, log information
LOGGER.debug("debug info")
LOGGER.info("info info")
LOGGER.warn("warn info")
LOGGER.error("error info")
LOGGER.exception("error info", exc_info=True)
LOGGER.critical("critical info")
```

{{< /expand >}}

{{% /tab %}}
{{% tab name="Go" %}}

1. Open `/models/<model-name>.go` and add necessary imports.

{{% /tab %}}
{{< /tabs >}}

5. Edit the generated <file>requirements.txt</file> file to include any packages that must be installed for the module to run.
   Depending on your use case, you may not need to add anything here beyond `viam-sdk` which is auto-populated.

## Test your module locally

## Upload your module
