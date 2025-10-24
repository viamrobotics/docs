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
# updated: ""  # When the tutorial was last entirely checked
# Python checked/updated: 2025-02-25
cost: "0"
---

## Decide what your module will do

The functionality you want to add to your machine determines the APIs you need to implement, so let's start by deciding what your module will do.
For the purposes of this guide, you're going to make a module that does two things:

- Opens an image file from a configured path on your machine
- Returns a random number

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
