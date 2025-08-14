{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type                                            | Method |
| ----------------------------------------------- | ------ |
| [Arm](/operate/reference/components/arm/)                         | `EndPosition`, `JointPositions`, `DoCommand` |
| [Board](/operate/reference/components/board/)                     | `Analogs`, `Gpios`, `DoCommand` |
| [Camera](/operate/reference/components/camera/)                   | `GetImages`, `ReadImage`, `NextPointCloud`, `DoCommand` |
| [Encoder](/operate/reference/components/encoder/)                 | `TicksCount`, `DoCommand` |
| [Gantry](/operate/reference/components/gantry/)                   | `Lengths`, `Position`, `DoCommand` |
| [Motor](/operate/reference/components/motor/)                     | `Position`, `IsPowered`, `DoCommand` |
| [Movement sensor](/operate/reference/components/movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `DoCommand` |
| [Sensor](/operate/reference/components/sensor/)                   | `Readings`, `DoCommand` |
| [Servo](/operate/reference/components/servo/)                     | `Position`, `DoCommand` |
| [Vision service](/operate/reference/services/vision/)             | `CaptureAllFromCamera`, `DoCommand` |
| [SLAM service](/operate/reference/services/slam/)             | `Position`, `PointCloudMap`, `DoCommand` |

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/operate/reference/components/movement-sensor/) | [`AngularVelocity`](/dev/reference/apis/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/dev/reference/apis/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/dev/reference/apis/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/operate/reference/components/sensor/) | [`GetReadings`](/dev/reference/apis/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}
