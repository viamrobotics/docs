{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type                                            | Method |
| ----------------------------------------------- | ------ |
| [Arm](/operate/reference/components/arm/)                         | `EndPosition`, `JointPositions`, `DoCommand` |
| [Base](/operate/reference/components/base/)                       | `Position`, `DoCommand` |
| [Board](/operate/reference/components/board/)                     | `Analogs`, `Gpios`, `DoCommand` |
| [Button](/operate/reference/components/button/)                   | `DoCommand` |
| [Camera](/operate/reference/components/camera/)                   | `GetImages`, `ReadImage` (deprecated), `NextPointCloud`, `DoCommand` |
| [Encoder](/operate/reference/components/encoder/)                 | `TicksCount`, `DoCommand` |
| [Gantry](/operate/reference/components/gantry/)                   | `Lengths`, `Position`, `DoCommand` |
| [Gripper](/operate/reference/components/gripper/)                 | `DoCommand` |
| [Input Controller](/operate/reference/components/input-controller/) | `DoCommand` | 
| [Motor](/operate/reference/components/motor/)                     | `Position`, `IsPowered`, `DoCommand` |
| [Movement sensor](/operate/reference/components/movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `DoCommand` |
| [Sensor](/operate/reference/components/sensor/)                   | `Readings`, `DoCommand` |
| [Power sensor](/operate/reference/components/power-sensor/)       | `Voltage`, `Current`, `Power`, `DoCommand` |
| [Servo](/operate/reference/components/servo/)                     | `Position`, `DoCommand` |
| [Switch](/operate/reference/components/switch/)                   | `DoCommand` |
| [Generic](/operate/reference/components/generic/)                 | `DoCommand` |
| [Base remote control service](/operate/reference/services/base-rc/) | `DoCommand` |
| [Discovery service](/operate/reference/services/discovery/)       | `DoCommand` |
| [Vision service](/operate/reference/services/vision/)             | `CaptureAllFromCamera`, `DoCommand` |
| [SLAM service](/operate/reference/services/slam/)                 | `Position`, `PointCloudMap`, `DoCommand` |
| [Motion service](/operate/reference/services/motion/)             | `DoCommand` |
| [Navigation service](/operate/reference/services/navigation/)     | `DoCommand` |
| Shell service | `DoCommand` |

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/operate/reference/components/movement-sensor/) | [`AngularVelocity`](/dev/reference/apis/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/dev/reference/apis/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/dev/reference/apis/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/operate/reference/components/sensor/) | [`GetReadings`](/dev/reference/apis/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}
