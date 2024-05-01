### Spin

{{< tabs >}}
{{% tab name="Python" %}}

Spin the base in place angle degrees, at the given angular velocity, expressed in degrees per second. When velocity is 0, the base will stop. This method blocks until completed or cancelled.

**Parameters:**

- `angle` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The angle (in degrees) to spin.
- `velocity` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The angular velocity (in degrees per second) to spin. Given a positive angle and a positive velocity, the base will turn to the left.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.spin).

``` python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=robot, name="my_base")

# Spin the base 10 degrees at an angular velocity of 15 deg/sec.
await my_base.spin(angle=10, velocity=15)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- [(angleDeg)](<INSERT PARAM TYPE LINK>)
- `degsPerSec`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `angleDeg` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `degsPerSec` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.base/BaseServiceClient/spin.html).

{{% /tab %}}
{{< /tabs >}}
