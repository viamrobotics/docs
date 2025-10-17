---
title: "Create a Hello World module"
linkTitle: "Hello World module"
type: "docs"
weight: 30
images: ["/registry/module-puzzle-piece.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Get started writing your own modular resources by creating a Hello World module that provides an example camera and sensor."
languages: ["python", "go"]
viamresources: ["components", "sensor", "camera"]
platformarea: ["registry"]
level: "Beginner"
date: "2024-10-22"
aliases:
  - /how-tos/hello-world-module/
  - /operate/get-started/other-hardware/hello-world-module/
  - /operate/modules/create-module/hello-world-module/
# updated: ""  # When the tutorial was last entirely checked
# Python checked/updated: 2025-02-25
cost: "0"
---

## What this guide covers

This guide walks you through creating a {{< glossary_tooltip term_id="modular-resource" text="modular" >}} camera component that returns a configured image.
This guide also includes optional steps to create a modular sensor that returns random numbers, to demonstrate how you can include two modular resources within one {{< glossary_tooltip term_id="module" text="module" >}}.
By the end, you will know how to create your own modular resources and package them into modules so you can use them on your machines.

{{% alert title="Note" color="note" %}}

This guide provides a basic learning example.
For a more comprehensive guide including usage of cloud build tools for deployment across different platforms, see [Create a module](/operate/modules/create-module/).

{{% /alert %}}

## Prerequisites

{{< expand "Install the Viam CLI and authenticate" >}}
Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

{{% expand "Install viam-server on your computer and connect to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand%}}
{{< expand "For Python users: Make sure you have at least Python 3.11" >}}

If you plan to write your module using Python, you need Python version 3.11 or newer installed on your computer to use the code generation tool in this guide.
You can check by running `python3 --version` or `python --version` in your terminal.

{{< /expand >}}

## Decide what your module will do

The functionality you want to add to your machine determines the APIs you need to implement, so let's start by deciding what your module will do.
For the purposes of this guide, you're going to make a module that does two things:

- Opens an image file from a configured path on your machine
- Returns a random number

## Choose an API to implement

Let's figure out which Viam [APIs](/dev/reference/apis/#component-apis) make sense for your module.
You need a way to return an image, and you need a way to return a number.

If you look at the [camera API](/dev/reference/apis/components/camera/), you can see the `GetImage` method, which returns an image.
That will work for the image.
None of the camera API methods return a number though.

Look at the [sensor API](/dev/reference/apis/components/sensor/), which includes the `GetReadings` method.
You can return a number with that, but the sensor API can't return an image.

Each model can implement only one API, but your module can contain multiple modular resources.
Let's make two modular resources: a camera to return the image, and a sensor to return a random number.

{{% alert title="Note" color="note" %}}

For a quicker hello world experience, you can skip the sensor and only create a camera modular resource.
If you prefer the simpler path, skip the sensor sections in the steps below.

{{% /alert %}}

## Generate stub files

The easiest way to generate the files for your module is to use the [Viam CLI](/dev/tools/cli/).

{{% alert title="Note" color="note" %}}
The steps below suggest that you disable cloud build when generating your stub files, for simplicity of local testing.
If you plan to publish your module to the Viam registry, we recommend enabling cloud build, and then following the testing, packaging and uploading steps in [Create a module](/operate/modules/create-module/) once you are done writing your API implementation in this guide.
Enabling cloud build will set up your module for a more automated deployment process if you plan to use your module for more than just learning.
{{% /alert %}}

### Generate the camera files

The CLI module generator generates the files for one modular resource at a time.
First let's generate the camera component files, and we'll add the sensor code later.

1.  Run the `module generate` command in your terminal:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module generate
    ```

1.  Follow the prompts, selecting the following options:

    - Module name: `hello-world`
    - Language: Your choice
    - Visibility: `Private`
    - Namespace/Organization ID:
      - Navigate to your organization settings through the menu in upper right corner of the page.
        Find the **Public namespace** (or create one if you haven't already) and copy that string.
        In the example snippets below, the namespace is `jessamy`.
    - Resource to add to the module (API): `Camera Component`.
      We will add the sensor later.
    - Model name: `hello-camera`
    - Enable cloud build: `No`
    - Register module: `Yes`

1.  Hit your Enter key and the generator will generate a folder called <file>hello-world</file> containing stub files for your modular camera component.

### Generate the sensor code

{{< expand "Click if you are also creating a sensor component" >}}

Some of the code you just generated is shared across the module no matter how many modular resource models it supports.
Some of the code you generated is camera-specific.
You need to add some sensor-specific code to support the sensor component.

1.  Instead of writing the code manually, use the module generator again.

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module generate
    ```

1.  You're going to delete this module after copy-pasting the sensor-specific code from it.
    The only things that matter are the API and the model name.

    - Module name: `temporary`
    - Language: Your choice
    - Visibility: `Private`
    - Namespace/Organization ID: Same as you used before.
    - Resource to add to the module (API): `Sensor Component`.
    - Model name: `hello-sensor`
    - Enable cloud build: `No`
    - Register module: `No`

{{< tabs >}}
{{% tab name="Python" %}}

3.  Move the <file>temporary/src/models/hello_sensor.py</file> file to <file>hello-world/src/models/</file>.<br><br>

1.  In <file>hello-world/src/models/hello_sensor.py</file>, change `temporary` to `hello-world` in the ModelFamily line, so you have, for example:

    ```python {class="line-numbers linkable-line-numbers" data-start="15" }
    MODEL: ClassVar[Model] = Model(ModelFamily("jessamy", "hello-world"), "hello-sensor")
    ```

    Save the file.<br><br>

1.  Open the <file>hello-world/src/main.py</file> file and add `HelloSensor` to the list of imports so you have:

    ```python {class="line-numbers linkable-line-numbers" data-line="6, 9"}
    import asyncio

    from viam.module.module import Module
    try:
        from models.hello_camera import HelloCamera
        from models.hello_sensor import HelloSensor
    except ModuleNotFoundError: # when running as local module with run.sh
        from .models.hello_camera import HelloCamera
        from .models.hello_sensor import HelloSensor

    if __name__ == '__main__':
        asyncio.run(Module.run_from_registry())

    ```

    Save the file.

{{% /tab %}}
{{% tab name="Go" %}}

3. Edit the file structure:<br><br>

   1. Change the name of <file>hello-world/module.go</file> to <file>hello-camera.go</file>.<br><br>

   1. Change the name of <file>temporary/module.go</file> to <file>hello-sensor.go</file>.
      Move the <file>hello-sensor.go</file> folder from <file>temporary/</file> to <file>/hello-world/</file>.<br><br>

1. Open <file>hello-world/cmd/module/main.go</file>.
   You need to add the necessary imports and define how it adds the sensor model from the registry.
   Delete all the contents and replace them with the following:<br><br>

   ```go {class="line-numbers linkable-line-numbers" data-start="29"}
   package main

   import (
       "helloworld"

       "go.viam.com/rdk/components/camera"
       "go.viam.com/rdk/components/sensor"
       "go.viam.com/rdk/module"
       "go.viam.com/rdk/resource"
   )

   func main() {
       // ModularMain can take multiple APIModel arguments, if your module implements multiple models.
       module.ModularMain(resource.APIModel{camera.API, helloworld.HelloCamera}, resource.APIModel{sensor.API, helloworld.HelloSensor})
   }
   ```

   Save the file.<br><br>

1. Change all instances of `temporary` in <file>hello-world/models/hello-sensor.go</file>:<br><br>

   1. On line 1, change `package temporary` to `package helloworld`.

   1. Edit `temporary` to `hello-world` on line 14, so it looks like this (but with your org ID in place of `jessamy`):<br><br>

      ```go {class="line-numbers linkable-line-numbers" data-start="14"}
      HelloSensor      = resource.NewModel("jessamy", "hello-world", "hello-sensor")
      ```

   1. Change all instances of `newTemporaryHelloSensor` to `newHelloWorldHelloSensor`.<br><br>

   1. Change all instances of `temporaryHelloSensor` to `helloWorldHelloSensor`.

{{% /tab %}}
{{< /tabs >}}

6.  Open <file>temporary/meta.json</file> and copy the model information.
    For example:<br><br>

    ```json {class="line-numbers linkable-line-numbers" data-start="8"}
    {
      "api": "rdk:component:sensor",
      "model": "jessamy:temporary:hello-sensor",
      "short_description": "A sensor that returns a random number.",
      "markdown_link": "README.md#model-jessamyhello-worldhello-sensor"
    }
    ```

1.  Open <file>hello-world/meta.json</file> and paste the sensor model into the model list.<br><br>

    Edit the `description` to include both models.<br><br>

    Change `temporary` to `hello-world`.<br><br>

    The file should now resemble the following:

    ```json {class="line-numbers linkable-line-numbers" data-line="6-20"}
    {
      "$schema": "https://dl.viam.dev/module.schema.json",
      "module_id": "jessamy:hello-world",
      "visibility": "private",
      "url": "",
      "description": "Example camera and sensor components: hello-camera and hello-sensor",
      "models": [
        {
          "api": "rdk:component:camera",
          "model": "jessamy:hello-world:hello-camera",
          "short_description": "A camera that returns an image.",
          "markdown_link": "README.md#model-jessamyhello-worldhello-camera"
        },
        {
          "api": "rdk:component:sensor",
          "model": "jessamy:hello-world:hello-sensor",
          "short_description": "A sensor that returns a random number.",
          "markdown_link": "README.md#model-jessamyhello-worldhello-sensor"
        }
      ],
      "entrypoint": "./run.sh",
      "first_run": ""
    }
    ```

1.  You can now delete the <file>temporary</file> module directory and all its contents.

{{< /expand >}}

## Implement the API methods

Edit the stub files to add the logic from your test script in a way that works with the camera and sensor APIs:

{{< tabs >}}
{{% tab name="Python" %}}

### Implement the camera API

First, implement the camera API methods by editing the camera class definition:

{{< table >}}
{{< tablestep >}}

Add the following to the list of imports at the top of <file>hello-world/src/models/hello_camera.py</file>:

```python {class="line-numbers linkable-line-numbers"}
from viam.media.utils.pil import pil_to_viam_image
from viam.media.video import CameraMimeType
from viam.utils import struct_to_dict
from PIL import Image
```

{{% /tablestep %}}
{{< tablestep >}}

Let's make the path a configurable attribute so you or other users of the module can set the path from which to get the image.
Add the following lines to the camera's `reconfigure()` function definition.
These lines set the `image_path` based on the configuration when the resource is configured or reconfigured.

```python {class="line-numbers" data-start="59"}
attrs = struct_to_dict(config.attributes)
self.image_path = str(attrs.get("image_path"))
```

{{% /tablestep %}}
{{< tablestep >}}

We are not providing a default image but rely on the end user to supply a valid path to an image when configuring the resource.
This means `image_path` is a required attribute.
Add the following code to the `validate()` function to throw an error if `image_path` isn't configured:

```python {class="line-numbers linkable-line-numbers" data-start="46"}
# Check that a path to get an image was configured
fields = config.attributes.fields
if "image_path" not in fields:
    raise Exception("Missing image_path attribute.")
elif not fields["image_path"].HasField("string_value"):
    raise Exception("image_path must be a string.")
```

{{% /tablestep %}}
{{< tablestep >}}

The module generator created a stub for the `get_image()` function we want to implement:

```python {class="line-numbers linkable-line-numbers" data-start="79" }
async def get_image(
    self,
    mime_type: str = "",
    *,
    extra: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
) -> ViamImage:
    self.logger.error("`get_image` is not implemented")
    raise NotImplementedError()
```

You need to replace `raise NotImplementedError()` with code to actually implement the method:

```python {class="line-numbers linkable-line-numbers" data-start="79" data-line="9-10" }
async def get_image(
    self,
    mime_type: str = "",
    *,
    extra: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
) -> ViamImage:
    img = Image.open(self.image_path)
    return pil_to_viam_image(img, CameraMimeType.JPEG)
```

Leave the rest of the functions not implemented, because this module is not meant to return a point cloud (`get_point_cloud()`), and does not need to return multiple images simultaneously (`get_images()`).

Save the file.

{{% /tablestep %}}
{{< tablestep >}}

Open <file>requirements.txt</file>.
Add the following line:

```text
Pillow
```

{{% /tablestep %}}
{{< /table >}}

### Implement the sensor API

{{< expand "Click if you are also creating a sensor component" >}}

Now edit the sensor class definition to implement the sensor API.
You don't need to edit any of the validate or configuration methods because you're not adding any configurable attributes for the sensor model.

1. Add `random` to the list of imports in <file>hello-world/src/models/hello_sensor.py</file> for the random number generation:

   ```python {class="line-numbers linkable-line-numbers"}
   import random
   ```

1. The sensor API only has one resource-specific method, `get_readings()`:

   ```python {class="line-numbers linkable-line-numbers" data-start="59" }
    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        self.logger.error("`get_readings` is not implemented")
        raise NotImplementedError()
   ```

   Replace the logger error and `raise NotImplementedError()` with the following code:

   ```python {class="line-numbers linkable-line-numbers" data-start="65" }
    ) -> Mapping[str, SensorReading]:
        number = random.random()
        return {
            "random_number": number
        }
   ```

   Save the file.

{{< /expand >}}

{{% /tab %}}
{{% tab name="Go" %}}

### Implement the camera API

First, implement the camera API methods by editing the camera class definition:

1. Add the following to the list of imports at the top of <file>hello-world/hello-camera.go</file>:

   ```go {class="line-numbers linkable-line-numbers" data-start="6"}
   "os"
   "reflect"
   ```

1. Add `imagePath = ""` to the global variables so you have the following:

   ```go {class="line-numbers linkable-line-numbers" data-line="22" data-start="19" data-line-offset="19"}
   var (
       HelloCamera      = resource.NewModel("jessamy", "hello-world", "hello-camera")
       errUnimplemented = errors.New("unimplemented")
       imagePath        = ""
   )
   ```

1. In the test script you hard-coded the path to the image.
   For the module, let's make the path a configurable attribute so you or other users of the module can set the path from which to get the image.

   Edit the `type Config struct` definition, replacing the comments with the following:

   ```go {class="line-numbers" data-start="33"}
   type Config struct {
       resource.AlwaysRebuild
       ImagePath string `json:"image_path"`
   }
   ```

   This adds the `image_path` attribute and causes the resource to rebuild each time the configuration is changed.

1. We are not providing a default image but rely on the end user to supply a valid path to an image when configuring the resource.
   This means `image_path` is a required attribute.
   Replace the `Validate` function with the following code to throw an error if `image_path` isn't configured or isn't a string:

   ```go {class="line-numbers linkable-line-numbers" data-start="38"}
   func (cfg *Config) Validate(path string) ([]string, error) {
     var deps []string
     if cfg.ImagePath == "" {
         return nil, resource.NewConfigValidationFieldRequiredError(path, "image_path")
     }
     if reflect.TypeOf(cfg.ImagePath).Kind() != reflect.String {
         return nil, errors.New("image_path must be a string.")
     }
     imagePath = cfg.ImagePath
     return deps, nil
   }
   ```

1. The module generator created a stub for the `Image` function we want to implement:

   ```go {class="line-numbers linkable-line-numbers" data-start="103" }
   func (s *helloWorldHelloCamera) Image(ctx context.Context, mimeType string, extra map[string]interface{}) ([]byte, camera.ImageMetadata, error) {
       panic("not implemented")
   }
   ```

   You need to replace `panic("not implemented")` with code to actually implement the method:

   ```go {class="line-numbers linkable-line-numbers" data-start="104" }
   imgFile, err := os.Open(imagePath)
   if err != nil {
     return nil, camera.ImageMetadata{}, errors.New("Error opening image.")
   }
   defer imgFile.Close()
   imgByte, err := os.ReadFile(imagePath)
   return imgByte, camera.ImageMetadata{}, nil
   ```

1. Delete the `SubscribeRTP` and `Unsubscribe` methods, since they are not applicable to this camera.

1. Leave the rest of the functions not implemented, because this module is not meant to return a point cloud (`NextPointCloud`), and does not need to return multiple images simultaneously (`Images`).

   However, you do need to edit the return statements to return empty structs that match the API.
   Edit these methods so they look like this:

   ```go {class="line-numbers linkable-line-numbers" data-start="110" }
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
   ```

1. Save the file.

### Implement the sensor API

{{< expand "Click if you are also creating a sensor component" >}}

Now edit the sensor class definition to implement the sensor API.
You don't need to edit any of the validate or configuration methods because you're not adding any configurable attributes for the sensor model.

1. Add `"math/rand"` to the list of imports in <file>hello-sensor.go</file> for the random number generation.<br><br>

1. Since `errUnimplemented` and `Config` are defined in <file>hello-camera.go</file>, you need to change <file>hello-sensor.go</file> to avoid redeclaring them:<br><br>

   - Delete line 16, `errUnimplemented = errors.New("unimplemented")` from <file>hello-sensor.go</file>.<br><br>

   - On line 27, change `type Config struct {` to `type sensorConfig struct {`.<br><br>

   - Search for all instances of `*Config` in <file>hello-sensor.go</file> and change them to `*sensorConfig`.

1. The sensor API only has one resource-specific method, `Readings`:

   ```go {class="line-numbers linkable-line-numbers" data-start="93" }
   func (s *helloWorldHelloSensor) Readings(ctx context.Context, extra map[string]interface{}) (map[string]interface{}, error) {
       panic("not implemented")
   }
   ```

   Replace `panic("not implemented")` with the following code:

   ```go {class="line-numbers linkable-line-numbers" data-start="94" }
   number := rand.Float64()
   return map[string]interface{}{
      "random_number": number,
   }, nil
   ```

1. In the `NewClientFromConn` definition, replace `panic("not implemented")` with the following:

   ```go {class="line-numbers linkable-line-numbers" data-start="90"}
   return nil, errUnimplemented
   ```

1. In the `DoCommand` definition, replace `panic("not implemented")` with the following:

   ```go {class="line-numbers linkable-line-numbers" data-start="101"}
   return map[string]interface{}{}, errors.New("not implemented")
   ```

1. Save the file.

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

### View the complete code

You can view the complete example code in the [hello-world-module repository on GitHub](https://github.com/viam-labs/hello-world-module/tree/main).

## Test your module

With the implementation written, it's time to test your module locally:

{{< table >}}
{{< tablestep >}}

{{< tabs >}}
{{% tab name="Python" %}}

Create a virtual Python environment with the necessary packages by running the setup file from within the <file>hello-world</file> directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
```

This environment is where the local module will run.
`viam-server` does not need to run inside this environment.

{{% /tab %}}
{{% tab name="Go" %}}

From within the <file>hello-world</file> directory, compile your module into a single executable:

```sh {class="command-line" data-prompt="$" data-output="5-10"}
make setup
viam module build local
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}

Make sure your machine's instance of `viam-server` is live and connected to Viam.

{{% /tablestep %}}
{{% tablestep %}}

Navigate to your machine's **CONFIGURE** page.

{{% /tablestep %}}
{{% tablestep %}}

Click the **+** button, select **Local module**, then again select **Local module**.

{{% /tablestep %}}
{{% tablestep %}}

{{< tabs >}}
{{% tab name="Python" %}}

Enter the path to the automatically-generated <file>run.sh</file> file, for example, `/home/jessamy/hello-world/run.sh` on Linux or `/Users/jessamy/hello-world/run.sh`.
Click **Create**.

{{% /tab %}}
{{% tab name="Go" %}}

Enter the path to the automatically-generated executable in the <file>/bin/</file> folder, for example, `/Users/jessamyt/myCode/hello-world/bin/hello-world`.
Click **Create**.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
Now add the modular camera resource provided by the module:

Click **+**, click **Local module**, then click **Local component**.

For the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, select or enter `<namespace>:hello-world:hello-camera`, replacing `<namespace>` with the organization namespace you used when generating the stub files.
For example, `jessamy:hello-world:hello-camera`.

For type, enter `camera`.

For name, you can use the automatic `camera-1`.
{{% /tablestep %}}
{{% tablestep %}}
Configure the image path attribute by pasting the following in place of the `{}` brackets:

```json {class="line-numbers linkable-line-numbers"}
{
  "image_path": "<replace with the path to your image>"
}
```

Replace the path with the path to your image, for example `"/Users/jessamyt/Downloads/hello-world.jpg"`.
{{% /tablestep %}}
{{% tablestep %}}
Save the config, then click the **TEST** section of the camera's configuration card.

{{<imgproc src="/how-tos/hello-camera.png" resize="x1100" declaredimensions=true alt="The configuration interface with the Test section of the camera card open, showing a hello world image." style="width:800px" class="shadow aligncenter" >}}

You should see your image displayed.
If not, check the **LOGS** tab for errors.
{{% /tablestep %}}
{{< /table >}}

{{< expand "Click if you also created a sensor component" >}}

1. Add the modular sensor:

   Click **+**, click **Local module**, then click **Local component**.

   For the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, select or enter `<namespace>:hello-world:hello-sensor`, replacing `<namespace>` with the organization namespace you used when generating the stub files.
   For example, `jessamy:hello-world:hello-sensor`.

   For type, enter `sensor`.

   For name, you can use the automatic `sensor-1`.

2. Save the config, then click **TEST** to see a random number generated every second.

   ![The sensor card test section open.](/how-tos/hello-sensor.png)

{{< /expand >}}

## Package and upload the module

You now have a working local module.
To make it available to deploy on more machines, you can package it and upload it to the [registry](https://app.viam.com/registry).

The hello world module you created is for learning purposes, not to provide any meaningful utility, so we recommend making it available only to machines within your {{< glossary_tooltip term_id="organization" text="organization" >}} instead of making it publicly available.

{{< expand "Click to see what you would do differently if this wasn't just a hello world module" >}}

1. Create a GitHub repo with all the source code for your module.
   Add the link to that repo as the `url` in the <file>meta.json</file> file.
1. Create a README to document what your module does and how to configure it.
1. If you wanted to share the module outside of your organization, you'd set `"visibility": "public"` in the <file>meta.json</file> file.

{{< /expand >}}

To package (for Python) and upload your module and make it available to configure on machines in your organization:

{{< tabs >}}
{{% tab name="Python" %}}

1. Package the module as an archive, run the following command from inside the <file>hello-world</file> directory:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -czf module.tar.gz run.sh setup.sh requirements.txt src meta.json
   ```

   This creates a tarball called <file>module.tar.gz</file>.

1. Run the `viam module upload` CLI command to upload the module to the registry:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.0 --platform any module.tar.gz
   ```

{{% /tab %}}
{{% tab name="Go" %}}

From within your <file>hello-world</file> directory, run the `viam module upload` CLI command to upload the module to the registry:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module upload --version 1.0.0 --platform any .
```

{{% /tab %}}
{{< /tabs >}}

Now, if you look at the [Viam Registry page](https://app.viam.com/registry) while logged into your account, you can find your private module listed.
With the module now in the registry, you can configure the hello-sensor and hello-camera on your machines just as you would configure other components and services.
There's no more need for local module configuration; local modules are primarily used for testing.

{{<imgproc src="/how-tos/hello-config.png" resize="x1100" declaredimensions=true alt="The create a component menu open, searching for hello. The hello-camera and hello-sensor components are shown in the search results." style="width:500px" class="shadow aligncenter" >}}

For more information about uploading modules, see [Update and manage modules you created](/operate/modules/advanced/manage-modules/).

## Next steps

For more module creation information, see the [Create a module](/operate/modules/create-module/) guide.

To update or delete a module, see [Update and manage modules](/operate/modules/advanced/manage-modules/).
