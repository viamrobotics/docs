{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type                                            | Method |
| ----------------------------------------------- | ------ |
| [Arm](/operate/reference/components/arm/)                         | `EndPosition`, `JointPositions` |
| [Board](/operate/reference/components/board/)                     | `Analogs`, `Gpios` |
| [Camera](/operate/reference/components/camera/)                   | `GetImages`, `ReadImage`, `NextPointCloud` |
| [Encoder](/operate/reference/components/encoder/)                 | `TicksCount` |
| [Gantry](/operate/reference/components/gantry/)                   | `Lengths`, `Position` |
| [Motor](/operate/reference/components/motor/)                     | `Position`, `IsPowered` |
| [Movement sensor](/operate/reference/components/movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position` |
| [Sensor](/operate/reference/components/sensor/)                   | `Readings` |
| [Servo](/operate/reference/components/servo/)                     | `Position` |
| [Vision service](/operate/reference/services/vision/)             | `CaptureAllFromCamera` |

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/operate/reference/components/movement-sensor/) | [`AngularVelocity`](/dev/reference/apis/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/dev/reference/apis/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/dev/reference/apis/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/operate/reference/components/sensor/) | [`GetReadings`](/dev/reference/apis/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}
