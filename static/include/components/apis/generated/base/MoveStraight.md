### MoveStraight

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: move_straight

Move the base in a straight line the given distance, expressed in millimeters, at the given velocity, expressed in millimeters per second. When distance or velocity is 0, the base will stop. This method blocks until completed or cancelled.

**Parameters:**

- `distance` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required) The distance (in millimeters) to move. Negative implies backwards.:
- `distance`- `velocity` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required) The velocity (in millimeters per second) to move. Negative implies backwards.:
- `velocity`- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional) Extra options to pass to the underlying RPC call.:
- `extra`- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional) An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.:
- `timeout`

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.move_straight).

``` python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Move the base 40 mm at a velocity of 90 mm/s, forward.
await my_base.move_straight(distance=40, velocity=90)

# Move the base 40 mm at a velocity of -90 mm/s, backward.
await my_base.move_straight(distance=40, velocity=-90)

```

\{\{% /tab %}}

\{\{% tab name="Go" %\}\}

Go Method: MoveStraight

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `distanceMm`[(int)](<INSERT PARAM TYPE LINK>)
- `mmPerSec`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: moveStraight

**Parameters:**

- `distanceMm` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `distanceMm`- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra`- `mmPerSec` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `mmPerSec`- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name`

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/moveStraight.html).

\{\{% /tab %}}

\{\{< /tabs >}}

