---
title: "Module dependencies"
linkTitle: "Module dependencies"
weight: 25
layout: "docs"
type: "docs"
description: "Handle dependencies in your custom modular resource."
---

This page covers intermediate-level information about modules and their dependencies.

## The lifecycle of a module

An instance of a module runs as a separate process from `viam-server`.
`viam-server` manages the lifecycle of the module, communicating with it over UNIX sockets.
The lifecycle of a module and the resources it provides is as follows:

1. `viam-server` starts, and if it is connected to the internet, it checks for configuration updates.
1. `viam-server` starts any configured modules.
1. For each modular resource configured on the machine, `viam-server` uses the resource's `validate` function and the `depends_on` field in the resource configuration to determine the dependencies of the resource.
1. If a dependency is not already running, `viam-server` starts it before starting the resource.
1. `viam-server` builds the resource based on its configuration.
1. If the configuration fails, `viam-server` attempts to reconfigure the resource.
1. The modular resource is ready to use.
1. If at any point the user changes the configuration of the machine, `viam-server` reconfigures the affected resources.
1. If a resource crashes, `viam-server` attempts to rebuild it.
1. When `viam-server` shuts down, it attempts to stop all running modules.

## What are dependencies?

Dependencies are other {{< glossary_tooltip term_id="resource" text="resources" >}} that your modular resource needs to access in order to function.
For example, a vision service might depend on a camera component, meaning that the camera is a dependency of that vision service.

When `viam-server` builds all the resources on a machine, it builds the dependencies first.

### Implicit versus explicit dependencies

- **Implicit dependencies** require users to configure a named attribute (for example `"left-motor": "motor1"`).
  - Recommended when dependencies are required, because implicit dependencies:
    - Make it more clear what needs to be configured.
    - Eliminate the need for users to configure the same resource name twice.
    - Make debugging easier.
  - Your module code must access the dependency using its attribute name and return it in the list of dependencies from the `validate` function.
- **Explicit dependencies** require that a user list the names of dependencies in the `depends_on` field of the resource's configuration.
  - Useful when dependencies are optional.
  - Depending on how you write your module, especially if your resources use multiple explicit dependencies, you may need users to configure the dependency both in the `depends_on` field and as an attribute so that your code can determine which dependency is which.

## Access dependencies

From within a module, you cannot access resources in the same way that you would in a client application.
For example, you cannot call `Camera.from_robot()` to get a camera resource.

Instead, you must access dependencies as follows:

### Access implicit dependencies

{{< tabs >}}
{{% tab name="Python" %}}

1. In your modular resource's `validate_config` method, check the configuration attributes, then add the dependency name to the list of dependencies.

   ```python {class="line-numbers linkable-line-numbers"}
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        deps = []
        fields = config.attributes.fields
        if not "camera_name" in fields:
            raise Exception("missing required camera_name attribute")
        elif not fields["camera_name"].HasField("string_value"):
            raise Exception("camera_name must be a string")
        camera_name = fields["camera_name"].string_value
        deps.append(camera_name)
        return deps
   ```

1. In your `reconfigure` method, access the dependency by using its name as a key in the `dependencies` mapping.
1. Cast the dependency to the correct type.

   ```python {class="line-numbers linkable-line-numbers"}
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        camera_name = config.attributes.fields["camera_name"].string_value
        camera_resource = dependencies[Camera.get_resource_name(camera_name)]
        self.the_camera = cast(Camera, camera_resource)

        # If you need to use the camera name in your module,
        # for example to pass it to a vision service method,
        # you can store it in an instance variable.
        self.camera_name = camera_name

        return super().reconfigure(config, dependencies)
   ```

1. Now you can call API methods on the dependency resource within your module, for example `await self.the_camera.get_image()`.

For full examples, see [<file>ackermann.py</file>](https://github.com/mcvella/viam-ackermann-base/blob/main/src/ackermann.py) or [Viam complex module examples on GitHub](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/complex_module/src).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

### Access explicit dependencies

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

{{% hiddencontent %}}
There is not currently an SDK method to access configuration attributes of dependencies in Python or Go, but in Python it is possible to use `get_robot_part` to return information including the whole configuration of a machine part, and then access the configuration attributes of the dependency from there.
{{% /hiddencontent %}}

## Configure your module's dependencies more easily with a discovery service
