{{< tabs >}}
{{% tab name="viam-server" %}}

<!-- prettier-ignore -->
| Type                                            | Method |
| ----------------------------------------------- | ------ |
| [Arm](/hardware/common-components/add-an-arm/)                         | `EndPosition`, `JointPositions`, `DoCommand` |
| [Base](/hardware/common-components/add-a-base/)                       | `Position`, `DoCommand` |
| [Board](/hardware/common-components/add-a-board/)                     | `Analogs`, `Gpios`, `DoCommand` |
| [Button](/hardware/common-components/add-a-button/)                   | `DoCommand` |
| [Camera](/hardware/common-components/add-a-camera/)                   | `GetImages`, `ReadImage` (deprecated), `NextPointCloud`, `DoCommand` |
| [Encoder](/hardware/common-components/add-an-encoder/)                 | `TicksCount`, `DoCommand` |
| [Gantry](/hardware/common-components/add-a-gantry/)                   | `Lengths`, `Position`, `DoCommand` |
| [Gripper](/hardware/common-components/add-a-gripper/)                 | `DoCommand` |
| [Input Controller](/hardware/common-components/add-an-input-controller/) | `DoCommand` | 
| [Motor](/hardware/common-components/add-a-motor/)                     | `Position`, `IsPowered`, `DoCommand` |
| [Movement sensor](/hardware/common-components/add-a-movement-sensor/) | `AngularVelocity`, `CompassHeading`, `LinearAcceleration`, `LinearVelocity`, `Orientation`, `Position`, `DoCommand` |
| [Sensor](/hardware/common-components/add-a-sensor/)                   | `Readings`, `DoCommand` |
| [Power sensor](/hardware/common-components/add-a-power-sensor/)       | `Voltage`, `Current`, `Power`, `DoCommand` |
| [Servo](/hardware/common-components/add-a-servo/)                     | `Position`, `DoCommand` |
| [Switch](/hardware/common-components/add-a-switch/)                   | `DoCommand` |
| [Generic](/hardware/common-components/add-a-generic/)                 | `DoCommand` |
| [Base remote control service](/operate/reference/services/base-rc/) | `DoCommand` |
| [Discovery service](/operate/reference/services/discovery/)       | `DoCommand` |
| [Vision service](/vision/configure/)             | `CaptureAllFromCamera`, `DoCommand` |
| [SLAM service](/operate/reference/services/slam/)                 | `Position`, `PointCloudMap`, `DoCommand` |
| [Motion service](/operate/reference/services/motion/)             | `DoCommand` |
| [Navigation service](/operate/reference/services/navigation/)     | `DoCommand` |
| Shell service | `DoCommand` |

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Type | Method |
| ---- | ------ |
| [Movement Sensor](/hardware/common-components/add-a-movement-sensor/) | [`AngularVelocity`](/reference/apis/components/movement-sensor/#getangularvelocity), [`LinearAcceleration`](/reference/apis/components/movement-sensor/#getlinearacceleration), [`LinearVelocity`](/reference/apis/components/movement-sensor/#getlinearvelocity) |
| [Sensor](/hardware/common-components/add-a-sensor/) | [`GetReadings`](/reference/apis/components/sensor/#getreadings) |

{{% /tab %}}
{{< /tabs >}}
