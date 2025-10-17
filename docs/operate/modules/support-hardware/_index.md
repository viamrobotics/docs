---
title: "Support additional hardware and software"
linkTitle: "Support hardware"
weight: 30
layout: "docs"
type: "docs"
icon: true
images: ["/registry/create-module.svg"]
description: "Add support for more physical or virtual hardware to the Viam ecosystem by creating a custom module."
aliases:
  - /registry/create/
  - /use-cases/create-module/
  - /how-tos/create-module/
  - /how-tos/sensor-module/
  - /registry/advanced/iterative-development/
  - /build/program/extend/modular-resources/
  - /program/extend/modular-resources/
  - /extend/
  - /extend/modular-resources/
  - /extend/modular-resources/create/
  - /build/program/extend/modular-resources/key-concepts/
  - /modular-resources/key-concepts/
  - /modular-resources/
  - /extend/modular-resources/examples/custom-arm/
  - /modular-resources/examples/custom-arm/
  - /registry/examples/custom-arm/
  - /program/extend/modular-resources/examples/
  - /extend/modular-resources/examples/
  - /modular-resources/examples/
  - /registry/examples/
  - /operate/get-started/other-hardware/
  - /operate/get-started/other-hardware/create-module/
  - /operate/modules/other-hardware/create-module/
---

If your physical or virtual hardware is not [already supported](/operate/modules/configure-modules/) by an existing {{< glossary_tooltip term_id="module" text="module" >}}, you can create a new module to add support for it.
You can keep the module private or share it with your organization or the public.
You can use built-in tools to manage versioning and deployment to machines as you iterate on your module.

{{% hiddencontent %}}
If you want to create a "custom module", this page provides instructions for creating one in Python and Go.
{{% /hiddencontent %}}

