---
title: "Pet Photographer: Create A Data Filtering Module"
linkTitle: "Pet Photographer"
type: "docs"
description: "Use the filter modular component in the Viam app to photograph your pet in their collar."
tags: ["vision", "filter", "camera", "detector", "services"]
aliases:
  - /tutorials/pet-photographer
  - /tutorials/filter-modular-component
authors: ["Sky Leilani"]
languages: []
viamresources: ["vision", "camera"]
level: "Beginner"
date: "2023-09-17"
# updated: ""
cost: "0"
no_list: true
weight: 3
---

You can write filter modules to selectively store data from your robot based on whether specified conditions have been met.
For example, you can use a module to capture images based on specific criteria, such as the presence of a color, image quality, or sensor thresholds.

In this tutorial, you will create a [color filter](https://github.com/viam-labs/modular-filter-examples) {{< glossary_tooltip term_id="module" text="module" >}} and use it to selectively store images from your robot when a specified color is in frame.
This allows you to get pictures of a pet in the following way:

1. Set up a webcam in a location where your pet is likely to appear in frame and use the data management service to periodically take pictures and sync them to [Viam's cloud](/services/data/#cloud-sync).
2. Attach a colored object, such as a blue collar, to your pet.
3. Set up the color filter module, which will process images and only store them if your pet and their easily identifiable colored object is present.

{{<imgproc src="/tutorials/pet-photographer/data-example.png" resize="700x" declaredimensions=true alt="Dog in blue collar in the camera's live feed">}}

{{< alert title="Note" color="note" >}}
While this tutorial is about creating a color filter, you can also use it as a reference when writing your own filter module for other components, like a [sensor](https://github.com/viam-labs/modular-filter-examples/tree/main/sensorfilter).
{{< /alert >}}

## Hardware Requirements

To create your own filtering pet photographer robot, you'll need the following hardware:

- A computer
- A webcam or an external camera
- A colored object, such as a blue collar for enhanced accuracy _(optional)_

{{< alert title="Tip" color="tip" >}}
In this tutorial, the camera is configured to identify and filter images with the color blue, as it is less common in many environments, including mine.
If your pet already has a distinct color that is different from their environment, you can also configure your camera to use that color to identify pictures of your pet.
{{< /alert >}}

## Set up

Here's how to get started:

1. Install [Go](https://go.dev/dl/) on both your local development computer and on your robot's board, if they are not the same device.
1. [Create a robot](https://docs.viam.com/manage/fleet/robots/#add-a-new-robot) and connect to it.
1. Update [`viam-server`](/installation/manage/#update-viam-server) or [update `viam-server`](/installation/#install-viam-server).
   Your `viam-server` must be version 0.8.0 or higher to access the filtering functionality.

## Create or download the filter module

This tutorial will guide you through the process of [coding your filter module](#code-your-entry-point-file).
However, if you prefer to use the pre-written or final code for the module, you can follow these steps:

1. Clone the [color filter module](https://github.com/viam-labs/modular-filter-examples) from GitHub onto your robot's computer:

   ```{class="command-line" data-prompt="$"}
   git clone https://github.com/viam-labs/modular-filter-examples.git
   ```

1. [Compile the executable](https://docs.viam.com/modular-resources/create/#compile-the-module-into-an-executable) that runs your module in the `module` directory.
1. Save the path to your module's executable for later use.
1. [Add the local module](#add-local-module) and continue the tutorial from there.

If you would rather manually code your color filter module, continue on to the next section.

### Code your filter resource model

To get started writing your filter resource model:

1. Create a folder for your module with the name of your model `colorfilter`.
   - Your model name must use all lowercase letters.
1. Inside that folder, create a file called <file>color_filter.py</file> or <file>color_filter.go</file>.

The full code for this colorfilter camera model's (<file>[color_filter.go](https://github.com/viam-labs/modular-filter-examples/blob/main/colorfilter/color_filter.go)</file>) or (<file>[color_filter.py](https://github.com/viam-labs/modular-filter-examples/blob/main/pycolorfilter/color_filter.py)</file>) file is from the full modular filter examples available on [GitHub](https://github.com/viam-labs/modular-filter-examples/tree/main).

#### Implement the subtype's required methods

Create a file called <file>color_filter.go</file> or <file>color_filter.py</file> within your `colorfilter` module directory and implement the required methods in it.

To code a new filter resource model, you must implement a client interface defined by the required methods outlined in the <file>client.go</file> file in the corresponding [resource's directory](https://github.com/viamrobotics/rdk/components/).
The camera file is at [`rdk/components/camera/client.go`](https://github.com/viamrobotics/rdk/components/camera/client.go).

You can create your own code or copy the code for your file [color_filter.py](https://github.com/viam-labs/modular-filter-examples/blob/main/pycolorfilter/color_filter.py) and [color_filter.go](https://github.com/viam-labs/modular-filter-examples/blob/main/colorfilter/color_filter.go).

For more information, refer to [Create a custom module](https://docs.viam.com/modular-resources/create/#create-a-custom-module).

#### Include the filter module requirements

Your custom filter module must contain two critical elements in your filter function.
One will check if the caller of the filter function is the data management service.
The other will ensure that if the data management service is not the caller, an error is returned.

#### Check the caller of the collector function

When creating your own filter module, it's required to check whether the data management service is the caller of the function responsible for data capture.
If a service other than the data management service calls the function, it will return the stream contents without filtering.
When writing a filter for other components, write your modular code to return the component's original data in case the data management service isn't the caller.

You can achieve this by examining the `fromDataManagement` value within the `extra` argument passed to your filter function in your <file>color_filter.py</file> or <file>color_filter.go</file> file.

{{< alert title="Important" color="note" >}}
When coding a modular camera with the Go SDK, `FromDMContextKey` is used to check the caller of the data capture function.
For all other components, you should use `FromDMString` instead.
{{< /alert >}}

The approach for checking this varies depending on the programming language used to configure your camera:

{{< tabs >}}
{{% tab name="Python"%}}
First, import `from_dm_from_extra`:

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import from_dm_from_extra
```

Then, include it in the conditional statement in your filter function:

```python {class="line-numbers linkable-line-numbers"}
if from_dm_from_extra(extra):
    detections = await self.vision_service.get_detections(img)
```

- The Python-configured camera checks if the data management service is the caller of the filter function by using `from_dm_from_extra` to determine whether to store data.

{{% /tab %}}
{{% tab name="Go"%}}

Write a conditional statement that checks `FromDMContextKey`:

```go {class="line-numbers linkable-line-numbers"}
if ctx.Value(data.FromDMContextKey{}) != true {
   // If not data management collector, return underlying stream contents without filtering.
   return fs.cameraStream.Next(ctx)
}

// Only return captured image if it contains a certain color set by the vision service.
 img, release, err := fs.cameraStream.Next(ctx)

 detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
```

- The Go-configured camera checks if the data management service is the caller of the filter function by using `FromDMContextKey` to determine whether to store data.
  - If `FromDMContextKey` is `true` and the data management service is the caller, captures an image by declaring the (`img`) variable and filling it with the content from the camera stream.
- Then, after capturing the image, the code continues to request detections.

**PLACEHOLDER: `FromDMContextKey` vs `FromDMString`?**

**`FromDMString` has been referenced as important and essential, but it's only used in the sensor filter.**
**Colorfilter uses `FromDMContextKey`.**
**Updating all references once clarified.**

{{% /tab %}}
{{< /tabs >}}

#### Return filter error to data management

After implementing a check to identify the initiator of the filter function, you must include the safeguard that will return an error if the data management service is not the caller.

To do this, include the following in your filter module's <file>color_filter.py</file> or <file>color_filter.go</file>:

{{< tabs name="Example tabs">}}
{{% tab name="Python"%}}

First, import the safeguard error `NoCaptureToStoreError` from Viam:

```python {class="line-numbers linkable-line-numbers"}
from viam.errors import NoCaptureToStoreError
```

Then, within your first conditional statement, create a conditional statement that returns the error when the data management service is not the caller of the filter function:

```python {class="line-numbers linkable-line-numbers"}
if from_dm_from_extra(extra):
    detections = await self.vision_service.get_detections(img)
    if len(detections) == 0:
        raise NoCaptureToStoreError()
```

- If the length of the `detections` variable is 0, it indicates that there is no content in the variable.
- `NoCaptureToStoreError()` is called to signify that the data management service was not the caller.

{{% /tab %}}
{{% tab name="Go"%}}

Inside your filter function, write a conditional statement that includes the error message `data.ErrNoCaptureToStore`:

```go {class="line-numbers linkable-line-numbers"}
if len(detections) == 0 {
   return nil, nil, data.ErrNoCaptureToStore
}
```

- If the length of the `detections` variable is 0, it indicates that there is no content in the variable.
- `data.ErrNoCaptureToStore` is called to signify that the data management service was not the caller.

{{% /tab %}}
{{< /tabs >}}

Once you've included the required safeguard and utility function, your complete color filter function should look like the following.

{{< tabs >}}
{{% tab name="Python"%}}

```python {class="line-numbers linkable-line-numbers"}
async def get_image(
  self,
  mime_type: str = "",
  *,
  extra: Optional[Dict[str, Any]] = None,
  timeout: Optional[float] = None,
  **kwargs
  ) -> Image.Image:
    """Filters the output of the underlying camera"""
    img = await self.actual_cam.get_image()
    if from_dm_from_extra(extra):
        detections = await self.vision_service.get_detections(img)
        if len(detections) == 0:
            raise NoCaptureToStoreError()

    return img
```

{{% /tab %}}
{{% tab name="Go"%}}

This code includes the safeguards you wrote earlier as well as error handling for getting the next source image and obtaining detections.

```go {class="line-numbers linkable-line-numbers"}
// Next contains the filtering logic and returns select data from the underlying camera.
func (fs filterStream) Next(ctx context.Context) (image.Image, func(), error) {
if ctx.Value(data.FromDMContextKey{}) != true {
// If not data management collector, return underlying stream contents without filtering.
return fs.cameraStream.Next(ctx)
}

    // Only return captured image if it contains a certain color set by the vision service.
    img, release, err := fs.cameraStream.Next(ctx)
    if err != nil {
      return nil, nil, errors.New("could not get next source image")
    }
    detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
    if err != nil {
      return nil, nil, errors.New("could not get detections")
    }

    if len(detections) == 0 {
      return nil, nil, data.ErrNoCaptureToStore
    }

    return img, release, err
}
```

{{% /tab %}}
{{< /tabs >}}

- If the data management service is the caller, the filter function requests detections from the vision service and returns the image if the specified color is detected.
  Otherwise, it raises `data.ErrNoCaptureToStore` or `NoCaptureToStoreError()`.

Once you have implemented your resource subtype's required methods and written your filter function, your final code should look like this:

{{< tabs >}}
{{% tab name="Python"%}}

<file>color_filter.py</file> implements "colorfilter", a custom model of the camera component.

<details>
  <summary>Click to view sample code from <file>color_filter.py</file></summary>

```python {class="line-numbers linkable-line-numbers"}
from typing import (
    ClassVar, Mapping, Sequence, Optional, cast, Tuple, List, Any, Dict
)
from typing_extensions import Self
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, ResponseMetadata, Geometry
from viam.components.camera import Camera
from viam.resource.types import Model, ModelFamily
from viam.resource.base import ResourceBase
from viam.media.video import NamedImage
from PIL import Image
from viam.errors import NoCaptureToStoreError
from viam.services.vision import Vision
from viam.utils import from_dm_from_extra


class ColorFilterCam(
        Camera,
        Reconfigurable
  ):

    """A ColorFilterCam wraps the underlying camera
    `actual_cam` and only keeps the data captured on the
    actual camera if `vision_service` detects a certain
    color in the captured image.
    """
    MODEL: ClassVar[Model] = Model(
        ModelFamily("example", "camera"),
        "colorfilter")

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def new_cam(
        cls,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        cam = cls(config.name)
        cam.reconfigure(config, dependencies)
        return cam

    @classmethod
    def validate_config(
        cls,
        config: ComponentConfig
    ) -> Sequence[str]:
        """Validates JSON configuration"""
        actual_cam = config.attributes.fields["actual_cam"].string_value
        if actual_cam == "":
            raise Exception(
              "actual_cam attribute is required for a ColorFilterCam component"
              )
        vision_service = config.attributes.fields[
          "vision_service"
        ].string_value
        if vision_service == "":
            raise Exception(
              """
              vision_service attribute
              is required for a
              ColorFilterCam component
              """
            )
        return [actual_cam, vision_service]

    def reconfigure(
        self,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """Handles attribute reconfiguration"""
        actual_cam_name = config.attributes.fields[
          "actual_cam"
        ].string_value
        actual_cam = dependencies[
          Camera.get_resource_name(actual_cam_name)
        ]
        self.actual_cam = cast(Camera, actual_cam)

        vision_service_name = config.attributes.fields[
          "vision_service"
          ].string_value
        vision_service = dependencies[
          Vision.get_resource_name(
            vision_service_name
          )
        ]
        self.vision_service = cast(
           Vision,
           vision_service
        )

    async def get_properties(
              self,
              *,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Camera.Properties:
        """Returns details about the camera"""
        return await self.actual_cam.get_properties()

    async def get_image(
              self,
              mime_type: str = "",
              *,
              extra: Optional[Dict[str, Any]] = None,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Image.Image:
        """Filters the output of the underlying camera"""
        img = await self.actual_cam.get_image()
        if from_dm_from_extra(extra):
            detections = await self.vision_service.get_detections(img)
            if len(detections) == 0:
                raise NoCaptureToStoreError()

        return img

    async def get_images(
              self,
              *,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Tuple[
         List[NamedImage],
         ResponseMetadata
         ]:
        raise NotImplementedError

    async def get_point_cloud(
              self,
              *,
              extra: Optional[Dict[str, Any]] = None,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Tuple[
         bytes,
         str
         ]:
        raise NotImplementedError

    async def get_geometries(self) -> List[Geometry]:
        raise NotImplementedError
```

- The Python SDK simplifies the verification process by exposing the utility function `from_dm_from_extra`, which handles the check for you.
- For other programming languages, similar utility functions will be exposed to help you check the caller of your filter function.
  The method for this verification may vary depending on the specific function and programming language.
  For detailed information, please refer to the SDK documentation relevant to your specific language.

- If the boolean is `true`, the function will call the vision service to get detections and return the image if the color is detected, otherwise, it raises `NoCaptureToStoreError()`.

{{% /tab %}}
{{% tab name="Go"%}}

<file>color_filter.go</file> implements "colorfilter", a custom model of the camera component.

<details>
  <summary>Click to view sample code from <file>color_filter.go</file></summary>

```go {class="line-numbers linkable-line-numbers"}
// Package colorfilter implements a modular camera that filters the output of an underlying camera and only keeps
// captured data if the vision service detects a certain color in the captured image.
package colorfilter

import (
"context"
"fmt"
"image"

    "github.com/edaniels/golog"
    "github.com/pkg/errors"
    "github.com/viamrobotics/gostream"

    "go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/data"
    "go.viam.com/rdk/pointcloud"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/rimage/transform"
    "go.viam.com/rdk/services/vision"

)

var (
// Model is the full model definition.
Model = resource.NewModel("example", "camera", "colorfilter")
errUnimplemented = errors.New("unimplemented")
)

func init() {
resource.RegisterComponent(camera.API, Model, resource.Registration[camera.Camera, *Config]{
Constructor: newCamera,
})
}

func newCamera(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger golog.Logger) (camera.Camera, error) {
c := &colorFilterCam{
Named: conf.ResourceName().AsNamed(),
logger: logger,
}
if err := c.Reconfigure(ctx, deps, conf); err != nil {
return nil, err
}
return c, nil
}

// Config contains the name to the underlying camera and the name of the vision service to be used.
type Config struct {
ActualCam string `json:"actual_cam"`
VisionService string `json:"vision_service"`
}

// Validate validates the config and returns implicit dependencies.
func (cfg \*Config) Validate(path string) ([]string, error) {
if cfg.ActualCam == "" {
return nil, fmt.Errorf(`expected "actual_cam" attribute in %q`, path)
}
if cfg.VisionService == "" {
return nil, fmt.Errorf(`expected "vision_service" attribute in %q`, path)
}

    return []string{cfg.ActualCam, cfg.VisionService}, nil

}

// A colorFilterCam wraps the underlying camera `actualCam` and only keeps the data captured on the actual camera if `visionService`
// detects a certain color in the captured image.
type colorFilterCam struct {
resource.Named
actualCam camera.Camera
visionService vision.Service
logger golog.Logger
}

// Reconfigure reconfigures the modular component with new settings.
func (c *colorFilterCam) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
camConfig, err := resource.NativeConfig[*Config](conf)
if err != nil {
return err
}

    c.actualCam, err = camera.FromDependencies(deps, camConfig.ActualCam)
    if err != nil {
      return errors.Wrapf(err, "unable to get camera %v for colorfilter", camConfig.ActualCam)
    }

    c.visionService, err = vision.FromDependencies(deps, camConfig.VisionService)
    if err != nil {
      return errors.Wrapf(err, "unable to get vision service %v for colorfilter", camConfig.VisionService)
    }

    return nil

}

// DoCommand simply echoes whatever was sent.
func (c \*colorFilterCam) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
return cmd, nil
}

// Close closes the underlying camera.
func (c \*colorFilterCam) Close(ctx context.Context) error {
return c.actualCam.Close(ctx)
}

// Images does nothing.
func (c \*colorFilterCam) Images(ctx context.Context) ([]camera.NamedImage, resource.ResponseMetadata, error) {
return nil, resource.ResponseMetadata{}, errUnimplemented
}

// Stream returns a stream that filters the output of the underlying camera stream in the stream.Next method.
func (c \*colorFilterCam) Stream(ctx context.Context, errHandlers ...gostream.ErrorHandler) (gostream.VideoStream, error) {
camStream, err := c.actualCam.Stream(ctx, errHandlers...)
if err != nil {
return nil, err
}

    return filterStream{camStream, c.visionService}, nil

}

// NextPointCloud does nothing.
func (c \*colorFilterCam)NextPointCloud(ctx context.Context)(pointcloud.PointCloud, error)
{
  return nil, errUnimplemented
}

// Properties returns details about the camera.
func (c \*colorFilterCam) Properties(ctx context.Context)(camera.Properties, error)
{
  return c.actualCam.Properties(ctx)
}

// Projector does nothing.
func (c \*colorFilterCam) Projector(ctx context.Context) (transform.Projector, error) {
  return nil, errUnimplemented
}

type filterStream struct {
cameraStream gostream.VideoStream
visionService vision.Service
}

// Next contains the filtering logic and returns select data from the underlying camera.
func (fs filterStream) Next(ctx context.Context) (image.Image, func(), error) {
if ctx.Value(data.FromDMContextKey{}) != true {
// If not data management collector, return underlying stream contents without filtering.
return fs.cameraStream.Next(ctx)
}

// Only return captured image if it contains a certain color set by the vision service.
img, release, err := fs.cameraStream.Next(ctx)
if err != nil {
return nil, nil, errors.New("could not get next source image")
}
detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
if err != nil {
return nil, nil, errors.New("could not get detections")
}

if len(detections) == 0 {
return nil, nil, data.ErrNoCaptureToStore
}

return img, release, err
}

// Close closes the stream.
func (fs filterStream) Close(ctx context.Context) error {
return fs.cameraStream.Close(ctx)
}
```

- A modular camera coded in Go looks for a flag called `fromDM` in the context (`ctx`) using `ctx.Value(data.FromDMContextKey{})` to figure out if data management triggered the filter, rather than using `extra`.

  - Instead of implementing [`GetImage`](/components/camera/#getimage) (like it is in Python, etc), in Go, you will implement `Stream` as shown in the example code.

- For other programming languages, similar utility functions will be exposed to help you check the caller of your filter function.
  The approach to perform this check may differ depending on the particular function and programming language. For detailed information, please refer to your chosen language's SDK documentation.
- If the boolean is `true`, the function will call the vision service to get detections and return the image if the color is detected; otherwise, it will raise the [`ErrNoCaptureToStore`](https://github.com/viamrobotics/rdk/blob/214879e147970a454f78035e938ea853fcd79f17/data/collector.go#L44) error.

  {{% /tab %}}
  {{< /tabs >}}

For more information, read [Code a new resource model](/modular-resources/create/#code-a-new-resource-model).

### Code your entry point file

Next, code your module entry point file to initialize and start the filter module.

To code your entry point file yourself, you must locate the subtype API as defined in the relevant `<resource-name>/<resource-name>.go` file in the RDK on Viam’s GitHub.

- In this example, the camera's API is defined in the <file>[camera.go](https://github.com/viamrobotics/rdk/blob/main/components/camera/camera.go)</file> file in the RDK on Viam's Github.
  When developing your <file>main.go</file> or <file>main.py</file> file, reference this file.

{{< alert title="Important" color="note" >}}
If you want to filter data based on a constraint other than color, you need to modify the code below.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Python"%}}
Inside your module's folder, create a file called <file>main.py</file> (the module entry point file).
Add the code below to initialize and start the filter module.

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from viam.components.camera import Camera
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
import color_filter


async def main():

    """
    This function creates and starts a new module,
    after adding all desired resource models.
    Resource creators must be
    registered to the resource
    registry before the module adds the resource model.
    """
    Registry.register_resource_creator(
        Camera.SUBTYPE,
        color_filter.ColorFilterCam.MODEL,
        ResourceCreatorRegistration(
            color_filter.ColorFilterCam.new_cam,
            color_filter.ColorFilterCam.validate_config
        )
    )
    module = Module.from_args()
    module.add_model_from_registry(
        Camera.SUBTYPE,
        color_filter.ColorFilterCam.MODEL
    )
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go"%}}
Inside your module's directory, create another folder with the name `module`.
Inside the `module` folder, create a file called <file>main.go</file> (the entry point file for the module).
Add the code below to initialize and start the filter module.

```go {class="line-numbers linkable-line-numbers"}
// Package main is a module which serves the colorfilter custom module.
package main

import (
  "context"

  "github.com/edaniels/golog"
  "go.viam.com/utils"

  "github.com/viam-labs/modular-filter-examples/colorfilter"
  "go.viam.com/rdk/components/camera"
  "go.viam.com/rdk/module"
)

func main() {
  utils.ContextualMain(mainWithArgs, module.NewLoggerFromArgs("colorfilter_module"))
}

func mainWithArgs(ctx context.Context, args []string, logger golog.Logger) (err error) {
  myMod, err := module.NewModuleFromArgs(ctx, logger)
  if err != nil {
    return err
  }

  err = myMod.AddModelFromRegistry(ctx, camera.API, colorfilter.Model)
  if err != nil {
    return err
  }

  err = myMod.Start(ctx)
  defer myMod.Close(ctx)
  if err != nil {
    return err
  }
  <-ctx.Done()
  return nil
}
```

{{% /tab %}}
{{< /tabs >}}

For more information on creating your own module, refer to [Code your own modules to create modular resources](https://docs.viam.com/modular-resources/create/).

Once you've written your filter module, [compile the executable](https://docs.viam.com/modular-resources/create/#compile-the-module-into-an-executable) that runs your module when executed.

Note the absolute path to your module’s executable for later use.

### Add local module

Now that you've completed writing and compiling your filter module, it's time to put it to use:

1. Navigate to your robot's page on the [Viam app](https://app.viam.com/robots) and select the **Config** tab.
1. Click the **Modules** subtab to configure the local color filter module for your robot's system in the Viam app.
1. You identified your module's path when you [compiled your module's executable](/modular-resources/create/#compile-the-module-into-an-executable).
1. In the **Add local module** section, enter the name of your module (`colorfilter`) along with the filter's executable, and click **Add module**.
   - The name should be all lowercase.
   - Enter the absolute path to your module's executable on the robot's computer as the **Executable path**. The executable path is the path you noted down when you [compiled your module's executable](/modular-resources/create/#compile-the-module-into-an-executable).
1. Then, click **Save config**.

![A color filter module that has been added.](/tutorials/pet-photographer/add-colorfilter-module.png)

## Add services

Add a [vision service](/services/vision/detection/) for color detection and a [data management service](/services/data/) for storing your filtered images.
Consider the specific services your filter might require when working with other components.
For example, the [sensors service](/services/sensors/) provides a central interface to all of your robot’s sensors.

### Add data management service

To enable data capture on your robot, add and configure the [data management service](/services/data/) to capture and store data on your robot's computer:

{{< tabs >}}
{{% tab name="Builder" %}}

1. On the **Config** page, click the **Services** subtab and click **Create service** in the lower-left corner.
1. Choose `Data Management` as the type and name your instance of the data manager `dm`.
   This service syncs data from your robot to the Viam app in the cloud.
1. Select **Create**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data every 0.1 minutes in the <file>~/.viam/capture</file> directory.

   You can leave the default settings as they are.
   Click **Save config** at the bottom of the window.

   ![An instance of the data management service named "dm". The cloud sync and capturing options are toggled on and the directory is empty. The interval is set to 0.1](/tutorials/pet-photographer/data-management-services.png)

   For more detailed information, see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).
   {{% /tab %}}
   {{% tab name="JSON Template" %}}
   Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
    {
      "name": "dm",
      "type": "data_manager",
      "namespace": "rdk",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "tags": [],
        "additional_sync_paths": []
      }
    },
  ... // Vision and other services
```

Click **Save Config** and head back to **Builder** mode.

{{% /tab %}}
{{< /tabs >}}

### Vision service to detect color

This tutorial uses the color of my dog's collar, `#43A1D0` or `rgb(67, 161, 208)` (blue), but you can use a different color that matches your pet or a distinctly colored item on your pet.

**Hex color #43A1D0**: {{<imgproc src="/tutorials/pet-photographer/43a1d0.png" resize="90x" declaredimensions=true alt="A color swatch for the color of the example subject's collar">}}

To configure your [vision service color detector](/services/vision/detection/):

{{< tabs >}}
{{% tab name="Builder" %}}

1. At the bottom-left of the page, click **Create service**.
1. Select the `Vision` type, then select the `Color Detector` model.
1. Enter `my_color_detector` as the name for your detector and click **Create**.
1. In the vision service panel, click the color selection box to set the color to be detected.
   For this tutorial, set the color to the color of your pet, or use a blue collar or ribbon to improve your filter's accuracy.
1. Then, set **Hue Tolerance** to `0.06` and **Segment Size px** to `100`.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to blue, the hue tolerance set to 0.06, and the segment size set to 100.](/tutorials/pet-photographer/vision-service.png)

For more detailed information, refer to [Configure a color detector](/services/vision/detection/#configure-a-color_detector).

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
  {
    "name": "my_color_detector",
    "type": "vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 100,
      "detect_color": "#43a1d0",
      "hue_tolerance_pct": 0.06
    }
  },
  ... // Other services
```

{{% /tab %}}
{{< /tabs >}}

## Configure the color filter camera

With the vision and data management services configured, you can now configure your camera to filter by color and store photos to Viam's cloud.

### Configure your camera

Navigate to your robot's page in the app and click on the **Config** tab.

1. Add your robot's [camera](/components/camera/) as a component by clicking **Create component** in the lower-left corner of the page and entering 'webcam'.
1. Select the `webcam` model and enter 'cam' as the name for your camera.
1. Then click **Create**.

Your robot's configuration page now includes a panel for your camera.

- To choose the camera the robot will use, click the **video path** field.
  - If your robot is connected, you'll see a list of available cameras.
  - Select the camera you want to use, then click **Save config**.

![An instance of the webcam component named 'cam'](/tutorials/pet-photographer/webcam-component.png)

### Add colorfilter component

1. Click the **Components** subtab and then click **Create component**.
1. Next, select the `local modular resource` type from the list.
   {{<imgproc src="extend/modular-resources/configure/add-local-module-list.png" resize="300x" declaredimensions=true alt="The add a component modal showing the list of components to add with 'local modular resource' shown at the bottom">}}
1. On the following screen:

   1. Select the camera from the drop down menu.
   1. Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} for your modular resource's {{< glossary_tooltip term_id="model" text="model" >}}, `example:camera:colorfilter`.
   1. Provide a name for this instance of your modular resource.
      This name must be different from the module name.

      {{<imgproc src="/tutorials/pet-photographer/add-colorfilter-module-create.png" resize="400x" declaredimensions=true alt="The add a component model showing the create a module step for a local color filter module">}}

1. Click **Create** to create the modular resource component.
1. Copy the following JSON configuration into the **Attributes** section:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "vision_service": "my_color_detector",
     "actual_cam": "cam"
   }
   ```

   ![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam](/tutorials/pet-photographer/colorfiltercam-component-attributes.png)

### Configure data capture

To add data capture for the color filter camera, click **Add Method** in the **Data Capture configuration** section of your color filter camera component.
Toggle the **Type** dropdown menu, select **ReadImage**, and set the **Frequency** of the capture to `0.1`.
Then, click **Save config**.

![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam as well as the data capture configuration capture set capture ReadImage at 0.1 frequency](/tutorials/pet-photographer/colorfiltercam-component.png)

## Test your color filter camera

To test that your color filter camera is capturing and filtering images properly, navigate to the **Control** tab on your robot's page.

On the **colorfiltercam** panel, toggle **view colorfiltercam** to view your camera's live feed.
Test the filter by moving a blue colored item within the camera's field of view.
Then, go to the **Data** tab to view pictures that contain the blue colored item.

For example, your pet with the blue collar:

![Filtered data tab contents from colorfiltercam showing only photos of dog with blue collar](/tutorials/pet-photographer/data-capture.png)

## Next steps

Your pet photographer is now set up.
Place it in an area your pet frequently visits and don't forget to attach the colored object to your pet.

If you want to learn more about data management or detection, you may enjoy one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/services/try-viam-color-detection.md" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" %}}
{{% card link="/tutorials/projects/guardian/" %}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{< /cards >}}
