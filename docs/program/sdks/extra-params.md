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

Utilize `extra` parameters as follows:

{{< tabs >}}
{{% tab name="Python" %}}

[`Optional[]`](https://docs.python.org/3/library/typing.html#typing.Optional) indicates you are required to pass in an object of either type `Dict[str, Any]` or `None` as a parameter when calling this method.

If passing an object of type `None`, you do not have to specify `None` in the method call.

A `Dict[str, Any]` is a [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) with keys of type [`str`](https://docs.python.org/3/library/stdtypes.html#str) and values of type [`Any`](https://docs.python.org/3/library/typing.html#typing.Any), which can be any type.

You can check the values of the keys you have passed to methods in the API specifications as follows:

``` python {class="line-numbers linkable-line-numbers"}
from typing import Optional, Dict, Any

@abc.abstractmethod
async def some_function(self, required_param: int, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
    # If extra["your_chosen_key"] is present, set usingSomeOption to the value of extra["your_chosen_key"]
    if extra["your_chosen_key"]:
        someOption = extra["your_chosen_key"]
    ...

async def main():
    ... # Connect to the robot

    # Get your resource from the robot
    your_resource = YourResource.from_robot(robot, "your-resource")
    
    # Define a dictionary containing extra information
    extra = {"motion_profile": "pseudolinear", "timeout": 20, "tolerance": 1.1}

    # Send this information in an call to your resource's API
    await your_resource.some_method(3, extra)
```

{{% /tab %}}
{{% tab name="Go" %}}

`extra (map[string]interface{})` indicates you are required to pass in an object of either type `map[string]interface{}` or type `nil` as a parameter when calling this method.

If passing an object of type `nil`, you must specify `nil` in the method call or the method will fail.

A `map[string]interface{}` is an [map](https://go.dev/blog/maps) with keys of type [`string`](https://go.dev/blog/strings) and values of [any type that you have cast to an interface](https://jordanorelli.com/post/32665860244/how-to-use-interfaces-in-go).

You can check the values of the keys you have passed to methods in the API specifications as follows:

```go {class="line-numbers linkable-line-numbers"}
func SomeFunction(ctx context.Context, required_param int, extra map[string]interface{}) error {
    // If extra["your_chosen_key"] is present, set usingSomeOption to the value of extra["your_chosen_key"]
    if yourValue, ok := extra["your_chosen_key"].(bool); ok {
        someOption = yourValue
    }
    ...
}

func main() {
    ... // Connect to the robot

    // Get your resource from the robot
    yourResource, err := YourResource.FromRobot(robot, "your-resource")

    // Define a mapping containing extra information
    extra := map[string]interface{}{"motion_profile": "pseudolinear", "timeout": 20, "tolerance": 1.1}

    // Send this information in an call to your resource's API
    err := yourResource.SomeMethod(context.Background(), 3, extra)

}
```

{{% /tab %}}
{{% /tabs %}}

Use this to pass information to a {{< glossary_tooltip term_id="resource" text="resource's" >}} driver that is not specified as a parameter in the resource type's base API specification.
To do this, code your own modified implementation of the resource type API for a model.
See [Extend Viam with Modular Resources](/program/extend/modular-resources/) for more information and [instructions](/program/extend/modular-resources/#use-a-modular-resource-with-your-robot) on modifying API specifications.
