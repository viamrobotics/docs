---
title: "Using Extra Params with Viam's SDKs"
linkTitle: "Extra Params"
weight: 40
type: "docs"
description: "Using extra parameters with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

Many component API methods have the option to pass in `extra` parameters.
These are optional to pass into method calls with the Python SDK, but you must specify or pass them in as `nil` with the Go SDK. TODO: unsure if putting here or at the end

Utilize `extra` parameters as follows:

{{< tabs >}}
{{% tab name="Python" %}}

``` python
# Must import Optional, Any from Typing

extra (Optional[Dict[str, Any]])

extra = 
```

`Optional[]` (TODO: link) indicates you are required to pass in an object of either type `Dict[str, Any]` or type `None` as a parameter when calling this method.
You do not have to specify the object of type `None`, not specifying an object for this parameter is sufficient.

A `Dict[str, Any]` is a [dictionary]() with keys of type `str` and values of type `Any`, which can be any type.
The keys can be whatever information you would like to pass.
An example:

You can check the values of the keys you have passed to methods in the API specifications as follows:

Use this to pass information to the {{< glossary_tooltip term_id="resource" text="resource's" >}} drivers' that is not specified as a parameter in the resource type's base API specification.
To do this, code your own modified implementation of the resource type API for a model.
See [Extend Viam with Modular Resources](/program/extend/modular-resources/) for more information and [instructions](/program/extend/modular-resources/#use-a-modular-resource-with-your-robot) on how to do this.

{{% /tab %}}
{{% tab name="Go" %}}

<!-- https://github.com/viamrobotics/motion-demos/blob/c99183e6eb9c1606013a961dbe4cde491322e095/ur5eNYC/ur5eNYC.go#L43 -->
```go {class="line-numbers linkable-line-numbers"}
extra (map[string]interface{})

extra := map[string]interface{}{"motion_profile": "pseudolinear", "timeout": 20, "tolerance": 1.1}

func SomeFunction(ctx context.Context, pos spatialmath.Pose, extra map[string]interface{}) error {
    if runtimeKinematicsSetting, ok := extra["arm_hosted_kinematics"].(bool); ok {
        usingHostedKinematics = runtimeKinematicsSetting
    }
}

package main

import (
    "fmt"
)

func PrintAll(vals []interface{}) {
    for _, val := range vals {
        fmt.Println(val)
    }
}

func main() {
    names := []string{"stanley", "david", "oscar"}
    vals := make([]interface{}, len(names))
    for i, v := range names {
        vals[i] = v
    }
    PrintAll(vals)
}
```

`extra (map[string]interface{})` indicates you are required to pass in an object of either type `map[string]interface{}` or type `nil` as a parameter when calling this method.
You do have to specify the object of type `nil`, not specifying an object for this parameter makes the call fail.

A `map[string]interface{}` is an [mapping]() with keys of type [`string`]() and values of any type (all types satisfy an empty interface)[https://jordanorelli.com/post/32665860244/how-to-use-interfaces-in-go] that have been passed into an interface.

{{% /tab %}}
{{% /tabs %}}
