
{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type                                            | Method |
| ----------------------------------------------- | ------ |
| [Arm](/components/arm/)                         | `EndPosition`, `JointPositions` |
| [Board](/components/board/)                     | `Analogs`, `Gpios` |
| [Camera](/components/camera/)                   | `GetImages`, `ReadImage`, `NextPointCloud` |
| [Encoder](/components/encoder/)                 | `TicksCount` |
| [Gantry](/components/gantry/)                   | `Lengths`, `Position` |
| [Motor](/components/motor/)                     | `Position`, `IsPowered` |
| [Movement sensor](/components/movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position` |
| [Sensor](/components/sensor/)                   | `Readings` |
| [Servo](/components/servo/)                     | `Position` |
| [Vision service](/services/vision/)             | `CaptureAllFromCamera` |

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/components/movement-sensor/) | [`AngularVelocity`](/appendix/apis/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/appendix/apis/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/appendix/apis/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/components/sensor/) | [`GetReadings`](/appendix/apis/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}
