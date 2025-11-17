---
title: "Support additional hardware and software"
linkTitle: "Support hardware"
weight: 30
layout: "docs"
type: "docs"
icon: true
images: ["/registry/create-module.svg"]
description: "Add support for more physical or virtual hardware to the Viam ecosystem by creating a custom module."
date: "2025-10-30"
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
  - /how-tos/hello-world-module/
  - /operate/get-started/other-hardware/hello-world-module/
  - /operate/modules/create-module/hello-world-module/
  - /operate/modules/supported-hardware/hello-world-module/
---

If your physical or virtual hardware is not supported by an existing registry {{< glossary_tooltip term_id="module" text="module" >}}, you can create a new module to add support for it.

{{% hiddencontent %}}
If you want to create a "custom module", this page provides instructions for creating one in Python and Go.
{{% /hiddencontent %}}

This page provides instructions for creating a module in Python or Go.
For C++ module examples, see the [C++ examples directory on GitHub](https://github.com/viamrobotics/viam-cpp-sdk/tree/main/src/viam/examples/).
If you want to create a module for use with a microcontroller, see [Modules for ESP32](/operate/modules/advanced/micro-module/).

**Example module:** With each step of this guide, you have instructions for creating a {{< glossary_tooltip term_id="module" text="module" >}} which does two things:

1. Gets an image from a configured path on your machine
2. Returns a random number

## Prerequisites

{{< expand "Install the Viam CLI and authenticate" >}}
Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

{{% expand "A running machine connected to Viam" %}}

You can write a module without a machine, but to test your module you'll need a [machine](/operate/install/setup/).

{{% snippet "setup.md" %}}

{{% /expand%}}

{{< expand "For Python developers: Use Python 3.11+" >}}

If you plan to write your module using Python, you need Python 3.11 or newer installed on your computer to use the code generation tool in this guide.

You can check by running `python3 --version` or `python --version` in your terminal.

{{< /expand >}}

## Preparation

While not required, we recommend starting by writing a test script to check that you can connect to and control your hardware from your computer, perhaps using the manufacturer's API or other low-level code.

**Example module:** For the example module, the test script will open an image in the same directory and print a random number.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers" data-start="1" }
import random
from PIL import Image

# Open an image
img = Image.open("example.png")
img.show()

# Return a random number
random_number = random.random()
print(random_number)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers" data-start="1" }
package main

import (
  "fmt"
  "math/rand"
  "os"
)

func main() {
  // Open an image
  imgFile, err := os.Open("example.png")
  if err != nil {
    fmt.Printf("Error opening image file: %v\n", err)
    return
  }
  defer imgFile.Close()
  imgByte, err := os.ReadFile("example.png")
  fmt.Printf("Image file type: %T\n", imgByte)
  if err != nil {
    fmt.Printf("Error reading image file: %v\n", err)
    return
  }

  // Return a random number
  number := rand.Float64()
  fmt.Printf("Random number: %f\n", number)
}
```

{{% /tab %}}
{{< /tabs >}}

## Choose an API

You can think of a module as a packaged wrapper around a script.
The module takes the functionality of the script and maps it to a standardized API for use within the Viam ecosystem.

Review the available [component APIs](/dev/reference/apis/#component-apis) and choose the one whose methods map most closely to the functionality you need.

If you need a method that is not in your chosen API, you can use the flexible `DoCommand` (which is built into all component APIs) to create custom commands.
See [Run control logic](/operate/modules/control-logic/) for more information.

**Example module:** To choose the Viam [APIs](/dev/reference/apis/#component-apis) that make sense for your module, think about the functionality you want to implement.
You need a way to return an image and you need a way to return a number.

If you look at the [camera API](/dev/reference/apis/components/camera/), you can see the `GetImage` method, which returns an image.
That will work for the image.

The camera API also has a few other methods.
You do not need to fully implement all the methods of an API.
For example, this camera does not use point cloud data, so for methods like `GetPointCloud` it will return an "unimplemented" error.

The [sensor API](/dev/reference/apis/components/sensor/) includes the `GetReadings` method.
You can return the random number with that.

Note that the camera API can't return a number and the sensor API can't return an image.
Each model can implement only one API, but your module can contain multiple modular resources.
Therefore it is best to make two modular resources: a camera to return the image and a sensor to return a random number.

## Write your module

### Generate stub files

Use the [Viam CLI](/dev/tools/cli/) to generate template files for your module.
You can work on the code for your module either on the device where you are running `viam-server` or on another computer.

{{< table >}}
{{% tablestep start=1 %}}

Run the `module generate` command in your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate
```

{{< expand "Click for more details about each prompt" >}}

<!--prettier-ignore-->
| Prompt | Description |
| -------| ----------- |
| Module name | Choose a name that describes the set of {{< glossary_tooltip term_id="resource" text="resources" >}} it supports. |
| Language | Choose the programming language for the module. The CLI supports `Python` and `Golang`. |
| Visibility | Choose `Private` to share only with your organization, or `Public` to share publicly with all organizations. If you are testing, choose `Private`. |
| Namespace/Organization ID | Navigate to your organization settings through the menu in the upper-right corner of the page. Find the **Public namespace** (or create one if you haven't already) and copy that string. If you use the organization ID, you must still create a public namespace first if you wish to share the module publicly. |
| Resource to add to the module (API) | The [component API](/dev/reference/apis/#component-apis) your module will implement. See [Choose an API](#choose-an-api) for more information. |
| Model name | Name your component model based on what it supports, for example, if it supports a model of ultrasonic sensor called "XYZ Sensor 1234" you could call your model `xyz_1234` or similar. Must be all-lowercase and use only alphanumeric characters (`a-z` and `0-9`), hyphens (`-`), and underscores (`_`). |
| Enable cloud build | If you select `Yes` (recommended) and push the generated files (including the <file>.github</file> folder) and create a release of the format `X.X.X`, the module will build for [all architectures specified in the meta.json build file](/operate/modules/advanced/metajson/). You can select `No` if you want to always build the module yourself before uploading it. For more information see [Update and manage modules](/operate/modules/advanced/manage-modules/). |
| Register module | Select `Yes` unless you are creating a local-only module for testing purposes and do not intend to upload it. Registering a module makes its name and metadata appear in the registry; uploading the actual code that powers the module is a separate step. If you decline to register the module at this point, you can run [`viam module create`](/dev/tools/cli/#module) to register it later. |

{{% /expand %}}

<br>

**Example module**: To build an example module that contains a camera model, use the following command:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language python --model-name hello-camera \
  --name hello-world --resource-subtype=camera --public false \
  --enable-cloud true
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language go --model-name hello-camera \
  --name hello-world --resource-subtype=camera --public false \
  --enable-cloud true
```

{{% /tab %}}
{{< /tabs >}}

The CLI only supports generating code for one model at a time.
You can add the model for the sensor in a later step in [Creating multiple models within one module](/operate/modules/support-hardware/#creating-multiple-models-within-one-module).

{{% /tablestep %}}
{{% tablestep %}}

The generator creates a directory containing stub files for your modular component.
In the next section, you'll customize some of the generated files to support your camera.

**Example module**: For the example module, the file structure is:

{{< tabs >}}
{{% tab name="Python" %}}

```treeview
hello-world/
└── src/
|   ├── models/
|   |   └── hello_camera.py
|   └── main.py
└── README.md
└── build.sh
└── meta.json
└── requirements.txt
└── run.sh
└── setup.sh
```

If you want to understand the module structure, here's what each file does:

- **<FILE>README.md</FILE>**: Documentation template that gets uploaded to the registry when you upload the module.
- **<FILE>meta.json</FILE>**: Module metadata that gets uploaded to the registry when you upload the module.
- **<FILE>main.py</FILE>** and **<FILE>hello_camera.py</FILE>**: Core code that registers the module and resource and provides the model implementation.
- **<FILE>setup.sh</FILE>** and **<FILE>requirements.txt</FILE>**: Setup script that creates a virtual environment and installs the dependencies listed in <FILE>requirements.txt</FILE>.
- **<FILE>build.sh</FILE>**: Build script that packages the code for upload.
- **<FILE>run.sh</FILE>**: Script that runs <FILE>setup.sh</FILE> and then executes the module from <FILE>main.py</FILE>.

{{% /tab %}}
{{% tab name="Go" %}}

```treeview
hello-world/
└── cmd/
|   ├── cli/
|   |   └── main.go
|   └── module/
|       └── main.go
└── Makefile
└── README.md
└── go.mod
└── module.go
└── meta.json
```

If you want to understand the module structure, here's what each file does:

- **<FILE>README.md</FILE>**: Documentation template that gets uploaded to the registry when you upload the module.
- **<FILE>meta.json</FILE>**: Module metadata that gets uploaded to the registry when you upload the module.
- **<FILE>module/main.go</FILE> and <FILE>module.go</FILE>**: Core code that registers the module and resource and provides the model implementation.
- **<FILE>cli/main.go</FILE>**: You can run this file to test the model you are creating (`go run ./cmd/cli`).
- **Makefile**: Build and setup commands.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

### Creating multiple models within one module

Some of the code you generated for your first modular resource is shared across the module no matter how many modular resource models it supports.
Some of the code you generated is resource-specific.

If you have multiple modular resources that are related, you can put them all into the same module.

For convenience, we recommend running the module generator again from within the first module's directory, generating an unregistered module, and copying the resource-specific code from it.

**Example module**: Change directory into the first module's directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cd hello-world
```

Run the following command from within the first module's directory to generate temporary code you can copy from.
Do not register this module.

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language python --model-name hello-sensor \
  --name hello-world --resource-subtype=sensor --public false \
  --enable-cloud true
```

Click on each tab to see how the file should change to add the sensor-specific code:

{{< tabs >}}
{{% tab name="hello_sensor.py" %}}

Move the generated <file>hello-world/hello-world/src/models/hello_sensor.py</file> file to <file>hello-world/src/models/</file>.

{{% /tab %}}
{{% tab name="main.py" %}}

Open the <file>hello-world/src/main.py</file> file and add `HelloSensor` to the list of imports so you have:

```python {class="line-numbers linkable-line-numbers" data-line="6, 9"}
import asyncio

from viam.module.module import Module
try:
    from models.hello_camera import HelloCamera
    from models.hello_sensor import HelloSensor
except ModuleNotFoundError:  # when running as local module with run.sh
    from .models.hello_camera import HelloCamera
    from .models.hello_sensor import HelloSensor

if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
```

Save the file.

{{% /tab %}}
{{% tab name="meta.json" %}}

Open <file>hello-world/meta.json</file> and add the sensor model into the model list.
Edit the `description` to include both models.

```json {class="line-numbers linkable-line-numbers" data-line="6,13-19"}
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "exampleorg:hello-world",
  "visibility": "private",
  "url": "",
  "description": "Example camera and sensor components: hello-camera and hello-sensor",
  "models": [
    {
      "api": "rdk:component:camera",
      "model": "exampleorg:hello-world:hello-camera",
      "short_description": "A camera that returns an image.",
      "markdown_link": "README.md#model-exampleorghello-worldhello-camera"
    },
    {
      "api": "rdk:component:sensor",
      "model": "exampleorg:hello-world:hello-sensor",
      "short_description": "A sensor that returns a random number.",
      "markdown_link": "README.md#model-exampleorghello-worldhello-sensor"
    }
  ],
  "applications": null,
  "markdown_link": "README.md",
  "entrypoint": "./run.sh",
  "first_run": "",
  "build": {
    "build": "./build.sh",
    "setup": "./setup.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64", "darwin/arm64", "windows/amd64"]
  }
}
```

Save the file.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language go --model-name hello-sensor \
  --name hello-world --resource-subtype=sensor --public false \
  --enable-cloud true
```

Click on each tab to see how the file should change to add the sensor-specific code:

{{< tabs >}}
{{% tab name="hello-camera.go" %}}

In the initial module, change the name of <file>hello-world/module.go</file> to <file>hello-camera.go</file>.

{{% /tab %}}
{{% tab name="hello-sensor.go" %}}

Move and rename <file>hello-world/hello-world/module.go</file> to <file>hello-world/hello-sensor.go</file>.

{{% /tab %}}
{{% tab name="module/main.go" %}}

Open <file>hello-world/cmd/module/main.go</file>.
This file must add resource imports and register the module's models:

```go {class="line-numbers linkable-line-numbers" data-start="1" data-line="8, 13-16"}
package main

import (
    "helloworld"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
    camera "go.viam.com/rdk/components/camera"
    sensor "go.viam.com/rdk/components/sensor"
)

func main() {
    // ModularMain can take multiple APIModel arguments, if your module implements multiple models.
    module.ModularMain(
      resource.APIModel{ camera.API, helloworld.HelloCamera},
      resource.APIModel{ sensor.API, helloworld.HelloSensor},
    )
}
```

Save the file.

{{% /tab %}}
{{% tab name="meta.json" %}}

Open <file>hello-world/meta.json</file> and add the sensor model into the model list.
Edit the `description` to include both models.

```json {class="line-numbers linkable-line-numbers" data-line="6,13-19"}
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "exampleorg:hello-world",
  "visibility": "private",
  "url": "",
  "description": "Example camera and sensor components: hello-camera and hello-sensor",
  "models": [
    {
      "api": "rdk:component:camera",
      "model": "exampleorg:hello-world:hello-camera",
      "short_description": "A camera that returns an image.",
      "markdown_link": "README.md#model-exampleorghello-worldhello-camera"
    },
    {
      "api": "rdk:component:sensor",
      "model": "exampleorg:hello-world:hello-sensor",
      "short_description": "A sensor that returns a random number.",
      "markdown_link": "README.md#model-exampleorghello-worldhello-sensor"
    }
  ],
  "applications": null,
  "markdown_link": "README.md",
  "entrypoint": "bin/hello-world",
  "first_run": "",
  "build": {
    "build": "make module.tar.gz",
    "setup": "make setup",
    "path": "module.tar.gz",
    "arch": ["linux/amd64", "linux/arm64", "darwin/arm64", "windows/amd64"]
  }
}
```

Save the file.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

You can now delete the temporary <file>hello-world/hello-world</file> directory and all its contents.

### Implement the components

At this point you have a template for your module.

If you want to see example modules, check out the Viam Registry.
Many modules have a linked GitHub repo, where you can see the module's code.
When logged in, you can also download the module's source code to inspect it.

{{< tabs >}}
{{% tab name="Python" %}}

Generally you will add your custom logic in these files:

<!-- prettier-ignore -->
| File | Description |
| ---- | ----------- |
| <file>/src/models/&lt;model-name&gt;.py</file> | Set up the configuration options for the model and implement the API methods for the model.      |
| `setup.sh` and `run.sh`                        | Add any logic for installing or running other software for your module.                          |
| `requirements.txt`                             | Add any Python packages that are required for your module. They will be installed by `setup.sh`. |

<br>

{{% /tab %}}
{{% tab name="Go" %}}

Generally you will add your custom logic in these files:

<!-- prettier-ignore -->
| File | Description |
| ---- | ----------- |
| Model file (for example `hello-camera.go`) | Implement the API methods for the model. |

{{% /tab %}}
{{< /tabs >}}

**Example module**: You can view complete example code in the [hello-world-module repository on GitHub](https://github.com/viam-labs/hello-world-module/tree/main).

#### Set up model configuration options

Many resource models have configuration options that allow you to specify options such as:

- A file path from which to access data
- A pin to which a device is wired
- An optional signal frequency to override a default value
- The name of _another_ resource you wish to use in the model

Model configuration happens in two steps:

{{< table >}}
{{% tablestep start=1 %}}
**Validation**

The validation step serves two purposes:

- Confirm that the model configuration contains all **required attributes** and that these attributes are of the right type.
- Identify and return a list of names of **required resources** and a list of names of **optional resources**.
  `viam-server` will pass these resources to the next step as dependencies.
  For more information, see [Module dependencies](/operate/modules/advanced/dependencies/).

**Example module**: Imagine how a user might configure the finished camera model.
Since the camera model returns an image at a provided path, the configuration must contain a variable to pass in the file path.

```json
{
  "image_path": "/path/to/file"
}
```

{{< tabs >}}
{{% tab name="Python" %}}

In <file>/src/models/&lt;model-name&gt;.py</file>, edit the `validate_config` function to:

```python {class="line-numbers linkable-line-numbers" data-start="38" data-line="5-10" }
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        # Check that a path to get an image was configured
        fields = config.attributes.fields
        if "image_path" not in fields:
            raise Exception("Missing image_path attribute.")
        elif not fields["image_path"].HasField("string_value"):
            raise Exception("image_path must be a string.")

        return [], []
```

{{% /tab %}}
{{% tab name="Go" %}}

In <file>hello-world/hello-camera.go</file> edit the `Validate` function to:

```go {class="line-numbers linkable-line-numbers" data-start="51" data-line="2-10" }
func (cfg *Config) Validate(path string) ([]string, []string, error) {
    var deps []string
    if cfg.ImagePath == "" {
        return nil, nil, resource.NewConfigValidationFieldRequiredError(path, "image_path")
    }
    if reflect.TypeOf(cfg.ImagePath).Kind() != reflect.String {
        return nil, nil, errors.New("image_path must be a string.")
    }
    imagePath = cfg.ImagePath
    return deps, []string{}, nil
}
```

Add the following import at the top of <file>hello-world/hello-camera.go</file>:

```go {class="line-numbers linkable-line-numbers" data-start="7"}
"reflect"
```

{{% /tab %}}
{{< /tabs >}}

For the sensor model, you do not need to edit any of the validation or configuration methods because the sensor has no configurable attributes.

{{% /tablestep %}}
{{% tablestep %}}
**Reconfiguration**

`viam-server` calls the `reconfigure` method when the user adds the model or changes its configuration.

The reconfiguration step serves two purposes:

- Use the configuration attributes and dependencies to set attributes on the model for usage within the API methods.
- Obtain access to dependencies.
  For information on how to use dependencies, see [Module dependencies](/operate/modules/advanced/dependencies/).

**Example module**: For the camera model, the reconfigure method serves to set the image path for use in API methods.

{{< tabs >}}
{{% tab name="Python" %}}

1. Open <file>/src/models/hello_camera.py</file>.

2. Edit the `reconfigure` function to:

   ```python {class="line-numbers" data-start="51" data-line="4-5"}
       def reconfigure(
           self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
       ):
           attrs = struct_to_dict(config.attributes)
           self.image_path = str(attrs.get("image_path"))

           return super().reconfigure(config, dependencies)
   ```

3. Add the following import to the top of the file:

   ```python {class="line-numbers" data-start="1"}
   from viam.utils import struct_to_dict
   ```

{{% /tab %}}
{{% tab name="Go" %}}

1. Open <file>hello-world/hello-camera.go</file>.

1. Add `imagePath = ""` to the global variables so you have the following:

   ```go {class="line-numbers linkable-line-numbers" data-line="22" data-start="18" data-line-offset="19"}
   var (
       HelloCamera      = resource.NewModel("exampleorg", "hello-world", "hello-camera")
       errUnimplemented = errors.New("unimplemented")
       imagePath        = ""
   )
   ```

1. Edit the `type Config struct` definition, replacing the comments with the following:

   ```go {class="line-numbers" data-start="32"}
   type Config struct {
       resource.AlwaysRebuild
       ImagePath string `json:"image_path"`
   }
   ```

   This adds the `image_path` attribute and causes the resource to rebuild each time the configuration is changed.

{{< expand "Need to maintain state? Click here." >}}
The `resource.AlwaysRebuild` parameter in the `Config` struct causes `viam-server` to fully rebuild the resource each time the user changes the configuration.

If you need to maintain the state of the resource, for example if you are implementing a board and need to keep the software PWM loops running, you can implement this function so `viam-server` updates the configuration without rebuilding the resource from scratch.
In this case, your `Reconfigure` function should do the following:

- If you assigned any configuration attributes to global variables, get the values from the latest `config` object and update the values of the global variables.
- Assign default values as necessary to any optional attributes if the user hasn't configured them.

If you create a `Reconfigure` function, you must also edit the constructor to explicitly call `Reconfigure`.

For an example that implements the `Reconfigure` method, see [<file>mybase.go</file> on GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go).

{{< /expand >}}

{{% hiddencontent %}}
`resource.AlwaysRebuild` provides an implementation of `Reconfigure` that returns a `NewMustRebuild` error.
This error doesn't exist in the other SDKs, so `AlwaysRebuild` is not supported in those SDKs.
{{% /hiddencontent %}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

#### Implement API methods

Depending on the component API you are implementing, you can implement different API methods.

{{< tabs >}}
{{% tab name="Python" %}}

For each API method you want to implement, replace the body of the method with your relevant logic.
Make sure you return the correct type in accordance with the function's return signature.
You can find details about the return types at [python.viam.dev](https://python.viam.dev/autoapi/viam/components/index.html).

**Example module:** Implement the camera API and the sensor API:

{{< table >}}
{{< tablestep start=1 >}}

The module generator created a stub for the `get_images()` function we want to implement in <file>hello-world/src/models/hello_camera.py</file>.

You need to replace `raise NotImplementedError()` with code to implement the method:

```python {class="line-numbers linkable-line-numbers" data-start="74" data-line="9-13" }
    async def get_images(
        self,
        *,
        filter_source_names: Optional[Sequence[str]] = None,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Tuple[Sequence[NamedImage], ResponseMetadata]:
        img = Image.open(self.image_path)
        vi_img = pil_to_viam_image(img, CameraMimeType.JPEG)
        named = NamedImage("default", vi_img.data, vi_img.mime_type)
        metadata = ResponseMetadata()
        return [named], metadata
```

Add the following import to the top of the file:

```python {class="line-numbers" data-start="1"}
from viam.media.utils.pil import pil_to_viam_image
from viam.media.video import CameraMimeType
from PIL import Image
```

Save the file.

{{% /tablestep %}}
{{< tablestep >}}

Leave the rest of the camera API methods unimplemented.
They do not apply to this camera.

{{% /tablestep %}}
{{< tablestep >}}

Open <file>requirements.txt</file>.
Add the following line:

```text
Pillow
```

{{% /tablestep %}}
{{< tablestep >}}

Next, implement the sensor API.
The module generator created a stub for the `get_readings()` function we want to implement in <file>hello-world/src/models/hello_sensor.py</file>.

Replace `raise NotImplementedError()` with code to implement the method:

```python {class="line-numbers linkable-line-numbers" data-start="63" data-line="8-11" }
    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        number = random.random()
        return {
            "random_number": number
        }
```

Add the following import to the top of the file:

```python {class="line-numbers" data-start="1"}
import random
```

Save the file.

{{% /tablestep %}}
{{< tablestep >}}

Leave the rest of the sensor API methods unimplemented.

{{% /tablestep %}}
{{< /table >}}

{{% hiddencontent %}}

You may see examples in registry modules that use a different pattern from what the generator creates.
For example, some older example modules define `async def main()` inside <file>main.py</file>.
We recommend using the pattern the generator follows:

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from viam.module.module import Module
try:
    from models.hello_camera import HelloCamera
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.hello_camera import HelloCamera

if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
```

A previous version of the CLI module generator created `__init__.py` files, but now uses a different module structure.
We recommend using what the current generator creates rather than old examples that use `__init__.py` files.

{{% /hiddencontent %}}

{{% /tab %}}
{{% tab name="Go" %}}

For each API method you want to implement, replace the body of the method with your relevant logic.
Make sure you return the correct type in accordance with the function's return signature.
You can find details about the return types at [go.viam.com/rdk/components](https://pkg.go.dev/go.viam.com/rdk/components).

**Example module:** Implement the camera API and the sensor API:

{{< table >}}
{{< tablestep start=1 >}}

The module generator created a stub for the `Images` function we want to implement in <file>hello-world/hello-camera.go</file>.

You need to replace `panic("not implemented")` with code to implement the method:

```go {class="line-numbers linkable-line-numbers" data-start="111" }
func (s *helloWorldHelloCamera) Images(ctx context.Context, filterSourceNames []string, extra map[string]interface{}) ([]camera.NamedImage, resource.ResponseMetadata, error) {
    var responseMetadataRetVal resource.ResponseMetadata

    imgFile, err := os.Open(imagePath)
    if err != nil {
        return nil, responseMetadataRetVal, errors.New("Error opening image.")
    }
    defer imgFile.Close()

    imgByte, err := os.ReadFile(imagePath)
    if err != nil {
        return nil, responseMetadataRetVal, err
    }

    named, err := camera.NamedImageFromBytes(imgByte, "default", "image/png")
    if err != nil {
        return nil, responseMetadataRetVal, err
    }

    return []camera.NamedImage{named}, responseMetadataRetVal, nil
}
```

{{% /tablestep %}}
{{% tablestep %}}

Add the following import at the top of <file>hello-world/hello-camera.go</file>:

```go {class="line-numbers linkable-line-numbers" data-start="7"}
"os"
```

Save the file.

{{% /tablestep %}}
{{< tablestep >}}

Leave the rest of the camera API methods unimplemented.
They do not apply to this camera.

{{% /tablestep %}}
{{< tablestep >}}

Next, implement the sensor API.
The module generator created a stub for the `Readings()` function we want to implement in <file>hello-world/hello-sensor.go</file>.

Replace `panic("not implemented")` with code to implement the method:

```go {class="line-numbers linkable-line-numbers" data-start="92" data-line="8-11" }
func (s *helloWorldHelloSensor) Readings(ctx context.Context, extra map[string]interface{}) (map[string]interface{}, error) {
    number := rand.Float64()
    return map[string]interface{}{
        "random_number": number,
    }, nil
}
```

{{% /tablestep %}}
{{< tablestep >}}

Add the following import to the list of imports at the top of <file>hello-world/hello-sensor.go</file>:

```go {class="line-numbers linkable-line-numbers" data-start="7"}
"math/rand"
```

{{% /tablestep %}}
{{< tablestep >}}

Since `errUnimplemented` and `Config` are defined in <file>hello-camera.go</file>, you need to change <file>hello-sensor.go</file> to avoid redeclaring them:<br><br>

In <file>hello-sensor.go</file>:

- Delete the `"errors"` import.
- Search for and delete the line `errUnimplemented = errors.New("unimplemented")`.
- Search for `type Config struct {` and change it to `type sensorConfig struct {`.
- Search for all instances of `*Config` in <file>hello-sensor.go</file> and change them to `*sensorConfig`.

{{% /tablestep %}}
{{< tablestep >}}

Leave the rest of the sensor API methods unimplemented.

Save the file.

{{% /tablestep %}}

{{< /table >}}

{{% /tab %}}
{{< /tabs >}}

## Test your module locally

You can test your module locally before uploading it to the [registry](https://app.viam.com/registry).
You can configure it in the web UI using the local files on your machine.

### Add module to machine

To get your module onto your machine, hot reloading builds and packages it and then uses the shell service to copy it to the machine for testing.
If you are using a Python virtual environment (venv), make sure your module files are on the same device where `viam-server` is running, and add the module manually instead.

{{% hiddencontent %}}
Hot reloading is the preferred solution for cross-compilation. We recommend using hot reloading rather than cross-compilation tools like Canon.
{{% /hiddencontent %}}

{{< tabs >}}
{{% tab name="Hot reloading (recommended)" %}}

Run the following command to build the module and add it to your machine:

{{< tabs >}}
{{% tab name="Same device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload-local --cloud-config /path/to/viam.json
```

{{% /tab %}}
{{% tab name="Other device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id 123abc45-1234-432c-aabc-z1y111x23a00
```

{{% /tab %}}
{{< /tabs >}}

For more information, see the [`viam module` documentation](/dev/tools/cli/#module).

{{< expand "Reload troubleshooting" >}}

- `Error: Could not connect to machine part: context deadline exceeded; context deadline exceeded; mDNS query failed to find a candidate`

  Try specifying the `--part-id`, which you can find by clicking the **Live** indicator on your machine's page and clicking **Part ID**.

- `Error: Rpc error: code = Unknown desc = stat /root/.viam/packages-local: no such file or directory`

  Try specifying the `--home` directory, for example `/Users/yourname/` on macOS.

- `Error: Error while refreshing token, logging out. Please log in again`

  Run `viam login` to reauthenticate the CLI.

### Try using a different command

If you are still having problems with the `reload` command, you can use a different, slower method of rebuilding and then restarting the module.
Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it on your machine's **CONFIGURE** tab.
In the upper-right corner of the module's card, click the **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="width:300px" class="shadow" >}}

{{< /expand >}}

{{< alert title="Refresh" color="note" >}}

You may need to refresh your machine page for your module to show up.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Manual (required for Python venv)" %}}

Navigate to your machine's **CONFIGURE** page.

{{< tabs >}}
{{% tab name="Python" %}}

Click the **+** button, select **Local module**, then again select **Local module**.

Enter the path to the automatically-generated <file>run.sh</file> script.
Click **Create**.
For local modules, `viam-server` uses this path to start the module.

**Example module**:
For the `hello-world` module, the path should resemble `/home/yourname/hello-world/run.sh` on Linux, or `/Users/yourname/hello-world/run.sh` on macOS.

Save the config.

{{% /tab %}}
{{% tab name="Go" %}}

From within the module directory, compile your module [with the `module build` command](/dev/tools/cli/#using-the-build-subcommand) into a single executable:

```sh {class="command-line" data-prompt="$" data-output="5-10"}
viam module build local
```

Click the **+** button, select **Local module**, then again select **Local module**.

Enter the path to the <file>/bin/&#60;module-name&#62;</file> executable.
For local modules, `viam-server` uses this path to start the module.

**Example module**:
For the `hello-world` module, the path should resemble `/home/yourname/hello-world/bin/hello-world`.

Click **Create**.

Save the config.

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

{{< table >}}
{{< /table >}}

### Add local model

{{< table >}}
{{% tablestep start=1 %}}
**Configure the model provided by your module**

On your machine's **CONFIGURE** page, click **+**, click **Local module**, then click **Local component** or **Local service**.

Select or enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, for example `exampleorg:hello-world:hello-camera`.
You can find the triplet in the `model` field of your <file>meta.json</file> file.

Select the **Type** corresponding to the API you implemented.

Enter a **Name** such as `camera-1`.
Click **Create**.

{{% /tablestep %}}
{{% tablestep %}}
**Configure attributes**

When you add a new component or service, a panel appears for it on the **CONFIGURE** tab.
If your model has required or optional attributes, configure them in the configuration field by adding them inside the `{}` object.

**Example module**: For the camera model, add the `image_path` attribute by replacing `{}` with:

```json {class="line-numbers linkable-line-numbers"}
{
  "image_path": "<replace with the path to your image>"
}
```

{{% /tablestep %}}
{{% tablestep %}}
Save the config and wait a few seconds for it to apply.

Then click the **TEST** section of the camera's configuration card.
If there are errors you will see them on the configuration panel and on the **LOGS** tab.

{{% /tablestep %}}
{{% tablestep %}}
**Test the component**

Click the **TEST** bar at the bottom of your modular component configuration, and check whether it works as expected.

**Example module**: For the camera model, the test panel should show the image:

{{<imgproc src="/how-tos/hello-camera.png" resize="x1100" declaredimensions=true alt="The configuration interface with the Test section of the camera card open, showing a hello world image." style="width:800px" class="shadow aligncenter" >}}

If you also implemented the sensor model, add and test it the same way.

{{% /tablestep %}}
{{% tablestep %}}
**Iterate**

If your component works, you're almost ready to share your module by uploading it to the registry.

Each time you make changes to the local module code, you must update the module on the machine:

{{< tabs >}}
{{% tab name="Hot reloading (recommended)" %}}

Run the reload command again to rebuild and restart your module:

{{< tabs >}}
{{% tab name="Same device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload-local --cloud-config /path/to/viam.json
```

{{% /tab %}}
{{% tab name="Other device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id 123abc45-1234-432c-aabc-z1y111x23a00
```

{{% /tab %}}
{{< /tabs >}}

Your machine may already have a previously published version of the module you are iterating on in its configuration.
If so you can toggle **Hot Reloading** on and off in the Viam web UI.
When toggled on, the machine uses the module that you are developing.
When toggled off, the machine uses the configured registry version.

{{% /tab %}}
{{% tab name="Manual (required for Python venv)" %}}

{{< tabs >}}
{{% tab name="Python" %}}

As you iterate, save the code changes, then restart the module in your machine's **CONFIGURE** tab:
In the upper-right corner of the module's card, click **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="width:300px" class="shadow" >}}

{{% /tab %}}
{{% tab name="Go" %}}

Run the following command to rebuild your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module build local
```

Then restart it in your machine's **CONFIGURE** tab.
In the upper-right corner of the module's card, click **...** menu, then click **Restart**.

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="max-width:300px" class="shadow" >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}

{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

## Next steps

Once you have thoroughly tested your module, continue to [package and deploy](/operate/modules/deploy-module/) it.
