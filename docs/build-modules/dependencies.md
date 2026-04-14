---
title: "Access machine resources from within a module"
linkTitle: "Module dependencies"
weight: 36
layout: "docs"
type: "docs"
description: "From within a modular resource, you can access other machine resources using dependencies."
aliases:
date: "2025-11-11"
---

From within a modular resource, you can access other machine {{< glossary_tooltip term_id="resource" text="resources" >}} using dependencies.
For background on required and optional dependencies, see the
[overview](/build-modules/overview/#dependencies).

## The dependency pattern

Every dependency follows three steps: declare it in validation, resolve it in your constructor or reconfigure method, then call its API methods.

The examples below show a base that depends on two motors -- a required left motor and an optional right motor (for a base that can operate in single-motor mode).

### 1. Declare dependencies in validation

Dependency names come from your resource's configuration attributes, keeping the module flexible:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-base",
  "api": "rdk:component:base",
  "model": "myorg:mymodule:mybase",
  "attributes": {
    "left_motor": "motor-1",
    "right_motor": "motor-2"
  }
}
```

Your validation method parses these names and returns them as required or optional dependencies:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
@classmethod
def validate_config(
    cls, config: ComponentConfig
) -> Tuple[Sequence[str], Sequence[str]]:
    req_deps = []
    opt_deps = []
    fields = config.attributes.fields

    # Required dependency
    if "left_motor" not in fields:
        raise Exception("missing required left_motor attribute")
    req_deps.append(fields["left_motor"].string_value)

    # Optional dependency
    if "right_motor" in fields:
        opt_deps.append(fields["right_motor"].string_value)

    return req_deps, opt_deps
```

{{% /tab %}}
{{% tab name="Go" %}}

Define your config struct with fields for each dependency name:

```go {class="line-numbers linkable-line-numbers"}
type Config struct {
    LeftMotor  string `json:"left_motor"`
    RightMotor string `json:"right_motor"`
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
    // Required dependency
    if cfg.LeftMotor == "" {
        return nil, nil,
            resource.NewConfigValidationFieldRequiredError(
                path, "left_motor")
    }
    reqDeps := []string{cfg.LeftMotor}

    // Optional dependency
    var optDeps []string
    if cfg.RightMotor != "" {
        optDeps = append(optDeps, cfg.RightMotor)
    }

    return reqDeps, optDeps, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Resolve dependencies

In Python, resolve dependencies in the `reconfigure` method. In Go, resolve them in your constructor (or `Reconfigure` method if you are not using `AlwaysRebuild`).

Use the dependency name to look up the resource, then cast it to the correct type.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from typing import cast
from viam.components.motor import Motor


def reconfigure(
    self, config: ComponentConfig,
    dependencies: Mapping[ResourceName, ResourceBase]
):
    fields = config.attributes.fields

    # Required dependency -- direct lookup
    left_name = fields["left_motor"].string_value
    self.left = cast(
        Motor,
        dependencies[Motor.get_resource_name(left_name)])

    # Optional dependency -- use .get() and handle None
    self.right = None
    if "right_motor" in fields:
        right_name = fields["right_motor"].string_value
        right_resource = dependencies.get(
            Motor.get_resource_name(right_name))
        if right_resource is not None:
            self.right = cast(Motor, right_resource)

    return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
    "go.viam.com/rdk/components/motor"
)

func newMyBase(ctx context.Context, deps resource.Dependencies,
    conf resource.Config, logger logging.Logger,
) (base.Base, error) {
    baseConfig, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return nil, err
    }

    b := &myBase{
        Named:  conf.ResourceName().AsNamed(),
        logger: logger,
    }

    // Required dependency
    b.left, err = motor.FromProvider(deps, baseConfig.LeftMotor)
    if err != nil {
        return nil, err
    }

    // Optional dependency -- check config, ignore error
    if baseConfig.RightMotor != "" {
        b.right, err = motor.FromProvider(
            deps, baseConfig.RightMotor)
        if err != nil {
            logger.Infow("right motor not available, "+
                "running in single-motor mode",
                "error", err)
        }
    }

    return b, nil
}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}
Go modules that use `resource.AlwaysRebuild` resolve dependencies in the constructor, which runs on every reconfiguration.
If you need to maintain state across reconfigurations, see [Handle reconfiguration](/build-modules/write-a-driver-module/#6-handle-reconfiguration-optional).
{{% /alert %}}

### 3. Use dependencies

Once resolved, call API methods on your dependencies like any other resource:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def set_power(
    self,
    linear: Vector3,
    angular: Vector3,
    *,
    extra: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
):
    await self.left.set_power(linear.y + angular.z)
    if self.right:
        await self.right.set_power(linear.y - angular.z)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func (b *myBase) SetPower(
    ctx context.Context,
    linear, angular r3.Vector,
    extra map[string]interface{},
) error {
    err := b.left.SetPower(
        ctx, linear.Y+angular.Z, extra)
    if err != nil {
        return err
    }
    if b.right != nil {
        return b.right.SetPower(
            ctx, linear.Y-angular.Z, extra)
    }
    return nil
}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Accessing built-in services" color="tip" %}}
Some services like the motion service are available by default as part of `viam-server` even though they don't appear in your machine config. To depend on one, use its full resource name in your validation method:

**Python:** `req_deps.append("rdk:service:motion/builtin")`

**Go:** `deps := []string{motion.Named("builtin").String()}`

Then resolve it the same way as any other dependency.
{{% /alert %}}

## What's next

- [Write a Driver Module](/build-modules/write-a-driver-module/) -- full walkthrough including dependency handling in context.
- [Write a Logic Module](/build-modules/write-a-logic-module/) -- build a module that coordinates multiple resources.
- [Access platform APIs](/build-modules/platform-apis/) -- access fleet management, data, and ML training APIs from within a module.
- For full examples, see the [Desk Safari tutorial](/try/) or [complex module examples on GitHub](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/complex_module/src).
