---
title: "Integrate other physical or virtual hardware"
linkTitle: "Integrate other hardware"
weight: 30
layout: "docs"
type: "docs"
icon: true
images: ["/registry/create-module.svg"]
description: "Add support for more physical or virtual hardware to the Viam ecosystem by creating a module."
aliases:
  - /registry/create/
  - /use-cases/create-module/
  - /how-tos/create-module/
  - /how-tos/sensor-module/
  - /registry/advanced/iterative-development/
  - /build/program/extend/modular-resources/
  - /program/extend/modular-resources/
  - /extend/modular-resources/
  - /extend/
  - /build/program/extend/modular-resources/key-concepts/
  - /modular-resources/key-concepts/
  - /modular-resources/
  - /how-tos/upload-module/
  - /extend/modular-resources/examples/custom-arm/
  - /modular-resources/examples/custom-arm/
  - /registry/examples/custom-arm/
  - /program/extend/modular-resources/examples/
  - /extend/modular-resources/examples/
  - /modular-resources/examples/
  - /registry/examples/
  - /extend/modular-resources/upload/
  - /modular-resources/upload/
  - /registry/upload/
prev: "/operate/get-started/supported-hardware/"
next: "/operate/get-started/other-hardware/hello-world-module/"
---

If your physical or virtual hardware is not [already supported](/operate/get-started/supported-hardware/) by an existing {{< glossary_tooltip term_id="module" text="module" >}}, you can create a new module to add support for it.
You can keep the module private or share it with your organization or the public.
You can use built-in tools to manage versioning and deployment to machines as you iterate on your module.

