---
title: "Using Extra Params with Viam's SDKs"
linkTitle: "Extra Params"
weight: 40
type: "docs"
description: "Using extra parameters with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["sdk", "extra", "extend"]
---

Many component API methods have the option to pass in `extra` parameters.
These are typed as `Optional[Dict[str, Any]]` in the Python SDK and `map[string]interface{}` in the Go SDK.

Here's how to [pass correctly typed objects to](#define) and [utilize](#utilize) these `extra` parameters.

## Define

{{< tabs >}}
{{% tab name="Python" %}}

[`Optional[Dict[str, Any]]`](https://docs.python.org/3/library/typing.html#typing.Optional) indicates you are required to pass in an object of either type `Dict[str, Any]` or `None` as a parameter when calling this method.

An object of type `Dict[str, Any]` is a [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) with keys of type [`str`](https://docs.python.org/3/library/stdtypes.html#str) and values of [`any type`](https://docs.python.org/3/library/typing.html#typing.Any),

For example:

``` python {class="line-numbers linkable-line-numbers"}
async def main():
    ... # Connect to the robot

    # Get your resource from the robot
    your_resource = YourResource.from_robot(robot, "your-resource")
    
    # Define a dictionary containing extra information
    extra = {"one": "one", "two": 2, "three": 3.0}

    # Send this information in an call to your resource's API
    await your_resource.some_function("this is required", extra)
```

{{% alert title="Note" color="note" %}}

If passing an object of type `None`, you do not have to specify `None` in the method call.

{{% /alert %}}
{{% /tab %}}
{{% tab name="Go" %}}

`extra (map[string]interface{})` indicates you are required to pass in an object of either type `map[string]interface{}` or `nil` as a parameter when calling this method.

An object of type `map[string]interface{}` is an [map](https://go.dev/blog/maps) with keys of type [`string`](https://go.dev/blog/strings) and values of [any type that you have cast to an interface](https://jordanorelli.com/post/32665860244/how-to-use-interfaces-in-go).

For example:

```go {class="line-numbers linkable-line-numbers"}
func main() {
    ... // Connect to the robot

    // Get your resource from the robot
    yourResource, err := YourResource.FromRobot(robot, "your-resource")

    // Define a map containing extra information
    extra := map[string]interface{}{"one": "one", "two": 2, "three": 3.0}

    // Send this information in an call to your resource's API
    err := yourResource.SomeFunction(context.Background(), "this is required", extra)
}
```

{{% alert title="Note" color="note" %}}

If passing an object of type `nil`, you must specify `nil` in the method call or the method will fail.

{{% /alert %}}
{{% /tab %}}
{{% /tabs %}}

## Utilize

Use these `extra` parameters to pass information to a {{< glossary_tooltip term_id="resource" text="resource's" >}} driver that is not specified as a parameter in the [built-in resource type's API specification](/program/extend/modular-resources/#apis).

To do this, you must code your own modified implementation of the resource type's API for a model.
See [Extend Viam with Modular Resources](/program/extend/modular-resources/) for more information and [instructions](/program/extend/modular-resources/#use-a-modular-resource-with-your-robot) on modifying API specifications.

An example of how to check the values of keys in an `extra` parameter of a [resource API method](/program/sdks/#add-control-logic):

{{< tabs >}}
{{% tab name="Python" %}}

``` python {class="line-numbers linkable-line-numbers"}
@abc.abstractmethod
async def some_function(self, required_param: str, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):

    # If extra["one"] is present, set someOption to the value of extra["one"]
    if extra["one"]:
        someOption = extra["one"]

    ... # The rest of the function
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func SomeFunction(ctx context.Context, required_param string, extra map[string]interface{}) error {

    // If extra["one"] is present, set someOption to the value of extra["one"]
    if yourValue, ok := extra["one"].(bool); ok {
        someOption = yourValue
    }

    ... // The rest of the function
}
```

{{% /tab %}}
{{% /tabs %}}