This page provides instructions for creating and uploading a module in Python or Go.
For C++ module examples, see the [C++ examples directory on GitHub](https://github.com/viamrobotics/viam-cpp-sdk/tree/main/src/viam/examples/).
If you want to create a module for use with a microcontroller, see [Modules for ESP32](/operate/modules/advanced/micro-module/).

{{< expand "How to design your module" >}}

If you want to plan your module before you write it, you can use the following steps to design your module:

1. **Write a test script (optional)**

   You can think of a module as a packaged wrapper around some script, that takes the functionality of the script and maps it to a standardized API for use within the Viam ecosystem.
   Start by finding or writing a test script to check that you can connect to and control your hardware from your computer, perhaps using the manufacturer's API or other low-level code.

   <br>

2. **Choose an API**

   Decide exactly what functionality you want your module to provide in terms of inputs and outputs.
   With this in mind, look through the [component APIs](/dev/reference/apis/#component-apis) and choose one that fits your use case.
   Each model implements one API.

   <br>

   For example, if you just need to get readings or other data and don't need any other endpoints, you could use the [sensor API](/dev/reference/apis/components/sensor/), which contains only the `GetReadings` method (as well as the methods that all Viam resources implement: `Reconfigure`, `DoCommand`, `GetResourceName`, and `Close`).

   <br>

   You do not need to fully implement all the methods of an API.
   For example, if you want to use the [camera API](/dev/reference/apis/components/camera/) because you want to return images, but your camera does not get point cloud data, you can implement the `GetImage` method but for the `GetPointCloud` method you can return nil and an "unimplemented" error or similar, depending on the method and the language you use to write your module.

   <br>

   If you need a method that is not in your chosen API, you can use the flexible `DoCommand` (which is built into all component APIs) to create custom commands.

   <br>

3. **Decide on configuration attributes and dependencies**

   Make a list of required and optional attributes for users to configure when adding your module to a machine.
   Some examples of attributes:

   - A filepath from which to access data
   - A pin to which a device is wired
   - An optional signal frequency to override a default value

   You can also add dependencies to other resources that your module needs to use.
   For example, if your module needs to access a camera, code your module to get a camera resource as a dependency.
   This will allow you to access the camera with the camera API methods from within your module.

   You'll add these attributes and dependencies to the `Validate` and `Reconfigure` functions when you write the module.

{{< /expand >}}

## Write your module

### Generate stub files

The easiest way to generate the files for your module is to use the [Viam CLI](/dev/tools/cli/):

1. Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

   {{< expand "Install the Viam CLI and authenticate" >}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

1. Run the `module generate` command in your terminal.
   If you are writing your module using Python, you must have Python version 3.11 or newer installed on your computer for this command to work:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module generate
   ```

1. Follow the prompts.

   {{< expand "Click for more details about each prompt" >}}

<!--prettier-ignore-->
| Prompt | Description |
| -------| ----------- |
| Module name | The module name describes the module or the family of devices it supports. It is generally the same as the name of the GitHub repo where you will put your module code. |
| Language | The language for the module. |
| Visibility | Choose `Private` to share only with your organization, or `Public` to share publicly with all organizations. If you are testing, choose `Private`. |
| Namespace/Organization ID | Navigate to your organization settings through the menu in upper right corner of the page. Find the **Public namespace** (or create one if you haven't already) and copy that string. If you use the organization ID, you must still create a public namespace first. |
| Resource to add to the module (API) | The [component API](/dev/reference/apis/#component-apis) your module will implement. See [How to design your module](./#how-to-design-your-module) for more information. |
| Model name | Name your component model based on what it supports, for example, if it supports a model of ultrasonic sensor called "XYZ Sensor 1234" you could call your model `xyz_1234` or similar. Must be all-lowercase and use only alphanumeric characters (`a-z` and `0-9`), hyphens (`-`), and underscores (`_`). |
| Enable cloud build | If you select `Yes` (recommended) and push the generated files (including the <file>.github</file> folder) and create a release of the format `vX.X.X`, the module will build and upload to the Viam registry and be available for all Viam-supported architectures without you needing to build for each architecture. `Yes` also makes it easier to [upload](#upload-your-module) using PyInstaller by creating a build entrypoint script. You can select `No` if you will always build the module yourself before uploading it. |
| Register module | Select `Yes` unless you are creating a local-only module for testing purposes and do not intend to upload it. Registering a module makes its name and metadata appear in the registry; uploading the actual code that powers the module is a separate step. If you decline to register the module at this point, you can run [`viam module create`](/dev/tools/cli/#module) to register it later. |

{{< /expand >}}

The generator will create a folder containing stub files for your modular sensor component.
In the next section, you'll customize some of the generated files to support your sensor.

#### Creating multiple models within one module

If you have multiple modular components that are related to or even dependent upon each other, you can opt to put them all into one module.
Note that each model can implement only one API.
For an example of how this is done, see [Create a Hello World module](/operate/modules/hello-world-module/).

### Implement the component API

Edit the generated files to add your logic:

{{< tabs >}}
{{% tab name="Python" %}}

{{< table >}}
{{< tablestep >}}
Open <file>/src/models/&lt;model-name&gt;.py</file> and add any necessary imports.
{{% /tablestep %}}
{{< tablestep >}}
**Edit the `validate_config` function** to do the following:

- Check that the user has configured required attributes and return errors if they are missing.
- Return a map of any dependencies ({{< glossary_tooltip term_id="resource" text="resources" >}} that your module needs).

For more information, see [Module dependencies](/operate/modules/dependencies/).

{{% /tablestep %}}
{{< tablestep >}}

**Edit the `reconfigure` function**, which gets called when the user changes the configuration.
This function should do the following:

- If you assigned any configuration attributes to global variables, get the values from the latest `config` object and update the values of the global variables.
- Assign default values as necessary to any optional attributes if the user hasn't configured them.
- If your module has dependencies, get the dependencies from the `dependencies` map and cast each resource according to which API it implements, as described in [Module dependencies](/operate/modules/dependencies/).
  {{% /tablestep %}}
  {{< tablestep >}}

**Edit the methods you want to implement**:

For each method you want to implement, replace the body of the method with your relevant logic.
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


class meteo_PM(Sensor, EasyResource):
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
        received from the machine, as well as to return any
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

You can find more examples by looking at the source code GitHub repos linked from each module in the [registry](https://app.viam.com/registry).

{{% /tablestep %}}
{{< tablestep >}}

**Add logging** messages as desired.
The following log severity levels are available for resource logs:

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
Resource-level error logs appear in the <strong>ERROR LOGS</strong> section of each resource's configuration card in the app.

{{% alert title="Note" color="note" %}}
In order to see resource-level debug logs when using your modular resource, you'll either need to run `viam-server` with the `-debug` option or [configure your machine or individual resource to display debug logs](/operate/reference/viam-server/#logging).
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

{{% /tablestep %}}
{{< tablestep >}}

**Edit the generated <file>requirements.txt</file> file** to include any packages that must be installed for the module to run.
Depending on your use case, you may not need to add anything here beyond <code>viam-sdk</code> which is auto-populated.

{{% /tablestep %}}
{{< /table >}}

For most modules, you do not need to edit the <file>main.py</file> file, unless you are implementing multiple models in the same module as in [Create a Hello World module](/operate/modules/hello-world-module/).

{{% hiddencontent %}}

You may see examples in registry modules that use a different pattern from what the generator creates.
For example, some older example modules define `async def main()` inside <file>main.py</file>.
We recommend using the pattern the generator follows:

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from viam.module.module import Module
try:
    from models.hello_camera import MyCamera
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.hello_camera import MyCamera

if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
```

A previous version of the CLI module generator created `__init__.py` files, but now uses a different module structure.
We recommend using what the current generator creates rather than old examples that use `__init__.py` files.

{{% /hiddencontent %}}

{{% /tab %}}
{{% tab name="Go" %}}

{{% hiddencontent %}}
`resource.AlwaysRebuild` provides an implementation of `Reconfigure` that returns a `NewMustRebuild` error.
This error doesn't exist in the other SDKs, so `AlwaysRebuild` is not supported in those SDKs.
{{% /hiddencontent %}}

{{< table >}}
{{< tablestep start=1 >}}
Open <file>module.go</file> and add necessary imports.
{{% /tablestep %}}
{{< tablestep >}}
**Add any configurable attributes to the `Config` struct.**
{{% /tablestep %}}
{{< tablestep >}}
**Edit the `Validate` function** to do the following:

- Check that the user has configured required attributes and return errors if they are missing.
- Return any dependencies ({{< glossary_tooltip term_id="resource" text="resources" >}} that your module needs to use).

For more information, see [Module dependencies](/operate/modules/dependencies/).
{{% /tablestep %}}
{{< tablestep >}}

**(Optional) Create and edit a `Reconfigure` function**:

In most cases, you can omit this function and leave `resource.AlwaysRebuild` in the `Config` struct.
This will cause `viam-server` to fully rebuild the resource each time the user changes the configuration.

If you need to maintain the state of the resource, for example if you are implementing a board and need to keep the software PWM loops running, you should implement this function so that `viam-server` updates the configuration without rebuilding the resource from scratch.
In this case, your `Reconfigure` function should do the following:

- If you assigned any configuration attributes to global variables, get the values from the latest `config` object and update the values of the global variables.
- Assign default values as necessary to any optional attributes if the user hasn't configured them.

For an example that implements the `Reconfigure` method, see [<file>mybase.go</file> on GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go).

{{% /tablestep %}}
{{< tablestep >}}

**Edit the constructor** to do the following:

- If you didn't create a `Reconfigure` function, use the constructor to assign default values as necessary to any optional attributes if the user hasn't configured them.
- If you created a `Reconfigure` function, make your constructor call `Reconfigure`.

{{% /tablestep %}}
{{< tablestep >}}

**Edit the methods you want to implement**:

For each method you want to implement, replace the body of the method with your relevant logic.
Make sure you return the correct type in accordance with the function's return signature.
You can find details about the return types at [go.viam.com/rdk/components](https://pkg.go.dev/go.viam.com/rdk/components).

{{< expand "Example code for a camera module" >}}
This example from [Hello World module](/operate/modules/hello-world-module/) implements only one method of the camera API by returning a static image.
It demonstrates a required configuration attribute (`image_path`) and an optional configuration attribute (`example_value`).

```go {class="line-numbers linkable-line-numbers"}
package hello_world

import (
  "context"
  "errors"
  "os"
  "reflect"

  "go.viam.com/rdk/components/camera"
  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/pointcloud"
  "go.viam.com/rdk/resource"
  "go.viam.com/utils/rpc"
)

var (
  HelloCamera      = resource.NewModel("jessamy", "hello-world", "hello-camera")
  errUnimplemented = errors.New("unimplemented")
)

func init() {
  resource.RegisterComponent(camera.API, HelloCamera,
    resource.Registration[camera.Camera, *Config]{
      Constructor: newHelloWorldHelloCamera,
    },
  )
}

type Config struct {
  ImagePath    string `json:"image_path"`
  ExampleValue string `json:"example_value"`
}

func (cfg *Config) Validate(path string) ([]string, error) {
  var deps []string
  if cfg.ImagePath == "" {
    return nil, resource.NewConfigValidationFieldRequiredError(path, "image_path")
  }
  if reflect.TypeOf(cfg.ImagePath).Kind() != reflect.String {
    return nil, errors.New("image_path must be a string.")
  }
  if cfg.ExampleValue != "" && reflect.TypeOf(cfg.ExampleValue).Kind() != reflect.String {
    return nil, errors.New("example_value must be a string.")
  }
  return deps, nil
}

type helloWorldHelloCamera struct {
  resource.AlwaysRebuild // Resource rebuilds instead of reconfiguring

  name resource.Name

  logger logging.Logger
  cfg    *Config

  exampleValue string

  cancelCtx  context.Context
  cancelFunc func()
}

func newHelloWorldHelloCamera(ctx context.Context, deps resource.Dependencies, rawConf resource.Config, logger logging.Logger) (camera.Camera, error) {
  conf, err := resource.NativeConfig[*Config](rawConf)
  if err != nil {
    return nil, err
  }

  cancelCtx, cancelFunc := context.WithCancel(context.Background())

  s := &helloWorldHelloCamera{
    name:       rawConf.ResourceName(),
    logger:     logger,
    cfg:        conf,
    cancelCtx:  cancelCtx,
    cancelFunc: cancelFunc,
}

  s.exampleValue = s.cfg.ExampleValue
  if s.exampleValue == "" {
    s.exampleValue = "default value"
    s.logger.Debug("setting default exampleValue: %s", s.exampleValue)
  }

 return s, nil
}

func (s *helloWorldHelloCamera) Name() resource.Name {
  return s.name
}

func (s *helloWorldHelloCamera) Image(ctx context.Context, mimeType string, extra map[string]interface{}) ([]byte, camera.ImageMetadata, error) {
  imagePath := s.cfg.ImagePath
  imgFile, err := os.Open(imagePath)
  if err != nil {
    return nil, camera.ImageMetadata{}, errors.New("Error opening image.")
  }
  defer imgFile.Close()
  imgByte, err := os.ReadFile(imagePath)
  s.logger.Info("The s.exampleValue is: " + s.exampleValue)
  return imgByte, camera.ImageMetadata{}, nil
}

func (s *helloWorldHelloCamera) NewClientFromConn(ctx context.Context, conn rpc.ClientConn, remoteName string, name resource.Name, logger logging.Logger) (camera.Camera, error) {
  return nil, errors.New("not implemented")
}

func (s *helloWorldHelloCamera) Images(ctx context.Context) ([]camera.NamedImage, resource.ResponseMetadata, error) {
  return []camera.NamedImage{}, resource.ResponseMetadata{}, errors.New("not implemented")
}

func (s *helloWorldHelloCamera) NextPointCloud(ctx context.Context) (pointcloud.PointCloud, error) {
  return nil, errors.New("not implemented")
}

func (s *helloWorldHelloCamera) Properties(ctx context.Context) (camera.Properties, error) {
  return camera.Properties{}, errors.New("not implemented")
}

func (s *helloWorldHelloCamera) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
  return map[string]interface{}{}, errors.New("not implemented")
}

func (s *helloWorldHelloCamera) Close(context.Context) error {
  s.cancelFunc()
  return nil
}

```

{{< /expand >}}

You can find more examples by looking at the source code GitHub repos linked from each module in the [registry](https://app.viam.com/registry).
{{% /tablestep %}}
{{< tablestep >}}
**Add logging** messages as desired.

You can add log messages with various levels of severity:

```go {class="line-numbers linkable-line-numbers"}
fn (c *component) someFunction(ctx context.Context, a int) {
  // Log with severity info:
  c.logger.CInfof(ctx, "performing some function with a=%v", a)
  // Log with severity debug (using value wrapping):
  c.logger.CDebugw(ctx, "performing some function", "a" ,a)
  // Log with severity warn:
  c.logger.CWarnw(ctx, "encountered warning for component", "name", c.Name())
  // Log with severity error without a parameter:
  c.logger.CError(ctx, "encountered an error")
}
```

{{% /tablestep %}}
{{< /table >}}

{{% alert title="Note" color="note" %}}
In order to see debug logs when using your modular resource, you'll need to run `viam-server` with the `-debug` option.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

## Test your module locally

It's a good idea to test your module locally before uploading it to the [registry](https://app.viam.com/registry).
You can configure it in the web UI using the local files on your machine.

{{% expand "Prerequisite: A running machine connected to Viam." %}}

You can write a module without a machine, but to test your module you'll need a [machine](/operate/install/setup/).
Make sure to physically connect your sensor to your machine's computer to prepare your machine for testing.

{{% snippet "setup.md" %}}

{{% /expand%}}

{{< table >}}
{{% tablestep start=1 %}}
**Prepare to run your module**

{{< tabs >}}
{{% tab name="Python: Hot reloading (recommended)" %}}

If you enabled cloud build, use these steps.

1. Create a <file>reload.sh</file> script in your module directory.
   You'll use this for local testing and can delete it before you upload your module.
   Paste the following contents into it and save the file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   #!/usr/bin/env bash

    # bash safe mode. look at `set --help` to see what these are doing
    set -euxo pipefail

    cd $(dirname $0)
    MODULE_DIR=$(dirname $0)
    VIRTUAL_ENV=$MODULE_DIR/venv
    PYTHON=$VIRTUAL_ENV/bin/python
    ./setup.sh

    # Be sure to use `exec` so that termination signals reach the python process,
    # or handle forwarding termination signals manually
    exec $PYTHON src/main.py $@
   ```

1. Make your reload script executable by running the following command in your module directory:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   chmod 755 reload.sh
   ```

1. Create a virtual Python environment with the necessary packages by running the setup file from within the module directory:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   sh setup.sh
   ```

1. Edit your <file>meta.json</file>, replacing the `"entrypoint"`, `"build"`, and `"path"` fields as follows:

   ```json {class="line-numbers linkable-line-numbers" data-start="13" data-line="1, 4, 6" }
     "entrypoint": "reload.sh",
     "first_run": "",
     "build": {
       "build": "rm -f module.tar.gz && tar czf module.tar.gz requirements.txt src/*.py src/models/*.py meta.json setup.sh reload.sh",
       "setup": "./setup.sh",
       "path": "module.tar.gz",
       "arch": [
         "linux/amd64",
         "linux/arm64"
       ]
     }
   ```

{{% /tab %}}
{{% tab name="Python: venv" %}}

Create a virtual Python environment with the necessary packages by running the setup file from within the module directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
```

This environment is where the local module will run.
`viam-server` does not need to run inside this environment.

{{% /tab %}}
{{% tab name="Go" %}}

From within the module directory, compile your module into a single executable:

```sh {class="command-line" data-prompt="$" data-output="5-10"}
viam module build local
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure your local module on a machine**

<a name="reload"></a>

{{< tabs >}}
{{% tab name="Python: Hot reloading (recommended)" %}}

Run the following command to build and start your module and push it to your machine:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload <insert relevant named args>
```

{{< expand "Reload example commands" >}}

For example, to run on your development machine:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --local
```

Or to run on a different machine (such as a single-board computer), specify the part ID of the remote machine:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id 123abc45-1234-432c-aabc-z1y111x23a00
```

{{< /expand >}}

For more information, run the command with the `-h` flag or see the [CLI documentation](/dev/tools/cli/#module).

{{< expand "Reload troubleshooting" >}}

`Error: Could not connect to machine part: context deadline exceeded; context deadline exceeded; mDNS query failed to find a candidate`

- Try specifying the `--part-id`, which you can find by clicking the **Live** indicator on your machine's page and clicking **Part ID**.

`Error: Rpc error: code = Unknown desc = stat /root/.viam/packages-local: no such file or directory`

- Try specifying the `--home` directory, for example `/Users/jessamy/` on macOS.

`Error: Error while refreshing token, logging out. Please log in again`

- Run `viam login` to reauthenticate the CLI.

### Try using a different command

If you are still having problems with the `reload` command, you can use a different, slower method of rebuilding and then restarting the module.
Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it in your machine's **CONFIGURE** tab.
In upper right corner of the module's card, click the **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="width:300px" class="shadow" >}}

{{< /expand >}}

When you run `viam module reload`, the module will be added to your device automatically.

{{% /tab %}}
{{% tab name="Python: venv" %}}

On your machine's **CONFIGURE** tab, click the **+** (create) icon in the left-hand menu.
Select **Local module**, then **Local module**.

Enter the absolute path to the <file>run.sh</file> script, for example `/home/jessamy/my-module/run.sh` on Linux, or `/Users/jessamy/my-python-sensor-module/run.sh` on macOS.
For modules configured this way, `viam-server` uses this path instead of the `entrypoint` field in your <file>meta.json</file> file.

Click **Create**.

{{% /tab %}}
{{% tab name="Go" %}}

On your machine's **CONFIGURE** tab, click the **+** (create) icon in the left-hand menu.
Select **Local module**, then **Local module**.

Enter the absolute path to the <file>/bin/&#60;module-name&#62;</file> executable, for example `/home/jessamy/my-go-module/bin/mymodule` on Linux, or `/Users/jessamy/my-go-module/bin/mymodule` on macOS.
For modules configured this way, `viam-server` uses this path instead of the `entrypoint` field in your <file>meta.json</file> file.

Click **Create**.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**Configure the model provided by your module**

Click the **+** button again, this time selecting **Local module** and then **Local component**.

Select or enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, for example `jessamy:weather:meteo-PM`.
You can find the triplet in the `model` field of your <file>meta.json</file> file.

Select the **Type** corresponding to the API you implemented.

Enter a **Name** such as `my-cool-component`.
Click **Create**.

{{<imgproc src="/how-tos/sensor-module-config.png" resize="600x" style="width: 300px" alt="Configuring a local model after the local module is configured" class="shadow" >}}

Configure any required attributes using proper JSON syntax.

{{% /tablestep %}}
{{% tablestep %}}
**Test the component**

Click the **TEST** bar at the bottom of your modular component configuration, and check whether it works as expected.
For example, if you created a sensor component, check whether readings are displayed.

{{<imgproc src="/how-tos/sensor-test.png" resize="x1100" declaredimensions=true alt="The test section of an example modular sensor, with readings displayed." style="width:600px" class="shadow" >}}

{{% /tablestep %}}
{{% tablestep %}}
**Iterate**

If your component works, you're almost ready to share your module by uploading it to the registry.
If not, you have some debugging to do.

Each time you make changes to your local module code, you need to update its instance on your machine:

{{< tabs >}}

{{% tab name="Python: PyInstaller (recommended)" %}}

Run the [reload command again](#reload) to rebuild and restart your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload <insert relevant named args>
```

{{% /tab %}}
{{% tab name="Python: venv" %}}

Since you are using <file>run.sh</file> instead of a built executable, you do not need to rebuild anything as you iterate.
Just save your code changes, then restart the module in your machine's **CONFIGURE** tab:
In upper right corner of the module's card, click **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="width:300px" class="shadow" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it in your machine's **CONFIGURE** tab.
In upper right corner of the module's card, click **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="max-width:300px" class="shadow" >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

See [Using the `build` subcommand](/dev/tools/cli/#using-the-build-subcommand) for advanced `build` options.

## Next steps

Once you have thoroughly tested your module, continue to [package and deploy](/operate/modules/deploy-module/) it.
