### GetKinematics

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: get_kinematics

Get the kinematics information associated with the arm.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional) Extra options to pass to the underlying RPC call.:
- `extra`- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional) An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.:
- `timeout`

**Returns:**

- [(Tuple[viam.components.arm.KinematicsFileFormat.ValueType, bytes])](INSERT RETURN TYPE LINK):  A tuple containing two values; the first [0] value represents the format of thefile, either in URDF format or Viam’s kinematic parameter format (spatial vector algebra), and the second [1] value represents the byte contents of the file.   

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_kinematics).

``` python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the kinematics information associated with the arm.
kinematics = await my_arm.get_kinematics()

# Get the format of the kinematics file.
k_file = kinematics[0]

# Get the byte contents of the file.
k_bytes = kinematics[1]

```

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: getKinematics

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra`- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name`

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.arm/ArmServiceClient/getKinematics.html).

\{\{% /tab %}}

\{\{< /tabs >}}

