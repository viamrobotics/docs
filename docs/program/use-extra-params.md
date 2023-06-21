---
title: "Using Extra Params with Viam's SDKs"
linkTitle: "Extra Params"
weight: 70
type: "docs"
description: "Using the extra parameter on resource API methods with Viam's SDKs."
images: ["/services/img/icons/sdk.svg"]
tags: ["sdk", "extra", "extend"]
---

How to [utilize](#utilize) and [define](#define) the `extra` parameters that many {{< glossary_tooltip term_id="resource" text="resource" >}} API methods offer in the Go and Python SDKs.

## Utilize

Use `extra` parameters to pass information to a {{< glossary_tooltip term_id="resource" text="resource's" >}} driver that is not explicitly specified as a parameter in the [built-in resource type's API specification](/extend/modular-resources/#apis).

To do this, you must code your own modified implementation of the resource type's API for a model.
See [Extend Viam with Modular Resources](/extend/modular-resources/) for more information and [instructions](/extend/modular-resources/#use-a-modular-resource-with-your-robot) on modifying API specifications.

An example of how to check the values of keys in an `extra` parameter of a [built-in resource API method](/program/sdks/), the sensor component's [Readings](/components/sensor/#readings):

{{< tabs >}}
{{% tab name="Python" %}}

``` python {class="line-numbers linkable-line-numbers"}
# Readings depends on extra parameters.
@abc.abstractmethod
async def get_readings(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):

    # Define an empty dictionary for readings.
    readings = {}

    # If extra["type"] is temperature or humidity, get the temperature or humidity from helper functions and return these values as the readings the sensor has provided.
    if extra["type"] is "temperature":
        readings["type"] = get_temp()
    elif extra["type"] is "humidity":
        readings["type"] = get_humidity()
    # If the type is not one of these two cases, raise an exception.
    else: 
        raise Exception(f"Invalid sensor reading request: type {type}")

    return readings
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Readings depends on extra parameters.
func (s *mySensor) Readings(ctx context.Context, extra map[string]interface{}) (map[string]interface{}, error) {

    // Define an empty map for readings.
    readings := map[string]interface{}{}

    // If extra["type"] is temperature or humidity, get the temperature or humidity from helper methods and return these values as the readings the sensor has provided.
    if readingType, ok := extra["type"]; ok {
        rType, ok := readingType.(string)
        if !ok {
            return nil, errors.New("invalid sensor reading request")
        }
        switch rType {
        case "temperature":
            readings[rType] = getTemp()
        case "humidity":
            readings[rType] = getHumidity()
        // If the type is not one of these two cases, return an error.
        default:
            return nil, errors.Errorf("Invalid sensor reading request: type %s", rType)
        }
    }

    // Return the readings and `nil`/no error.
    return readings, nil
}
```

{{% /tab %}}
{{% /tabs %}}

## Define

{{< tabs >}}
{{% tab name="Python" %}}

[`Optional[Dict[str, Any]]`](https://docs.python.org/3/library/typing.html#typing.Optional) indicates you are required to pass in an object of either type `Dict[str, Any]` or `None` as a parameter when calling this method.

An object of type `Dict[str, Any]` is a [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) with keys of type [`str`](https://docs.python.org/3/library/stdtypes.html#str) and values of [`any type`](https://docs.python.org/3/library/typing.html#typing.Any),

For example:

``` python {class="line-numbers linkable-line-numbers"}
async def main():
    ... # Connect to the robot.

    # Get your sensor resource from the robot.
    your_sensor = YourSensor.from_robot(robot, "your-sensor")
    
    # Define a dictionary containing extra information.
    your_info = {"type": "temperature", "description": "more info", "id": 123}

    # Send this information in an call to the sensor resource's API.
    await your_sensor.get_readings(extra=your_info)
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

    // Get your sensor resource from the robot.
    yourSensor, err := YourSensor.FromRobot(robot, "your-sensor")

    // Define a map containing extra information.
    your_info := map[string]interface{}{"type": "temperature", "description": "more info", "id": 123}

    // Send this information in an call to the sensor resource's API.
    err := yourSensor.Readings(context.Background(), your_info)
}
```

{{% alert title="Note" color="note" %}}

If passing an object of type `nil`, you must specify `nil` in the method call or the method will fail.

{{% /alert %}}
{{% /tab %}}
{{% /tabs %}}