This page provides instructions for creating and uploading a module in Python or Go.
For C++ module examples, see the [C++ examples directory on GitHub](https://github.com/viamrobotics/viam-cpp-sdk/tree/main/src/viam/examples/).

{{% alert title="See also" color="info" %}}

- [Write a module for microcontrollers](/operate/get-started/other-hardware/micro-module/)
- [Hello World guide to writing a module with Python or Go](/operate/get-started/other-hardware/hello-world-module/)
- [Update and manage modules](/operate/get-started/other-hardware/manage-modules/)

{{% /alert %}}

{{< expand "How and where do modules run?" >}}
Modules run on your machine, alongside [`viam-server`](/operate/reference/viam-server/) as separate processes, communicating with `viam-server` over UNIX sockets.

When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and associated [APIs](/dev/reference/apis/) with `viam-server`, making the new model available for use.
`viam-server` manages the [dependencies](/operate/reference/viam-server/#dependency-management), [start-up](/operate/reference/viam-server/#start-up), [reconfiguration](/operate/reference/viam-server/#reconfiguration), [data management](/data-ai/capture-data/capture-sync/), and [shutdown](/operate/reference/viam-server/#shutdown) behavior of your modular resource.

For microcontrollers, you must flash a [firmware build that includes the Micro-RDK](/operate/get-started/other-hardware/micro-module/) and one or more modules onto your device.
{{< /expand >}}

## Design your module

{{< table >}}
{{% tablestep number=1 %}}
**Write a test script (optional)**

You can think of a module as a packaged wrapper around some script, that takes the functionality of the script and maps it to a standardized API for use within the Viam ecosystem.
Start by finding or writing a test script to check that you can connect to and control your hardware from your computer, perhaps using the manufacturer's API or other low-level code.

{{% /tablestep %}}
{{% tablestep number=2 %}}
**Choose an API**

Decide exactly what functionality you want your module to provide in terms of inputs and outputs.
With this in mind, look through the [component APIs](/dev/reference/apis/#component-apis) and choose one that fits your use case.
Each model implements one API.

For example, if you just need to get readings or other data and don't need any other endpoints, you could use the [sensor API](/dev/reference/apis/components/sensor/), which contains only the `GetReadings` method (as well as the methods that all Viam resources implement: `Reconfigure`, `DoCommand`, `GetResourceName`, and `Close`).

You do not need to fully implement all the methods of an API.
For example, if you want to use the [camera API](/dev/reference/apis/components/camera/) because you want to return images, but your camera does not get point cloud data, you can implement the `GetImage` method but for the `GetPointCloud` method you can return nil and an "unimplemented" error or similar, depending on the method and the language you use to write your module.

If you need a method that is not in your chosen API, you can use the flexible `DoCommand` (which is built into all component APIs) to create custom commands.

{{% /tablestep %}}
{{% tablestep number=3 %}}
**Decide on configuration attributes and dependencies**

Make a list of required and optional attributes for users to configure when adding your module to a machine.
For example, you can require users to configure a path from which to access data, or a pin to which a device is wired, and you could allow them to optionally change a frequency from some default.
You'll need to add these attributes to the `Validate` and `Reconfigure` functions when you write the module.

{{% /tablestep %}}
{{< /table >}}

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
| Namespace/Organization ID | In the [Viam app](https://app.viam.com), navigate to your organization settings through the menu in upper right corner of the page. Find the **Public namespace** (or create one if you haven't already) and copy that string. If you use the organization ID, you must still create a public namespace first. |
| Resource to add to the module (API) | The [component API](/dev/reference/apis/#component-apis) your module will implement. |
| Model name | Name your component model based on what it supports, for example, if it supports a model of ultrasonic sensor called "XYZ Sensor 1234" you could call your model `xyz_1234` or similar. Must be all-lowercase and use only alphanumeric characters (`a-z` and `0-9`), hyphens (`-`), and underscores (`_`). |
| Enable cloud build | If you select `Yes` (recommended) and push the generated files (including the <file>.github</file> folder) and create a release of the format `vX.X.X`, the module will build and upload to the Viam registry and be available for all Viam-supported architectures without you needing to build for each architecture. `Yes` also makes it easier to [upload](#upload-your-module) using PyInstaller by creating a build entrypoint script. You can select `No` if you will always build the module yourself before uploading it. |
| Register module | Select `Yes` unless you are creating a local-only module for testing purposes and do not intend to upload it. Registering a module makes its name and metadata appear in the Viam app registry page; uploading the actual code that powers the module is a separate step. If you decline to register the module at this point, you can run [`viam module create`](/dev/tools/cli/#module) to register it later. |

{{< /expand >}}

The generator will create a folder containing stub files for your modular sensor component.
In the next section, you'll customize some of the generated files to support your sensor.

#### Creating multiple models within one module

If you have multiple modular components that are related to or even dependent upon each other, you can opt to put them all into one module.
Note that each model can implement only one API.
For an example of how this is done, see [Create a Hello World module](/operate/get-started/other-hardware/hello-world-module/).

### Implement the component API

Edit the generated files to add your logic:

{{< tabs >}}
{{% tab name="Python" %}}

1. Open <file>/src/models/&lt;model-name&gt;.py</file> and add any necessary imports.
1. **Edit the `validate_config` function** to do the following:

   - Check that the user has configured required attributes and return errors if they are missing.
   - Return a map of any implicit dependencies.

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

       - See [<file>ackermann.py</file>](https://github.com/mcvella/viam-ackermann-base/blob/main/src/ackermann.py) or [Viam complex module examples on GitHub](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/complex_module/src) for example usage.

       </details><br>

1. **Edit the `reconfigure` function**, which gets called when the user changes the configuration.
   This function should do the following:

   - Get any values from the `config` object that the user has configured.
   - Assign default values as necessary to any optional attributes if the user hasn't configured them.
   - If your module has dependencies, get the dependencies from the `dependencies` map and cast each resource according to which API it implements, as in [this <file>ackermann.py</file> example](https://github.com/mcvella/viam-ackermann-base/blob/main/src/ackermann.py).

<ol><li style="counter-reset: item 3"><strong>Edit the methods you want to implement</strong>:

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

You can find more examples by looking at the source code GitHub repos linked from each module in the [Viam Registry](https://app.viam.com/registry).

</li></ol>

<ol><li style="counter-reset: item 4"><strong>Add logging</strong> messages as desired.
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

</li></ol>

<ol><li style="counter-reset: item 5"><strong>Edit the generated <file>requirements.txt</file> file</strong> to include any packages that must be installed for the module to run.
   Depending on your use case, you may not need to add anything here beyond <code>viam-sdk</code> which is auto-populated.

</li></ol>

{{% /tab %}}
{{% tab name="Go" %}}

1. Open <file>module.go</file> and add necessary imports.

1. **Add any configurable attributes to the `Config` struct.**

1. **Edit the `Validate` function** to do the following:

   - Check that the user has configured required attributes and return errors if they are missing.
   - Return any implicit dependencies.

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

       - See [<file>mybase.go</file> on GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go) for an example.

       </details><br>

1. **(Optional) Create and edit a `Reconfigure` function**:

   In most cases, you can omit this function and leave `resource.AlwaysRebuild` in the `Config` struct.
   This will cause `viam-server` to fully rebuild the resource each time the user changes the configuration.

   If you need to maintain the state of the resource, for example if you are implementing a board and need to keep the software PWM loops running, you should implement this function so that `viam-server` updates the configuration without rebuilding the resource from scratch.
   In this case, your `Reconfigure` function should do the following:

   - If you assigned any configuration attributes to global variables, get the values from the latest `config` object and update the values of the global variables.
   - Assign default values as necessary to any optional attributes if the user hasn't configured them.<br><br>

1. **Edit the constructor** to do the following:

   - Assign default values as necessary to any optional attributes if the user hasn't configured them.<br><br>

<ol><li style="counter-reset: item 4"><strong>Edit the methods you want to implement</strong>:

For each method you want to implement, replace the body of the method with the relevant logic from your test script.
Make sure you return the correct type in accordance with the function's return signature.
You can find details about the return types at [go.viam.com/rdk/components](https://pkg.go.dev/go.viam.com/rdk/components).

{{< expand "Example code for a camera module" >}}
This example from [Hello World module](/operate/get-started/other-hardware/hello-world-module/) implements only one method of the camera API by returning a static image.
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
  resource.AlwaysRebuild // Resource rebuilds instead of reconfiguring
  ImagePath string `json:"image_path"`
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

  s.exampleValue = "default value"

  return s, nil
}

func (s *helloWorldHelloCamera) Name() resource.Name {
  return s.name
}

func (s *helloWorldHelloCamera) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
  return errUnimplemented
}

func (s *helloWorldHelloCamera) Image(ctx context.Context, mimeType string, extra map[string]interface{}) ([]byte, camera.ImageMetadata, error) {
  imagePath := s.cfg.ImagePath
  imgFile, err := os.Open(imagePath)
  if err != nil {
    return nil, camera.ImageMetadata{}, errors.New("Error opening image.")
  }
  defer imgFile.Close()
  imgByte, err := ioutil.ReadFile(imagePath)
  s.logger.Info("The example value is: " + s.exampleValue)
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

You can find more examples by looking at the source code GitHub repos linked from each module in the [Viam Registry](https://app.viam.com/registry).

</li></ol>

<ol><li style="counter-reset: item 5"><strong>Add logging</strong> messages as desired.

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

</li></ol>

{{% alert title="Note" color="note" %}}
In order to see debug logs when using your modular resource, you'll need to run `viam-server` with the `-debug` option.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

## Test your module locally

It's a good idea to test your module locally before uploading it to the [Viam Registry](https://app.viam.com/registry).
You'll configure it through the Viam app, but the configured module will consist of local files.

{{% expand "Prerequisite: A running machine connected to the Viam app." %}}

You can write a module without a machine, but to test your module you'll need a [machine](/operate/get-started/setup/).
Make sure to physically connect your sensor to your machine's computer to prepare your machine for testing.

{{% snippet "setup.md" %}}

{{% /expand%}}

{{< table >}}
{{% tablestep number=1 %}}
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
make setup
viam module build local
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep number=2 %}}
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

- Try specifying the `--part-id`, which you can find by clicking the **Live** indicator on your machine's page in the Viam app and clicking **Part ID**.

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

Then restart it in your machine's **CONFIGURE** tab in the Viam app.
In upper right corner of the module's card, click the **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="max-width:300px" class="shadow" >}}

{{< /expand >}}

When you run `viam module reload`, the module will be added to your device automatically.

{{% /tab %}}
{{% tab name="Python: venv" %}}

On your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), click the **+** (create) icon in the left-hand menu.
Select **Local module**, then **Local module**.

Enter the absolute path to the <file>run.sh</file> script, for example `/home/jessamy/my-module/run.sh` on Linux, or `/Users/jessamy/my-python-sensor-module/run.sh` on macOS.

Click **Create**.

{{% /tab %}}
{{% tab name="Go" %}}

On your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com), click the **+** (create) icon in the left-hand menu.
Select **Local module**, then **Local module**.

Enter the absolute path to the <file>/bin/&#60;module-name&#62;</file> executable, for example `/home/jessamy/my-go-module/bin/mymodule` on Linux, or `/Users/jessamy/my-go-module/bin/mymodule` on macOS.

Click **Create**.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep number=3 %}}
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
{{% tablestep number=4 %}}
**Test the component**

Click the **TEST** bar at the bottom of your modular component configuration, and check whether it works as expected.
For example, if you created a sensor component, check whether readings are displayed.

{{<imgproc src="/how-tos/sensor-test.png" resize="x1100" declaredimensions=true alt="The test section of an example modular sensor, with readings displayed." style="max-width:600px" class="shadow" >}}

{{% /tablestep %}}
{{% tablestep number=5 %}}
**Iterate**

If your component works, you're almost ready to share your module by uploading it to the registry.
If not, you have some debugging to do.

Each time you make changes to your local module, you need to rebuild the module and then restart its instance on your machine.

{{< tabs >}}

{{% tab name="Python: PyInstaller (recommended)" %}}

Run the [reload command again](#reload) to rebuild and restart your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload <insert relevant named args>
```

{{% /tab %}}
{{% tab name="Python: venv" %}}

Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it in your machine's **CONFIGURE** tab in the Viam app.
In upper right corner of the module's card, click **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="max-width:300px" class="shadow" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it in your machine's **CONFIGURE** tab in the Viam app.
In upper right corner of the module's card, click **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="max-width:300px" class="shadow" >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

See [Using the `build` subcommand](/dev/tools/cli/#using-the-build-subcommand) for advanced `build` options.

## Upload your module

Once you are done testing locally, you can upload your module to the [Viam Registry](https://app.viam.com/registry) and make it available either to all machines in your organization, or to the general public.

{{< table >}}
{{% tablestep number=1 %}}
**Create a README (optional)**

It's quite helpful to create a README to document what your module does and how to use it, especially if you plan to share your module with others.

{{< expand "Example sensor module README" >}}

````md
# `meteo_PM` modular component

This module implements the [Viam sensor API](https://docs.viam.com/dev/reference/apis/components/sensor/) in a `jessamy:weather:meteo_PM` model.
With this model, you can gather [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api) PM2.5 and PM10 air quality data from anywhere in the world, at the coordinates you specify.

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com/).
Click the **+** button, select **Component**, then select the `sensor / weather:meteo_PM` model provided by the [`weather` module](https://app.viam.com/module/jessamy/weather).
Click **Add module**, enter a name for your sensor, and click **Create**.

## Configure your `meteo_PM` sensor

On the new component panel, copy and paste the following attribute template into your sensor's **Attributes** box:

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

{{% /tablestep %}}
{{% tablestep number=2 %}}
**Create a GitHub repo**

Create a GitHub repository with all the source code and the README for your module.
This is required for cloud build to work.

Add the link to that repo as the `url` in the <file>meta.json</file> file.

{{% /tablestep %}}
{{% tablestep number=3 %}}
**Edit the meta.json file**

Make any necessary edits to the `meta.json` file.
Click below for information about the available fields.

{{< expand "meta.json reference" >}}

<table class="table table-striped">
<tr>
<th>Name</th>
<th>Type</th>
<th>Inclusion</th>
<th>Description</th>
</tr>
<tr>
<td><code>module_id</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>The module ID, which includes either the module <a href="/operate/reference/naming-modules/#create-a-namespace-for-your-organization">namespace</a> or organization ID, followed by its name.
<div class="alert alert-caution" role="alert">
<h4 class="alert-heading">Caution</h4>

<p>The <code>module_id</code> uniquely identifies your module.
Do not change the <code>module_id</code>.</p>

</div>
</td>

</tr>
<tr>
<td><code>visibility</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>Whether the module is accessible only to members of your <a href="/manage/reference/organize/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can later make a private module public using the <code>viam module update</code> command. Once you make a module public, you can change it back to private if it is not configured on any machines outside of your organization.</td>
</tr>
<tr>
<td><code>url</code></td>
<td>string</td>
<td>Optional</td>
<td>The URL of the GitHub repository containing the source code of the module. Required for cloud build.</td>
</tr>
<tr>
<td><code>description</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>A description of your module and what it provides.</td>
</tr>
<tr>
<td><code>models</code></td>
<td>object</td>
<td><strong>Required</strong></td>
<td><p>A list of one or more {{< glossary_tooltip term_id="model" text="models" >}} provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair. If you are publishing a public module (<code>"visibility": "public"</code>), the namespace of your model must match the <a href="/operate/reference/naming-modules/#create-a-namespace-for-your-organization">namespace of your organization</a>.</p>
<p>You are strongly encouraged to include a <code>markdown_link</code> to the section of the README containing configuration information about each model, so that the section will be displayed alongside the configuration panel when configuring the model. For example, <code>"README.md#configure-your-meteo_pm-sensor"</code>. Please also include a <code>short_description</code> describing what hardware the model supports.</p></td>
</tr>
<tr>
<td><code>entrypoint</code></td>
<td>string</td>
<td><strong>Required</strong></td>
<td>The name of the file that starts your module program. This can be a compiled executable, a script, or an invocation of another program. If you are providing your module as a single file to the <code>upload</code> command, provide the path to that single file. If you are providing a directory containing your module to the <code>upload</code> command, provide the path to the entry point file contained within that directory.</td>
</tr>
<tr>
<td><code>build</code></td>
<td>object</td>
<td>Optional</td>
<td>An object containing the command to run to build your module, as well as optional fields for the path to your dependency setup script, the target architectures to build for, and the path to your built module. Use this with the <a href="/dev/tools/cli/#using-the-build-subcommand">Viam CLI's build subcommand</a>. </td>
</tr>
<tr>
<td><code>$schema</code></td>
<td>string</td>
<td>Optional</td>
<td>Enables VS Code hover and autocomplete as you edit your module code. Gets auto-generated when you run <code>viam module generate</code> or <code>viam module create</code>. Has no impact on the module's function.</td>
</tr>

</table>

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep number=4 %}}
**Package and upload**

To package (for Python) and upload your module and make it available to configure on machines in your organization (or in any organization, depending on how you set `visibility` in the <file>meta.json</file> file):

{{< tabs >}}
{{% tab name="Python: PyInstaller (recommended)" %}}

The recommended approach for Python is to use [PyInstaller](https://pypi.org/project/pyinstaller/) to compile your module into a packaged executable: a standalone file containing your program, the Python interpreter, and all of its dependencies.
When packaged in this fashion, you can run the resulting executable on your desired target platform or platforms without needing to install additional software or manage dependencies manually.

{{% alert title="Note" color="note" %}}
To follow these PyInstaller packaging steps, you must have enabled cloud build when moving through the module generator prompts.
If you did not, you will need to manually create a <file>build.sh</file> entrypoint script.
{{% /alert %}}

Edit your <file>meta.json</file> file back to its original state, reverting the edits you made for local testing purposes.
It should resemble the following:

```json {class="line-numbers linkable-line-numbers" data-start="13" data-line="1, 4, 6" }
 "entrypoint": "dist/main",
 "first_run": "",
 "build": {
   "build": "./build.sh",
   "setup": "./setup.sh",
   "path": "dist/archive.tar.gz",
   "arch": [
     "linux/amd64",
     "linux/arm64"
   ]
 }
```

Delete the <file>reload.sh</file> script since it was only meant for testing purposes.

Now you are ready to build and upload your module, either using Viam's cloud build tooling which is recommended for continuous integration, or a more manual process:

{{< tabs >}}
{{% tab name="PyInstaller cloud build (recommended)" %}}

We recommend you use PyInstaller with the [`build-action` GitHub action](https://github.com/viamrobotics/build-action) which provides a simple cross-platform build setup for multiple platforms: x86 and Arm Linux distributions, and MacOS.

The `viam module generate` command already generated the `build-action` file in your <file>.github/workflows</file> folder, so you just need to set up authentication in GitHub, and then create a new release to trigger the action:

1. In your terminal, run `viam organizations list` to view your organization ID.
1. Create an organization API key by running the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam organization api-key create --org-id YOUR_ORG_UUID --name descriptive-key-name
   ```

1. In the GitHub repo for your project, go to **Settings** &rarr; **Secrets and variables** &rarr; **Actions**.
   Create two new secrets using the **New repository secret** button:

   - `VIAM_KEY_ID` with the UUID from `Key ID:` in your terminal
   - `VIAM_KEY_VALUE` with the string from `Key Value:` in your terminal

1. From the main code page of your GitHub repo, find **Releases** in the right side menu and click **Create a new release**.
1. In the **Choose a tag** dropdown, create a new tag such as `1.0.0`.
   _Do not prepend the tag with `v` or the GH action will not trigger._
   For details about versioning, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

1. Click **Publish release**.
   The cloud build action will begin building the new module version for each architecture listed in your <file>meta.json</file>, and any machines configured to use the latest release of the module will receive the update once it has finished building.

See [Update an existing module using a GitHub action](/operate/get-started/other-hardware/manage-modules/#update-automatically) for more information.

{{% /tab %}}
{{% tab name="Manual PyInstaller build" %}}

From within the module directory, create a virtual Python environment with the necessary packages and then build an executable by running the setup and build scripts:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
sh build.sh
```

Run the `viam module upload` CLI command to upload the module to the registry, replacing `any` with one or more of `linux/any` or `darwin/any` if your module requires Linux OS-level support or macOS OS-level support, respectively.
If your module does not require OS-level support (such as platform-specific dependencies), you can run the following command exactly:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module upload --version 1.0.0 --platform any dist/archive.tar.gz
```

For details on platform support, see [Using the `--platform` argument](/dev/tools/cli/#using-the---platform-argument).

For details about versioning, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

{{% alert title="Important" color="note" %}}
The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}

PyInstaller does not support relative imports in entrypoints (imports starting with `.`).
If you get `"ImportError: attempted relative import with no known parent package"`, set up a stub entrypoint as described on [GitHub](https://github.com/pyinstaller/pyinstaller/issues/2560).

In addition, PyInstaller does not support cross-compiling: you must compile your module on the target architecture you wish to support.
For example, you cannot run a module on a Linux `arm64` system if you compiled it using PyInstaller on a Linux `amd64` system.
Viam makes this easy to manage by providing a build system for modules.
Follow [these instructions](/dev/tools/cli/#using-the-build-subcommand) to automatically build for each system your module can support using Viam's [CLI](/dev/tools/cli/).

{{% /alert %}}

{{% /tab %}}
{{% tab name="Python: venv" %}}

You can use the following package and upload method if you opted not to enable cloud build when you ran `viam module generate`.

1.  To package the module as an archive, run the following command from inside the module directory:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    tar -czf module.tar.gz run.sh setup.sh requirements.txt src
    ```

    where `run.sh` is your entrypoint file, `requirements.txt` is your pip dependency list file, and `src` is the directory that contains the source code of your module.

    This creates a tarball called <file>module.tar.gz</file>.

1.  Run the `viam module upload` CLI command to upload the module to the registry, replacing `any` with one or more of `linux/any` or `darwin/any` if your module requires Linux OS-level support or macOS OS-level support, respectively.
    If your module does not require OS-level support (such as platform-specific dependencies), you can run the following command exactly:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module upload --version 1.0.0 --platform any module.tar.gz
    ```

    For details on platform support, see [Using the `--platform` argument](/dev/tools/cli/#using-the---platform-argument).

    For details about versioning, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

{{% alert title="Important" color="note" %}}
The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.
{{% /alert %}}

{{% /tab %}}
{{% tab name="Go" %}}

From within your module's directory, run the `viam module upload` CLI command to upload the module to the registry, replacing `<platform>` with `linux/amd64`, `linux/arm64`, or one or more other [platforms depending on what your module requires](/dev/tools/cli/#using-the---platform-argument).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module upload --version 1.0.0 --platform <platform> .
```

For details about versioning, see [Module versioning](/operate/reference/module-configuration/#module-versioning).

{{% alert title="Important" color="note" %}}
The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

Now, if you look at the [Viam Registry page](https://app.viam.com/registry) while logged into your account, you'll be able to find your module listed.

{{% /tablestep %}}
{{< /table >}}

## Add your new modular resource to your machines

Now that your module is in the registry, you can configure the component you added on your machines just as you would configure other components and services; there's no more need for local module configuration.
The local module configuration is primarily for testing purposes.

Click the **+** button on your machine's **CONFIGURE** tab and search for your model.
For more details, see [Configure hardware on your machine](/operate/get-started/supported-hardware/#configure-hardware-on-your-machine).
