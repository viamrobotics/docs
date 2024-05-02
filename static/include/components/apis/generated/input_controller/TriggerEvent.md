### TriggerEvent

{{< tabs >}}
{{% tab name="Python" %}}

Directly send an Event (such as a button press) from external code

**Parameters:**

- `event` [(viam.components.input.input.Event)](<INSERT PARAM TYPE LINK>) (required): The event to trigger
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/input/client/index.html#viam.components.input.client.ControllerClient.trigger_event).

``` python {class="line-numbers linkable-line-numbers"}
# Define a "Button is Pressed" event for the control BUTTON_START.
button_is_pressed_event = Event(
    time(), EventType.BUTTON_PRESS, Control.BUTTON_START, 1.0)

# Trigger the event on your controller. Set this trigger to timeout if it has
# not completed in 7 seconds.
await myController.trigger_event(event=my_event, timeout=7.0)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `event`[(Event)](https://pkg.go.dev#Event):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/input#Triggerable).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `controller` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `event` [(Event)](https://flutter.viam.dev/viam_protos.component.input_controller/Event-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.input_controller/InputControllerServiceClient/triggerEvent.html).

{{% /tab %}}
{{< /tabs >}}
